import copy,json,unittest
from pathlib import Path
import business

ROOT=Path(__file__).resolve().parents[2]
class BusinessIntegrityTests(unittest.TestCase):
    def content(self):return business.load(ROOT/'videos/2026-11-13-quan-dong-khach-het-tien/content.json')
    def test_fictional_math(self):
        checks=business.validate(self.content())['exampleChecks']
        self.assertEqual(checks['monthlyDiscountUnitsCeil'],3429)
        self.assertEqual(checks['preserve60MillionUnitsCeil'],4286)
        self.assertEqual(checks['cashShortfall'],-5000000)
    def test_changed_economics_cannot_reuse_old_graphics(self):
        content=self.content();content['example']['price']=34000
        with self.assertRaises(ValueError):business.validate(content)
    def test_forbidden_brand_in_spoken_or_visual_text(self):
        for field in ['text','headline']:
            c=self.content();c['chapters'][0]['beats'][0][field]+=' TYRANNO'
            c['chapters'][0]['text']=' '.join(b['text'] for b in c['chapters'][0]['beats'])
            with self.assertRaisesRegex(ValueError,'branding'):business.validate(c)
    def data(self):
        return {'fps':30,'shots':[{'id':'a','start':0,'end':60,'layout':'b-photo','design':{},'images':[{'file':'business/clip.mp4','mediaType':'video','trimBeforeFrames':0,'availableFrames':120}]},
            {'id':'b','start':60,'end':120,'layout':'b-photo','design':{},'images':[{'file':'business/clip.mp4','mediaType':'video','trimBeforeFrames':60,'availableFrames':120}]}]}
    def test_nonoverlapping_normal_speed_intervals(self):self.assertEqual(business.validate_media_intervals(self.data())['movingMediaSeconds'],4)
    def test_reused_interval_rejected(self):
        d=self.data();d['shots'][1]['images'][0]['trimBeforeFrames']=30
        with self.assertRaisesRegex(ValueError,'Repeated'):business.validate_media_intervals(d)
    def test_short_background_video_also_rejected(self):
        d=self.data();d['shots'][0]['layout']='b-coffee';d['shots'][0]['images'][0]['availableFrames']=59
        with self.assertRaisesRegex(ValueError,'freeze'):business.validate_media_intervals(d)
    def test_alias_paths_do_not_hide_repeated_source(self):
        d=self.data()
        for i,s in enumerate(d['shots']):
            s['images'][0].update({'file':f'business/alias-{i}.mp4','sourceHash':'same-source','trimBeforeFrames':0})
        with self.assertRaisesRegex(ValueError,'Repeated'):business.validate_media_intervals(d)

if __name__=='__main__':unittest.main()
