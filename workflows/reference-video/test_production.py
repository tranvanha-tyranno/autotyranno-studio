"""Regression cases for stale inspections, exact speech, isolated assets and resume."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image

import production as p


class ProductionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.asset = self.root / 'assets/example.jpg'
        self.asset.parent.mkdir()
        Image.new('RGB', (128, 96), 'green').save(self.asset)
        digest = p.sha(self.asset)
        self.manifest = {'schema': 'reference-video-production/1', 'id': 'test-original', 'direction': 'long',
            'title': 'An original test', 'editorialAngle': 'Concrete choice then its mechanism',
            'audience': 'People considering a household choice', 'hookPromise': 'Explain the choice',
            'payoff': 'A practical way to compare', 'sections': [], 'assets': [{
                'id': 'example', 'file': 'assets/example.jpg', 'sha256': digest,
                'source': {'kind': 'original', 'url': 'original:fixture', 'creator': 'Test author',
                           'license': 'Original test asset', 'licenseURL': 'original:permission'},
                'observed': {'subject': 'A green test image', 'action': 'Static', 'objects': 'Plain colour',
                             'limits': 'No real-world claim is shown'},
                'inspection': {'status': 'inspected', 'reviewer': 'Test reviewer', 'sha256': digest,
                               'observations': 'Opened the fixture; plain green pixels only.'}}]}
        for phase, text in zip(p.PHASES, ['One choice.', 'An illustration.', 'Compare the whole cost.', 'Try it.']):
            self.manifest['sections'].append({'phase': phase, 'text': text, 'shots': [{
                'id': phase, 'phrase': text.split()[0], 'narrationClause': text,
                'needToSee': 'A neutral illustrative visual', 'mediaRole': 'metaphor',
                'supports': 'A placeholder for this test only', 'limits': 'No factual claim about people',
                'layout': 'full', 'images': ['example'], 'review': {'status': 'inspected',
                    'reviewer': 'Test reviewer', 'observations': 'The image remains a test metaphor.',
                    'assetHashes': {'example': digest}}}]})
        self.path = self.root / 'production.json'
        self.batch = self.root / 'batch'
        self.write()

    def tearDown(self):
        self.temp.cleanup()

    def write(self):
        p.save(self.path, self.manifest)

    def audio(self, receipt_override=None):
        _, folder = p.plan(self.path, self.batch)
        audio = folder / 'audio/narration-original.mp3'
        audio.parent.mkdir()
        audio.write_bytes(b'pretend-audio-tested-with-duration-stub')
        text = p.writing_text(self.manifest)
        payload = {'text': text, 'model_id': 'eleven_v3', 'language_code': 'vi',
                   'voice_settings': {'stability': .5, 'similarity_boost': .8, 'speed': 1.0}}
        endpoint = f'/v1/text-to-speech/{p.VOICE}/with-timestamps'
        digest = hashlib.sha256(json.dumps({'endpoint': endpoint, 'body': payload}, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        receipt = {'sha256': p.sha(audio), 'request_hash': digest}
        receipt.update(receipt_override or {})
        p.save(audio.with_suffix('.receipt.json'), receipt)
        p.save(audio.with_suffix('.alignment.json'), {'characters': list(text),
            'character_start_times_seconds': [i * .05 for i in range(len(text))],
            'character_end_times_seconds': [(i + 1) * .05 for i in range(len(text))]})
        return folder

    def test_every_spoken_word_must_have_one_ordered_visual_clause(self):
        self.manifest['sections'][2]['shots'][0]['narrationClause'] = 'Compare the cost.'
        self.write()
        with self.assertRaisesRegex(ValueError, 'every narration word'):
            p.check(self.path, self.batch)

    def test_duplicate_clause_cannot_be_found_later_and_silently_shift_cuts(self):
        original = self.manifest['sections'][2]['shots'][0]
        original['narrationClause'] = 'Compare the whole'
        second = copy.deepcopy(original)
        second.update({'id': 'content2', 'phrase': 'Compare', 'narrationClause': 'cost.'})
        self.manifest['sections'][2]['shots'].append(second)
        self.write()
        with self.assertRaisesRegex(ValueError, 'must open'):
            p.check(self.path, self.batch)

    def test_catalog_labels_do_not_bypass_pending_visual_inspection(self):
        self.manifest['assets'][0]['inspection']['status'] = 'pending'
        self.write()
        with self.assertRaisesRegex(ValueError, 'inspection remains pending'):
            p.check(self.path, self.batch)

    def test_changing_pixels_invalidates_all_prior_visual_notes(self):
        Image.new('RGB', (128, 96), 'red').save(self.asset)
        with self.assertRaisesRegex(ValueError, 'differs from catalog'):
            p.check(self.path, self.batch)

    def test_scene_review_hashes_are_not_inferred_from_asset_labels(self):
        self.manifest['sections'][2]['shots'][0]['review']['assetHashes'] = {'example': '0' * 64}
        self.write()
        with self.assertRaisesRegex(ValueError, 'exact selected assets'):
            p.check(self.path, self.batch)

    def test_stock_cannot_be_passed_as_evidence_of_a_specific_claim(self):
        self.manifest['assets'][0]['source'].update({'kind': 'stock', 'url': 'https://example.com/image', 'licenseURL': 'https://example.com/license'})
        self.manifest['sections'][2]['shots'][0]['mediaRole'] = 'evidence'
        self.write()
        with self.assertRaisesRegex(ValueError, 'illustrative stock'):
            p.check(self.path, self.batch)

    def test_asset_path_cannot_escape_manifest_root(self):
        self.manifest['assets'][0]['file'] = '../outside.jpg'
        self.write()
        with self.assertRaisesRegex(ValueError, 'leaves its declared root'):
            p.check(self.path, self.batch)

    def test_prepare_uses_new_batch_sources_and_never_marks_aesthetic_acceptance(self):
        folder = self.audio()
        with patch('documentary.duration', return_value=8):
            p.prepare(self.path, self.batch)
        data = p.load(folder / 'data.json')
        self.assertEqual(data['shots'][0]['start'], 0)
        self.assertEqual(data['shots'][-1]['end'], 9 * 30)
        self.assertTrue(all(a['end'] == b['start'] for a, b in zip(data['shots'], data['shots'][1:])))
        derivative = self.batch / 'production-public/directions/long/example.jpg'
        self.assertTrue(derivative.is_file())
        self.assertEqual(p.load(folder / 'preflight.json')['userAcceptance'], 'pending')
        self.assertEqual(p.load(folder / 'render-assets.json')['assets'][0]['originalSHA256'], p.sha(self.asset))

    def test_wrong_voice_or_speed_receipt_cannot_be_reused_for_new_script(self):
        self.audio({'request_hash': 'different-voice-or-speed'})
        with patch('documentary.duration', return_value=8):
            with self.assertRaisesRegex(ValueError, 'pinned Vietnamese voice'):
                p.prepare(self.path, self.batch)

    def test_selected_derivative_keeps_its_name_beside_a_raw_original(self):
        selected = self.asset.with_name('example-720p.jpg')
        self.asset.rename(selected)
        self.asset = selected
        self.manifest['assets'][0]['file'] = 'assets/example-720p.jpg'
        self.write()
        folder = self.audio()
        raw = folder / 'assets/example.jpg'
        raw.parent.mkdir()
        Image.new('RGB', (256, 192), 'red').save(raw)
        before = p.sha(raw)
        with patch('documentary.duration', return_value=8):
            p.prepare(self.path, self.batch)
        self.assertEqual(p.sha(raw), before)
        self.assertEqual(p.load(folder / 'image-sources.json')[0]['file'], 'assets/example-720p.jpg')
        self.assertTrue((folder / 'assets/example-720p.jpg').exists())

    def test_actual_word_alignment_must_equal_final_script(self):
        folder = self.audio()
        aligned = folder / 'audio/narration-original.alignment.json'
        value = p.load(aligned)
        value['characters'][0] = 'X'
        p.save(aligned, value)
        with patch('documentary.duration', return_value=8):
            with self.assertRaisesRegex(ValueError, 'differs from complete final script'):
                p.prepare(self.path, self.batch)

    def video_asset(self, available_frames=60):
        import cv2
        import numpy as np
        file = self.root / 'assets/moving.mp4'
        writer = cv2.VideoWriter(str(file), cv2.VideoWriter_fourcc(*'mp4v'), 30, (160, 90))
        self.assertTrue(writer.isOpened())
        for i in range(60):
            writer.write(np.full((90, 160, 3), i * 3, dtype=np.uint8))
        writer.release()
        asset = self.manifest['assets'][0]
        asset.update({'file': 'assets/moving.mp4', 'mediaType': 'video', 'availableFrames': available_frames})
        asset['sha256'] = p.sha(file)
        asset['inspection']['sha256'] = asset['sha256']
        for section in self.manifest['sections']:
            section['shots'][0]['review']['assetHashes'] = {'example': asset['sha256']}
        self.write()

    def test_real_video_duration_uses_decoded_frames_and_never_fills_by_loop(self):
        self.video_asset(available_frames=8)
        self.audio()
        with patch('documentary.duration', return_value=8):
            with self.assertRaisesRegex(ValueError, 'without looping/freezing'):
                p.prepare(self.path, self.batch)

    def test_clip_cannot_declare_more_frames_than_decoded_source(self):
        self.video_asset(available_frames=600)
        with self.assertRaisesRegex(ValueError, 'actual decoded duration'):
            p.check(self.path, self.batch)

    def test_renderer_stages_only_the_selected_batch_and_checks_derivative_bytes(self):
        import render_directions
        folder = self.audio()
        with patch('documentary.duration', return_value=8):
            p.prepare(self.path, self.batch)
        mix = folder / 'audio/final-mix.wav'
        mix.write_bytes(b'audio hash only fixture')
        p.save(folder / 'audio-sources.json', {'mix': {'sha256': p.sha(mix)}})
        public = self.batch / 'production-public'
        films = render_directions.preflight(self.batch, ['long'], public)
        selected = films['long']['assets']['directions/long/example.jpg']
        self.assertTrue(selected.is_relative_to(public))
        selected.write_bytes(b'changed derivative')
        with self.assertRaisesRegex(ValueError, 'derivative missing/changed'):
            render_directions.preflight(self.batch, ['long'], public)

    def test_queue_resume_does_not_repeat_paid_speech_and_detects_tampering(self):
        queue = self.root / 'queue.json'
        p.save(queue, {'schema': 'reference-video-queue/1', 'jobs': [{'id': 'one', 'manifest': self.path.name,
            'batch': 'batch', 'steps': ['plan', 'check', 'voice']}]})

        def stub(*args):
            folder = self.batch / 'long/audio'
            folder.mkdir(parents=True, exist_ok=True)
            for name in ['narration-original.mp3', 'narration-original.receipt.json', 'narration-original.alignment.json']:
                (folder / name).write_text('test voice result', encoding='utf-8')

        with patch.object(p, 'voice', side_effect=stub) as speech:
            p.queue(queue)
            p.queue(queue)
            self.assertEqual(speech.call_count, 1)
            (self.batch / 'long/audio/narration-original.mp3').write_text('changed', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Completed queue output changed'):
                p.queue(queue)
            self.assertEqual(speech.call_count, 1)

    def test_failed_step_stops_queue_and_requires_explicit_retry(self):
        queue = self.root / 'queue.json'
        p.save(queue, {'schema': 'reference-video-queue/1', 'jobs': [{'id': 'one', 'manifest': self.path.name,
            'batch': 'batch', 'steps': ['plan', 'check', 'voice']}]})
        with patch.object(p, 'voice', side_effect=RuntimeError('unresolved provider intent')) as speech:
            with self.assertRaisesRegex(RuntimeError, 'unresolved provider'):
                p.queue(queue)
            with self.assertRaisesRegex(ValueError, '--retry-failed'):
                p.queue(queue)
            self.assertEqual(speech.call_count, 1)
        state = p.load(queue.with_suffix('.state.json'))
        self.assertEqual(state['jobs']['one']['status'], 'failed')
        self.assertEqual(state['jobs']['one']['steps']['voice']['attempt'], 1)

    def test_guidance_is_a_verified_export_and_pinned_to_initial_plan(self):
        guidance = self.root / 'guidance.json'
        p.save(guidance, {'schema': 'reference-video-guidance/1', 'lessons': []})
        _, folder = p.plan(self.path, self.batch, guidance)
        before = p.sha(folder / 'learning-guidance.json')
        p.plan(self.path, self.batch)
        self.assertEqual(p.sha(folder / 'learning-guidance.json'), before)
        p.save(guidance, {'schema': 'reference-video-guidance/1', 'lessons': [], 'new-version': True})
        with self.assertRaisesRegex(ValueError, 'already pinned'):
            p.plan(self.path, self.batch, guidance)
        self.assertEqual(p.sha(folder / 'learning-guidance.json'), before)

    def test_unverified_guidance_is_not_promoted_by_check(self):
        guidance = self.root / 'guidance.json'
        p.save(guidance, {'schema': 'reference-video-guidance/1', 'lessons': [{'id': 'proposal', 'status': 'proposed'}]})
        with self.assertRaisesRegex(ValueError, 'unverified lessons'):
            p.check(self.path, self.batch, guidance)

    def test_guidance_cannot_be_inserted_after_planning_without_a_new_revision(self):
        p.plan(self.path, self.batch)
        guidance = self.root / 'guidance.json'
        p.save(guidance, {'schema': 'reference-video-guidance/1', 'lessons': []})
        with self.assertRaisesRegex(ValueError, 'after planning'):
            p.plan(self.path, self.batch, guidance)

    def test_bounded_memory_profile_changes_only_requested_render_controls(self):
        from render_directions import render_arguments, resolved_render_options
        defaults = resolved_render_options(3, 19)
        self.assertEqual(defaults['concurrency'], 3)
        default_argv = render_arguments('props.json', defaults)
        self.assertIn('--concurrency=3', default_argv)
        self.assertFalse(any('cache' in value for value in default_argv))
        bounded = resolved_render_options(3, 19, 'bounded')
        argv = render_arguments('props.json', bounded)
        self.assertIn('--concurrency=1', argv)
        self.assertIn('--media-cache-size-in-bytes=268435456', argv)
        self.assertIn('--crf=19', argv)
        self.assertFalse(any('offthread' in value or 'hardware' in value or 'parallel-encoding' in value for value in argv))

    def test_production_forwards_memory_profile_only_when_manifest_requests_it(self):
        with patch.object(p.subprocess, 'run') as process:
            p.render(self.path, self.batch)
            self.assertNotIn('--memory-profile', process.call_args.args[0])
        self.manifest['renderOptions'] = {'memoryProfile': 'bounded'}
        self.write()
        with patch.object(p.subprocess, 'run') as process:
            p.render(self.path, self.batch)
            argv = process.call_args.args[0]
            self.assertEqual(argv[argv.index('--memory-profile') + 1], 'bounded')
            self.assertIn('--skip-existing', argv)

    def test_unknown_memory_profile_cannot_silently_change_renderer(self):
        self.manifest['renderOptions'] = {'memoryProfile': 'unlimited'}
        self.write()
        with self.assertRaisesRegex(ValueError, 'memoryProfile'):
            p.check(self.path, self.batch)


    def test_country_preference_does_not_invent_a_location_for_existing_assets(self):
        self.manifest['visualPolicy'] = {'preferredCountry': 'VN', 'requireLocationEvidence': True}
        self.write()
        p.check(self.path, self.batch)  # Original mechanisms and unknown/foreign context remain usable.
        self.manifest['assets'][0]['location'] = {'countryCode': 'VN', 'place': 'Hanoi'}
        self.write()
        with self.assertRaisesRegex(ValueError, 'location evidence'):
            p.check(self.path, self.batch)

    def test_preferred_country_needs_source_evidence_not_an_ethnicity_label(self):
        self.manifest['visualPolicy'] = {'preferredCountry': 'VN', 'requireLocationEvidence': True}
        self.manifest['assets'][0]['location'] = {'countryCode': 'VN', 'place': 'Hanoi',
            'sourceURL': 'original:looks-Vietnamese', 'evidence': 'Appearance is not a location receipt.'}
        self.write()
        with self.assertRaisesRegex(ValueError, 'HTTPS sourceURL'):
            p.check(self.path, self.batch)

    def test_explicit_disclaimer_is_opt_in_and_requires_a_brief_visible_body(self):
        p.check(self.path, self.batch)
        self.manifest['visualPolicy'] = {'explicitDisclaimer': True}
        self.write()
        with self.assertRaisesRegex(ValueError, 'literal Vietnamese heading'):
            p.check(self.path, self.batch)
        shot = self.manifest['sections'][1]['shots'][0]
        shot['eyebrow'] = 'MIỄN TRỪ TRÁCH NHIỆM'
        shot['body'] = ' '.join(['word'] * 46)
        self.write()
        with self.assertRaisesRegex(ValueError, 'brief relevant body'):
            p.check(self.path, self.batch)
        shot['body'] = 'Ví dụ minh họa; hành vi thực tế có thể khác.'
        self.write()
        p.check(self.path, self.batch)
        self.assertEqual(p.writing_text(self.manifest), 'One choice.\n\nAn illustration.\n\nCompare the whole cost.\n\nTry it.')

    def test_motion_rejects_unused_options_bad_cues_and_unpinned_prices(self):
        shot = self.manifest['sections'][2]['shots'][0]
        shot['layout'] = 'object3d'
        cases = [None, {'kind': 'random'}, {'kind': 'basket', 'stage': 'total'},
                 {'kind': 'price', 'price': 10000}, {'kind': 'price', 'stage': 'offer'},
                 {'kind': 'basket', 'revealFrames': [True]}, {'kind': 'basket', 'revealFrames': [float('nan')]},
                 {'kind': 'basket', 'revealFrames': [-1]}, {'kind': 'basket', 'revealFrames': [8, 8]},
                 {'kind': 'basket', 'revealFrames': [9, 8]}, {'kind': 'basket', 'revealFrames': [0, 1, 2, 3]}]
        for motion in cases:
            with self.subTest(motion=motion):
                shot['motion'] = motion
                with self.assertRaises(ValueError):
                    p.validate_structure(self.manifest)
        shot['layout'], shot['motion'] = 'full', {'kind': 'basket'}
        with self.assertRaisesRegex(ValueError, 'only rendered'):
            p.validate_structure(self.manifest)

    def test_exact_take_bounds_all_motion_cues(self):
        shot = self.manifest['sections'][2]['shots'][0]
        shot.update({'layout': 'object3d', 'motion': {'kind': 'basket', 'revealFrames': [1000]}})
        self.write()
        self.audio()
        with patch('documentary.duration', return_value=8):
            with self.assertRaisesRegex(ValueError, 'outside its exact narrated shot'):
                p.prepare(self.path, self.batch)

    def test_dedicated_disclaimer_does_not_silently_swallow_object_motion(self):
        self.manifest['sections'][1]['shots'][0].update({'layout': 'object3d', 'motion': {'kind': 'journey'}})
        with self.assertRaisesRegex(ValueError, 'dedicated layout'):
            p.validate_structure(self.manifest)

    def test_object3d_video_context_requires_a_hash_checked_poster(self):
        self.video_asset()
        shot = self.manifest['sections'][2]['shots'][0]
        shot.update({'layout': 'object3d', 'motion': {'kind': 'basket'}})
        self.write()
        with self.assertRaisesRegex(ValueError, 'poster derivative'):
            p.check(self.path, self.batch)
        self.manifest['assets'][0].update({'posterFile': 'assets/example.jpg', 'posterSHA256': p.sha(self.asset)})
        self.write()
        p.check(self.path, self.batch)
        Image.new('RGB', (128, 96), 'red').save(self.asset)
        with self.assertRaisesRegex(ValueError, 'poster differs'):
            p.check(self.path, self.batch)

    def test_prepare_preserves_motion_location_receipts_and_nonoverlapping_country_timing(self):
        self.manifest['visualPolicy'] = {'preferredCountry': 'VN', 'requireLocationEvidence': True}
        location = {'countryCode': 'VN', 'place': 'Hanoi', 'sourceURL': 'https://example.com/location-receipt',
                    'evidence': 'Test receipt names Hanoi; this fixture does not depict a real place.'}
        self.manifest['assets'][0]['location'] = location
        motion = {'kind': 'price', 'stage': 'total', 'revealFrames': [0, 10, 20]}
        self.manifest['sections'][2]['shots'][0].update({'layout': 'object3d', 'motion': motion})
        self.write()
        folder = self.audio()
        with patch('documentary.duration', return_value=8):
            p.prepare(self.path, self.batch)
        data, preflight = p.load(folder / 'data.json'), p.load(folder / 'preflight.json')
        self.assertEqual(data['shots'][2]['motion'], motion)
        self.assertEqual(p.load(folder / 'image-sources.json')[0]['location'], location)
        coverage = preflight['visualCoverage']
        self.assertEqual(coverage['preferredCountryAssetCount'], 1)
        object_seconds = (data['shots'][2]['end'] - data['shots'][2]['start']) / 30
        self.assertEqual(coverage['preferredCountryPresenceSeconds'], 9 - object_seconds)
        self.assertAlmostEqual(coverage['preferredCountryPresenceShare'], (9 - object_seconds) / 9)
        self.assertEqual(coverage['shots'][2]['documentedCountries'], [])  # Geometry-only price shows no retained photo.
        self.assertEqual(coverage['object3DSeconds'], object_seconds)
        self.assertEqual(preflight['userAcceptance'], 'pending')

    def test_mixed_country_presence_is_not_reported_as_exclusively_vietnamese(self):
        foreign = copy.deepcopy(self.manifest['assets'][0])
        foreign.update({'id': 'foreign', 'location': {'countryCode': 'US', 'place': 'US test location',
            'sourceURL': 'https://example.com/us', 'evidence': 'Source names US.'}})
        self.manifest['assets'].append(foreign)
        self.manifest['visualPolicy'] = {'preferredCountry': 'VN'}
        self.manifest['assets'][0]['location'] = {'countryCode': 'VN'}  # An unsupported declaration counts as unknown.
        shots = []
        for index, section in enumerate(self.manifest['sections']):
            section['shots'][0]['images'] = ['example', 'foreign']
            shots.append({**section['shots'][0], 'start': index * 30, 'end': (index + 1) * 30})
        self.assertEqual(p.visual_coverage(self.manifest, shots, 30)['documentedCountryPresenceSeconds'], {})
        for shot in shots:
            shot['layout'] = 'diptych'
        coverage = p.visual_coverage(self.manifest, shots, 30)
        self.assertEqual(coverage['documentedCountryPresenceSeconds'], {'US': 4})
        self.assertEqual(coverage['preferredCountryPresenceSeconds'], 0)
        self.assertEqual(coverage['preferredCountryAssetCount'], 0)

    def test_legacy_preparation_does_not_add_motion_or_country_policy(self):
        folder = self.audio()
        with patch('documentary.duration', return_value=8):
            p.prepare(self.path, self.batch)
        self.assertNotIn('visualCoverage', p.load(folder / 'preflight.json'))
        self.assertTrue(all('motion' not in shot for shot in p.load(folder / 'data.json')['shots']))
        self.assertNotIn('location', p.load(folder / 'image-sources.json')[0])


if __name__ == '__main__':
    unittest.main()
