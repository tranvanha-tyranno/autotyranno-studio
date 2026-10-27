"""Checks for duplicate billing prevention and preserving full-speed footage."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import json
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('product_video_runner', Path(__file__).with_name('run.py'))
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class WorkflowTests(unittest.TestCase):
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
