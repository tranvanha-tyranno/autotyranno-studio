import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('mica',Path(__file__).with_name('compile.py'))
mica=importlib.util.module_from_spec(spec);spec.loader.exec_module(mica)


class CompileTests(unittest.TestCase):
    def product(self,id,name):
        return {'id':id,'name':name,'reference_image':id+'.png','features':['Tính năng được cấp '+id]}

    def test_order_and_no_cross_product_claims(self):
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/'pack'
            result=mica.compile_pack({'products':[self.product('first','Một'),self.product('second','Hai')],'selected_video_prompts':[]},output)
            self.assertEqual(result['image_count'],6)
            self.assertEqual([(j['product_id'],j['scene']) for j in result['image_order']],[('first','mall'),('first','appliance-store'),('first','factory'),('second','mall'),('second','appliance-store'),('second','factory')])
            self.assertEqual((output/'001-first/01-mall/label.txt').read_text(encoding='utf-8'),'Một\nTính năng được cấp first')
            self.assertNotIn('Tính năng được cấp second',(output/'001-first/01-mall/image-prompt.txt').read_text(encoding='utf-8'))

    def test_capabilities_filter_jobs_and_hand_counts(self):
        with tempfile.TemporaryDirectory() as directory:
            output=Path(directory)/'pack'
            result=mica.compile_pack({'products':[self.product('one','Một')],'selected_video_prompts':[11,18,20],'capabilities':{'mall':['doorway']}},output)
            self.assertEqual(result['selected_video_count'],7)
            self.assertEqual(len(result['skipped']),2)
            self.assertTrue(all(j['max_hands']==2 for j in result['video_jobs'] if j['prompt_id'] in [18,20]))
            self.assertNotIn('Đúng MỘT tay', (output/'001-one/01-mall/video-18.txt').read_text(encoding='utf-8'))
            self.assertEqual(result['provider_calls_made'],0)

    def test_no_overwrite_and_invalid_names(self):
        with tempfile.TemporaryDirectory() as directory:
            config={'products':[self.product('one','Một')]}
            with self.assertRaises(ValueError):mica.compile_pack(config,Path(directory))
            config['products'][0]['id']='..'
            with self.assertRaises(ValueError):mica.validate_config(config)

    def test_all_ten_actions_exported(self):
        self.assertEqual([a['id'] for a in mica.ACTIONS],list(range(11,21)))
        self.assertTrue(all('6 giây' in mica.video_prompt(a) for a in mica.ACTIONS))


if __name__=='__main__':unittest.main()
