"""Real FFmpeg timeline checks using synthetic footage; not an actual lip-sync evaluation."""
import copy
import importlib.util
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import talking_review as talking
from prepare_reference_review import build_configs

spec = importlib.util.spec_from_file_location('product_runner', Path(__file__).with_name('run.py'))
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class TalkingReviewTests(unittest.TestCase):
    def test_drafts_require_visible_synchronized_speech_and_accept_product_below_chin(self):
        for config in build_configs():
            runner.validate(config)
            seconds = sum(s['seconds'] for s in config['clips'][0]['scenes']
                          if s['speech_mode'] == 'lip_sync')
            self.assertEqual(seconds, 17)
        config = build_configs()[0]
        config['clips'][0]['scenes'][0]['video_prompt'] += ' No speaking or lip-sync.'
        with self.assertRaisesRegex(ValueError, 'conflicts'):
            runner.validate(config)
        config = build_configs()[0]
        config['clips'][0]['scenes'][0]['opening_prompt'] += ' Frame from below chin to desk.'
        with self.assertRaisesRegex(ValueError, 'conflicts'):
            runner.validate(config)

    def test_reference_profile_cannot_silently_become_offscreen_voiceover(self):
        config = build_configs()[0]
        for scene in config['clips'][0]['scenes']:
            scene['speech_mode'] = 'voiceover'
        with self.assertRaisesRegex(ValueError, 'at least 60%'):
            runner.validate(config)
        legacy = {'product_description': 'x', 'duration_seconds': 20, 'reference_style': talking.STYLE,
                  'clips': [{'slug': 'test', 'background': 'desk', 'presenter': 'adult', 'dialogue': 'x'}]}
        with self.assertRaisesRegex(ValueError, 'explicit scenes'):
            runner.validate(legacy)

    def test_final_speed_sync_survives_render_and_is_invalidated_by_audio_or_timing_changes(self):
        storyboard = runner.storyboard_module()
        with tempfile.TemporaryDirectory() as directory:
            batch = Path(directory)
            scene = {
                'seconds': 2, 'visual_speed': 1.5, 'speech_mode': 'lip_sync', 'face_visible': True,
                'dialogue': 'A', 'opening_prompt': 'Face visible', 'video_prompt': 'Presenter speaks',
            }
            clip = {'slug': 'synthetic-sync-test', 'scenes': [scene], 'dialogue': 'A',
                    'background': 'test', 'presenter': 'fictional adult'}
            config = {'duration_seconds': 2, 'product_description': 'synthetic test',
                      'quality': {'require_video_review': True}, 'clips': [clip]}
            runner.validate(config)
            path = storyboard.folder(runner, batch, 1, clip, 1)
            voice = storyboard.voice_folder(runner, path)
            voice.mkdir(parents=True)
            Image.new('RGB', (72, 128), 'purple').save(path/'opening.png')
            runner.save_json(path/'opening-review.json', {
                'result': 'accepted', 'sha256': talking.sha(path/'opening.png'),
                'notes': 'Synthetic geometry fixture only',
            })
            runner.run_ff([runner.FF, '-y', '-f', 'lavfi', '-i', 'color=c=purple:s=72x128:r=24:d=10',
                           '-c:v', 'libx264', '-preset', 'ultrafast', str(path/'source.mp4')])
            runner.run_ff([runner.FF, '-y', '-f', 'lavfi', '-i', 'sine=frequency=440:duration=2.1',
                           '-c:a', 'libmp3lame', str(voice/'voice.mp3')])
            (voice/'dialogue.txt').write_text('A', encoding='utf-8')
            runner.save_json(path/'video-review.json', {
                'result': 'accepted', 'source_sha256': talking.sha(path/'source.mp4'),
                'notes': 'Synthetic fixture, not a human mouth test',
            })
            talking.prepare(runner, storyboard, batch, config, 1, clip, 1)
            speech = path/'speech'
            original_identity = runner.read_json(speech/'input.json')
            self.assertGreater(original_identity['audio_tempo_before_sync'], 1.)
            talking.prepare(runner, storyboard, batch, config, 1, clip, 1)
            self.assertEqual(original_identity, runner.read_json(speech/'input.json'))
            with self.assertRaisesRegex(ValueError, 'actual synced'):
                storyboard.render(runner, batch, config, 1, clip)
            # Synthetic adapter fixture exercises I/O contracts, never claims to generate a mouth.
            shutil.copy2(speech/'video.mp4', speech/'synced.mp4')
            runner.save_json(speech/'sync-review.json', {
                'result': 'accepted', 'engine': 'synthetic unit-test fixture only',
                'notes': 'No person or speech exists in this test. Timeline plumbing only.',
                'audio_sha256': talking.sha(speech/'voice.wav'),
                'video_sha256': talking.sha(speech/'video.mp4'),
                'synced_sha256': talking.sha(speech/'synced.mp4'),
                'mouth_audio_reviewed': True, 'product_face_hands_reviewed': True,
                'reviewed_interval_seconds': [0, 2],
            })
            storyboard.render(runner, batch, config, 1, clip)
            report = runner.read_json(runner.clip_path(batch, 1, clip)/'verification.json')
            self.assertEqual(report['video_frame_count'], 60)
            self.assertEqual(report['scene_timings'][0]['visual_speed'], 1.)
            self.assertEqual(report['scene_timings'][0]['audio_tempo'], 1.)
            changed = copy.deepcopy(clip)
            changed['scenes'][0]['source_start'] = .5
            with self.assertRaisesRegex(ValueError, 'identity is stale'):
                talking.require_synced(runner, storyboard, batch, config, 1, changed, 1)
            with (speech/'voice.wav').open('ab') as file:
                file.write(b'changed audio')
            with self.assertRaisesRegex(ValueError, 'stale, rejected'):
                talking.require_synced(runner, storyboard, batch, config, 1, clip, 1)
            with self.assertRaisesRegex(ValueError, 'new scene revision'):
                talking.prepare(runner, storyboard, batch, config, 1, clip, 1)


if __name__ == '__main__':
    unittest.main()
