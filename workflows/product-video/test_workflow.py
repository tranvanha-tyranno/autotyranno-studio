"""Checks for duplicate billing prevention and preserving full-speed footage."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import json
from unittest.mock import patch
import base64
import io
from PIL import Image

spec = importlib.util.spec_from_file_location('product_video_runner', Path(__file__).with_name('run.py'))
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class WorkflowTests(unittest.TestCase):
    def test_full_24fps_scene_keeps_two_hundred_frames_after_1_5x_conversion(self):
        module = runner.storyboard_module()
        with tempfile.TemporaryDirectory() as directory:
            batch = Path(directory)
            scene = {'seconds': 20/3, 'visual_speed': 1.5, 'dialogue': 'A',
                     'opening_prompt': 'image', 'video_prompt': 'video'}
            clip = {'slug': 'fps24-test', 'scenes': [scene]}
            sf = module.folder(runner, batch, 1, clip, 1)
            vf = module.voice_folder(runner, sf)
            vf.mkdir(parents=True)
            Image.new('RGB', (72, 128), 'purple').save(sf/'opening.png')
            import hashlib
            runner.save_json(sf/'opening-review.json', {
                'result': 'accepted', 'sha256': hashlib.sha256((sf/'opening.png').read_bytes()).hexdigest()})
            (vf/'dialogue.txt').write_text('A', encoding='utf-8')
            runner.run_ff([runner.FF, '-y', '-f', 'lavfi', '-i',
                           'color=c=purple:s=72x128:r=24:d=10',
                           '-c:v', 'libx264', '-preset', 'ultrafast', str(sf/'source.mp4')])
            runner.run_ff([runner.FF, '-y', '-f', 'lavfi', '-i',
                           'sine=frequency=440:duration=1',
                           '-c:a', 'libmp3lame', str(vf/'voice.mp3')])
            module.render(runner, batch, {'duration_seconds': 20/3}, 1, clip)
            report = runner.read_json(runner.clip_path(batch, 1, clip)/'verification.json')
            self.assertEqual(report['video_frame_count'], 200)
            self.assertAlmostEqual(report['video_seconds'], 20/3)

    def test_render_excludes_a_tail_rejected_by_visual_interval_review(self):
        module = runner.storyboard_module()
        with tempfile.TemporaryDirectory() as directory:
            batch = Path(directory)
            scene = {'seconds': 20/3, 'visual_speed': 1.5, 'dialogue': 'A',
                     'opening_prompt': 'image', 'video_prompt': 'video'}
            clip = {'slug': 'interval-test', 'scenes': [scene]}
            sf = module.folder(runner, batch, 1, clip, 1)
            vf = module.voice_folder(runner, sf)
            vf.mkdir(parents=True)
            Image.new('RGB', (72, 128), 'purple').save(sf/'opening.png')
            (sf/'source.mp4').write_bytes(b'original ten-second source')
            (vf/'voice.mp3').write_bytes(b'voice')
            (vf/'dialogue.txt').write_text('A', encoding='utf-8')
            import hashlib
            runner.save_json(sf/'opening-review.json', {
                'result': 'accepted', 'sha256': hashlib.sha256((sf/'opening.png').read_bytes()).hexdigest()})
            runner.save_json(sf/'video-review.json', {
                'result': 'accepted_selected_interval', 'reviewed_interval_seconds': [0, 9],
                'source_sha256': hashlib.sha256((sf/'source.mp4').read_bytes()).hexdigest()})
            with patch.object(runner, 'duration', return_value=10), patch.object(runner, 'run_ff') as ff:
                with self.assertRaisesRegex(ValueError, 'accepted source interval'):
                    module.render(runner, batch, {'duration_seconds': 20/3,
                                  'quality': {'require_video_review': True}}, 1, clip)
                ff.assert_not_called()

    def test_narration_cleanup_keeps_speech_and_pause_boundary_guards(self):
        spec = importlib.util.spec_from_file_location('audio_timing', Path(__file__).with_name('audio_timing.py'))
        timing = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(timing)
        segments, removed = timing.speech_segments(8., [(0, .5), (1., 1.8), (3., 3.2), (7.7, 8.)])
        self.assertEqual(removed, [[1.12, 1.68]])
        self.assertEqual(segments, [[0., 1.12], [1.68, 8.]])
        self.assertAlmostEqual(sum(end-start for start, end in segments), 7.44)
        self.assertEqual(timing.silence_ranges('silence_start: 1.0\nsilence_end: 1.8 | duration: 0.8'), [(1., 1.8)])

    def test_exposure_lifts_dim_shell_without_turning_black_window_gray(self):
        quality = runner.storyboard_module().quality_module()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            source, corrected = path/'source.mp4', path/'corrected.mp4'
            runner.run_ff([runner.FF, '-y', '-f', 'lavfi', '-i',
                           'color=c=gray:s=72x128:r=24:d=1,drawbox=x=0:y=0:w=36:h=128:color=black:t=fill',
                           '-c:v', 'libx264', '-preset', 'ultrafast', str(source)])
            plan = {'enabled': True, 'preserve_blacks': True, 'black_floor': .12,
                    'black_transition': .32, 'ffmpeg_filter': 'eq=brightness=.07'}
            graph = quality.exposure_filters('0:v', 'out', plan, 'qa_')
            runner.run_ff([runner.FF, '-y', '-i', str(source), '-filter_complex',
                           ';'.join(graph), '-map', '[out]', '-c:v', 'libx264',
                           '-preset', 'ultrafast', str(corrected)])
            before = quality.sample_frame(runner.FF, source, .3, (72, 128))
            after = quality.sample_frame(runner.FF, corrected, .3, (72, 128))
            self.assertLess(abs(after.getpixel((12, 64))[0]-before.getpixel((12, 64))[0]), 4)
            self.assertGreater(after.getpixel((54, 64))[0]-before.getpixel((54, 64))[0], 12)

    def test_exposure_can_sample_the_end_of_a_full_ten_second_24fps_scene(self):
        quality = runner.storyboard_module().quality_module()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            opening, source = path/'opening.png', path/'source.mp4'
            Image.new('RGB', (72, 128), (128, 128, 128)).save(opening)
            runner.run_ff([runner.FF, '-y', '-f', 'lavfi', '-i',
                           'color=c=gray:s=72x128:r=24:d=10',
                           '-c:v', 'libx264', '-preset', 'ultrafast', str(source)])
            plan = quality.exposure_plan(runner.FF, source, opening,
                                        {'seconds': 20/3, 'visual_speed': 1.5},
                                        {'enabled': True})
            self.assertAlmostEqual(plan['points'][-1]['source_seconds'], 9.9)
            self.assertGreater(plan['end_to_opening_ratio'], .95)

    def test_marketing_hook_and_cta_are_part_of_actual_narration(self):
        module = runner.storyboard_module()
        clip = {'dialogue': '[upbeat] Hook. Benefit. Buy now.',
                'scenes': [{'seconds': 6, 'dialogue': '[upbeat] Hook. Benefit. Buy now.',
                            'opening_prompt': 'image', 'video_prompt': 'video'}],
                'marketing': {'hook': 'Hook.', 'hook_seconds': 3, 'cta': 'Buy now.',
                              'buyer_benefit': 'Benefit', 'reason_to_believe': 'Evidence'}}
        module.validate_scenes({'duration_seconds': 6}, clip)
        clip['marketing']['hook_seconds'] = 4
        with self.assertRaisesRegex(ValueError, 'first three seconds'):
            module.validate_scenes({'duration_seconds': 6}, clip)
        clip['marketing']['hook_seconds'] = 3
        clip['marketing']['cta'] = 'A CTA that was never spoken'
        with self.assertRaisesRegex(ValueError, 'purchase CTA'):
            module.validate_scenes({'duration_seconds': 6}, clip)

    def test_storyboard_renders_distinct_scenes_with_aligned_audio_and_captions(self):
        module = runner.storyboard_module()
        with tempfile.TemporaryDirectory() as directory:
            batch = Path(directory)
            scenes = [{'seconds': 2, 'visual_speed': 1.5, 'dialogue': 'A',
                       'audio_segments': [[0, .7], [.7, 1.5]],
                       'opening_prompt': 'image', 'video_prompt': 'video',
                       'on_screen': {'title': 'PIN ĐỎ?', 'subtitle': 'Hook', 'seconds': 1}},
                      {'seconds': 2, 'visual_speed': 1.5, 'dialogue': 'B',
                       'opening_prompt': 'image', 'video_prompt': 'video',
                       'on_screen': {'title': 'CHỌN PHIÊN BẢN'}}]
            clip = {'slug': 'storyboard-test', 'scenes': scenes, 'text_overlays': True}
            for number, color in enumerate(['red', 'blue'], 1):
                sf = module.folder(runner, batch, 1, clip, number)
                vf = module.voice_folder(runner, sf)
                vf.mkdir(parents=True)
                (vf/'dialogue.txt').write_text(scenes[number-1]['dialogue'], encoding='utf-8')
                image = sf/'opening.png'
                Image.new('RGB', (72, 128), color).save(image)
                import hashlib
                runner.save_json(sf/'opening-review.json', {'result': 'accepted', 'sha256': hashlib.sha256(image.read_bytes()).hexdigest()})
                runner.run_ff([runner.FF, '-y', '-f', 'lavfi', '-i', f'color=c={color}:s=72x128:r=30:d=10',
                               '-c:v', 'libx264', '-preset', 'ultrafast', str(sf/'source.mp4')])
                runner.run_ff([runner.FF, '-y', '-f', 'lavfi', '-i', f'sine=frequency={number*440}:duration=1.5',
                               '-c:a', 'libmp3lame', str(vf/'voice.mp3')])
            module.render(runner, batch, {'duration_seconds': 4}, 1, clip)
            target = runner.clip_path(batch, 1, clip)
            report = runner.read_json(target/'verification.json')
            self.assertEqual(report['final_seconds'], 4)
            self.assertEqual(report['independent_scenes'], 2)
            self.assertEqual([t['audio_tempo'] for t in report['scene_timings']], [1, 1])
            import subprocess
            for second, channel in [(0.5, 0), (2.5, 2)]:
                pixel = subprocess.run([runner.FF, '-v', 'error', '-ss', str(second),
                    '-i', str(target/'final.mp4'), '-frames:v', '1', '-vf',
                    'crop=2:2:360:640,scale=1:1', '-pix_fmt', 'rgb24', '-f', 'rawvideo', 'pipe:1'],
                    capture_output=True, check=True).stdout
                self.assertGreater(pixel[channel], 200)
            # User's no-text preference must override even an old on_screen
            # entry. No caption asset is needed and caption inputs are absent.
            clip['text_overlays'] = False
            for number in (1, 2):
                (module.folder(runner, batch, 1, clip, number)/'caption.png').unlink()
            with patch.object(module, 'caption_card', side_effect=AssertionError('caption generated')):
                module.render(runner, batch, {'duration_seconds': 4}, 1, clip)
            self.assertFalse(runner.read_json(target/'verification.json')['text_overlays'])
            pixel = subprocess.run([runner.FF, '-v', 'error', '-ss', '0.5',
                '-i', str(target/'final.mp4'), '-frames:v', '1', '-vf',
                'crop=2:2:60:1060,scale=1:1', '-pix_fmt', 'rgb24', '-f', 'rawvideo', 'pipe:1'],
                capture_output=True, check=True).stdout
            self.assertGreater(pixel[0], 200)
            scenes[0]['dialogue'] = 'Changed after TTS generation'
            with patch.object(runner, 'run_ff') as ff:
                with self.assertRaisesRegex(ValueError, 'audio script is stale'):
                    module.render(runner, batch, {'duration_seconds': 4}, 1, clip)
                ff.assert_not_called()

    def test_canonical_portrait_must_be_reviewed_before_scene_and_is_used_in_every_request(self):
        module = runner.storyboard_module()
        with self.assertRaisesRegex(ValueError, 'version 5 requires'):
            module.validate_scenes({'recipe_version': 5}, {'presentation_mode': 'presenter'})
        with tempfile.TemporaryDirectory() as directory:
            batch = Path(directory)
            config = {'references': ['product.png'], 'character': {'prompt': 'fictional adult'},
                      'quality': {'lock_exposure': True}}
            clip = {'slug': 'test', 'scenes': [{'opening_prompt': 'open', 'video_prompt': 'move'}]}
            Image.new('RGB', (20, 30), 'purple').save(batch/'product.png')
            portrait = module.character_path(batch, config)
            portrait.parent.mkdir()
            Image.new('RGB', (20, 30), 'green').save(portrait)
            with self.assertRaisesRegex(ValueError, 'canonical character'):
                module.opening_payload(runner, batch, config, 1, clip, 1)
            import hashlib
            runner.save_json(portrait.with_name('portrait-review.json'),
                             {'result': 'accepted', 'sha256': hashlib.sha256(portrait.read_bytes()).hexdigest()})
            payload = module.opening_payload(runner, batch, config, 1, clip, 1)
            self.assertEqual(payload['images'][1]['url'], runner.image_url(portrait))
            sf = module.folder(runner, batch, 1, clip, 1)
            sf.mkdir(parents=True)
            Image.new('RGB', (20, 30), 'blue').save(sf/'opening.png')
            video = module.video_payload(runner, batch, config, sf, clip['scenes'][0])
            self.assertEqual(video['images'][2]['url'], runner.image_url(portrait))
            self.assertIn('EXPOSURE CONTINUITY', video['prompt'])
            Image.new('RGB', (20, 30), 'red').save(portrait)
            with self.assertRaisesRegex(ValueError, 'canonical character'):
                module.opening_payload(runner, batch, config, 1, clip, 1)

    def test_gradual_dimming_is_measured_and_smooth_bounded_correction_restores_brightness(self):
        quality = runner.storyboard_module().quality_module()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            opening, source = path/'opening.png', path/'source.mp4'
            Image.new('RGB', (72, 128), (128, 128, 128)).save(opening)
            runner.run_ff([runner.FF, '-y', '-f', 'lavfi', '-i',
                           "color=c=gray:s=72x128:r=30:d=10,eq=brightness='-0.008*t':eval=frame",
                           '-c:v', 'libx264', '-preset', 'ultrafast', str(source)])
            plan = quality.exposure_plan(runner.FF, source, opening,
                                        {'seconds': 6, 'visual_speed': 1.5},
                                        {'enabled': True, 'max_brightness': .12})
            self.assertLess(plan['end_to_opening_ratio'], .91)
            self.assertGreater(plan['points'][-1]['brightness'], plan['points'][0]['brightness'])
            self.assertTrue(all(abs(point['brightness']) <= .12 for point in plan['points']))
            corrected = path/'corrected.mp4'
            runner.run_ff([runner.FF, '-y', '-i', str(source), '-vf',
                           'trim=duration=9,setpts=PTS/1.5,'+plan['ffmpeg_filter'],
                           '-c:v', 'libx264', '-preset', 'ultrafast', str(corrected)])
            self.assertGreater(quality.luma(quality.sample_frame(runner.FF, corrected, 5.9)), 122)
            self.assertLess(quality.luma(quality.sample_frame(runner.FF, corrected, 5.9)), 134)

    def test_image_upload_reencodes_mislabeled_webp_as_real_png(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)/'opening.png'
            Image.new('RGB', (20, 30), 'purple').save(source, format='WEBP')
            original = source.read_bytes()
            value = runner.image_url(source)
            self.assertTrue(value.startswith('data:image/png;base64,'))
            with Image.open(io.BytesIO(base64.b64decode(value.split(',', 1)[1]))) as decoded:
                self.assertEqual(decoded.format, 'PNG')
                self.assertEqual(decoded.size, (20, 30))
            self.assertEqual(source.read_bytes(), original)

    def test_storyboard_requires_enough_footage_and_exact_spoken_script(self):
        scenes = [{'seconds': 20/3, 'dialogue': str(n), 'opening_prompt': 'image', 'video_prompt': 'video'} for n in range(6)]
        clip = {'slug': 'test', 'background': 'shop', 'presenter': 'adult',
                'dialogue': '\n\n'.join(s['dialogue'] for s in scenes), 'scenes': scenes}
        config = {'duration_seconds': 40, 'visual_speed': 1.5, 'product_description': 'product', 'clips': [clip]}
        runner.validate(config)
        scenes[0]['visual_speed'] = 1.6
        with self.assertRaisesRegex(ValueError, 'more than ten seconds'):
            runner.validate(config)
        scenes[0]['visual_speed'] = 1.5
        clip['dialogue'] = 'unrelated cached narration'
        with self.assertRaisesRegex(ValueError, 'narration exactly'):
            runner.validate(config)

    def test_image_review_receipt_is_invalidated_when_image_changes(self):
        module = runner.storyboard_module()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            image = path/'opening.png'
            image.write_bytes(b'first')
            import hashlib
            runner.save_json(path/'opening-review.json', {'result': 'accepted', 'sha256': hashlib.sha256(image.read_bytes()).hexdigest(), 'notes': 'reviewed'})
            module.require_approval(runner, path)
            image.write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'Inspect opening'):
                module.require_approval(runner, path)

    def test_storyboard_video_uses_opening_then_original_product(self):
        module = runner.storyboard_module()
        with tempfile.TemporaryDirectory() as directory:
            batch = Path(directory)
            product, opening = batch/'crop.png', batch/'scene/opening.png'
            opening.parent.mkdir()
            Image.new('RGB', (20, 30), 'purple').save(product)
            Image.new('RGB', (20, 30), 'blue').save(opening)
            payload = module.video_payload(runner, batch, {'references': ['crop.png']}, opening.parent, {'video_prompt': 'preserve'})
            self.assertEqual(payload['images'][0]['url'], runner.image_url(opening))
            self.assertEqual(payload['images'][1]['url'], runner.image_url(product))
            self.assertNotIn('reference_image', payload)
            Image.new('RGB', (20, 30), 'green').save(batch/'presenter.png')
            payload = module.video_payload(runner, batch, {'references': ['crop.png']}, opening.parent,
                                            {'video_prompt': 'preserve', 'presenter_reference': 'presenter.png'})
            self.assertEqual(payload['images'][2]['url'], runner.image_url(batch/'presenter.png'))
            clip = {'slug': 'example', 'scenes': [{'revision': 2}]}
            self.assertEqual(module.folder(runner, batch, 1, clip, 1).name, 'scene-01-r02')

    def test_fast_edit_preserves_three_distinct_shots_in_twenty_seconds(self):
        with tempfile.TemporaryDirectory() as directory:
            batch=Path(directory)
            clip={'slug':'fast-test','scene_count':3,'visual_speed':1.5}
            folder=runner.clip_path(batch,1,clip)
            folder.mkdir()
            for number,color in enumerate(['red','lime','blue'],1):
                runner.run_ff([runner.FF,'-y','-f','lavfi','-i',f'color=c={color}:s=72x128:r=24:d=10','-c:v','libx264','-preset','ultrafast',str(folder/f'scene-{number:02}.mp4')])
            runner.run_ff([runner.FF,'-y','-f','lavfi','-i','sine=frequency=440:duration=18','-c:a','libmp3lame',str(folder/'voice.mp3')])
            runner.render(batch,{},1,clip)
            self.assertAlmostEqual(runner.duration(folder/'final.mp4'),20,places=1)
            for second,dominant_channel in [(2,0),(9,1),(16,2)]:
                import subprocess
                frame=subprocess.run([runner.FF,'-v','error','-ss',str(second),'-i',str(folder/'final.mp4'),'-frames:v','1','-vf','scale=1:1','-pix_fmt','rgb24','-f','rawvideo','pipe:1'],capture_output=True,check=True).stdout
                self.assertGreater(frame[dominant_channel],200)
                self.assertLess(max(value for i,value in enumerate(frame[:3]) if i!=dominant_channel),60)
            report=json.loads((folder/'verification.json').read_text(encoding='utf-8'))
            self.assertFalse(report['looped'])
            self.assertEqual(report['audio_tempo'],1.0)

    def test_uncertain_submission_does_not_repeat_post(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory)
            runner.save_json(folder/'scene-01-submission.json', {'intent_at':'interrupted'})
            with patch.object(runner,'muse_headers',return_value={}), patch.object(runner.requests,'post') as post:
                with self.assertRaisesRegex(RuntimeError,'uncertain'):
                    runner.task_media(folder,{},folder,folder/'scene-01.mp4','/v1/videos',{'prompt':'example'})
                post.assert_not_called()

    def test_resume_failed_task_does_not_submit_new_generation(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory)
            runner.save_json(folder/'scene-01-task.json', {'id':'task_existing'})
            with patch.object(runner,'muse_headers',return_value={}), patch.object(runner.requests,'post') as post, patch.object(runner.requests,'get') as get:
                get.return_value.json.return_value={'status':'failed','error':'quota exhausted'}
                with self.assertRaisesRegex(RuntimeError,'quota exhausted'):
                    runner.task_media(folder,{},folder,folder/'scene-01.mp4','/v1/videos',{'prompt':'example'})
                post.assert_not_called()
                self.assertTrue(get.call_args.args[0].endswith('/task_existing'))

    def test_short_footage_cannot_be_stretched_to_fill_target(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(runner,'duration',side_effect=[8.0,10.0]), patch.object(runner,'run_ff') as ff:
                with self.assertRaisesRegex(RuntimeError,'shorter than 10 seconds'):
                    runner.render(Path(directory),{},1,{'slug':'example'})
                ff.assert_not_called()

    def test_overlong_script_cannot_be_cut_to_fit(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(runner,'duration',side_effect=[10.0,10.0,40.0]), patch.object(runner,'run_ff') as ff:
                with self.assertRaisesRegex(RuntimeError,'Dialogue too long'):
                    runner.render(Path(directory),{},1,{'slug':'example'})
                ff.assert_not_called()

    def test_muse_cache_hit_skips_post_and_copies_media(self):
        with tempfile.TemporaryDirectory() as directory:
            batch=Path(directory)
            folder=batch/'clip'; folder.mkdir()
            payload={'prompt':'same prompt','duration':10}
            key=runner.request_key('/v1/videos',payload)
            cached,meta=runner.cache_paths(runner.MUSE_CACHE,key,'.mp4')
            cached.write_bytes(b'cached-video')
            runner.save_json(meta,{'cache_key':key})
            target=folder/'scene-01.mp4'
            with patch.object(runner,'muse_headers',return_value={}), patch.object(runner.requests,'post') as post:
                runner.task_media(batch,{},folder,target,'/v1/videos',payload)
                post.assert_not_called()
            self.assertEqual(target.read_bytes(),b'cached-video')

    def test_tts_cache_key_changes_when_dialogue_changes(self):
        first={'text':'A','model_id':'eleven_v3','language_code':'vi','voice_settings':{'stability':0.5},'voice_id':'pNInz6obpgDQGcFmaJgB','output_format':'mp3_44100_128'}
        second=dict(first); second['text']='B'
        self.assertNotEqual(runner.request_key('elevenlabs-tts',first),runner.request_key('elevenlabs-tts',second))

    def test_warm_cache_indexes_existing_voice_without_provider_call(self):
        with tempfile.TemporaryDirectory() as directory:
            batch=Path(directory)
            clip={'slug':'old','dialogue':'[happy] Hello','background':'x','presenter':'y'}
            folder=runner.clip_path(batch,1,clip); folder.mkdir(parents=True)
            (folder/'dialogue.txt').write_text(clip['dialogue'],encoding='utf-8')
            (folder/'voice.mp3').write_bytes(b'voice')
            config={'clips':[clip]}
            runner.warm_cache(batch,config)
            payload={'text':clip['dialogue'],'model_id':'eleven_v3','language_code':'vi','voice_settings':{'stability':0.5},'voice_id':'pNInz6obpgDQGcFmaJgB','output_format':'mp3_44100_128'}
            cached,_=runner.cache_paths(runner.TTS_CACHE,runner.request_key('elevenlabs-tts',payload),'.mp3')
            self.assertTrue(cached.exists())


if __name__=='__main__': unittest.main()
