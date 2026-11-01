"""Check caption coverage, beat motion and samples from the encoded delivery."""
import argparse
import json
from pathlib import Path
import subprocess
from PIL import Image, ImageChops, ImageStat
import sql_paper as renderer


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    out=args.output
    scenes=json.loads((args.source/"timed-scenes.json").read_text(encoding="utf-8"))
    captions=json.loads((out/"alignment/captions.json").read_text(encoding="utf-8"))
    errors=[]
    for i,s in enumerate(scenes):
        cues=captions[i]["cues"]
        if " ".join(c["text"] for c in cues)!=s["dialogue"]:
            errors.append(f"Scene {i+1}: caption text differs from script")
        for cue in cues:
            if not 0<=cue["start"]<cue["end"]<=s["duration_seconds"]:
                errors.append(f"Scene {i+1}: invalid cue timing")
            page=renderer.frame(i,(cue["start"]+cue["end"])/2,s["duration_seconds"],cues)
            for x,y,w,h,text in page.bounds:
                if y>=1019 and y+h>1095:
                    errors.append(f"Scene {i+1}: caption outside panel: {text}")
    sheet=Image.new("RGB",(1080,2700),renderer.P["paper"])
    offset=0
    for i,s in enumerate(scenes):
        timestamp=offset+s["duration_seconds"]*.7
        path=out/"previews"/f"encoded-{i+1:02}.png"
        subprocess.run([renderer.FF,"-v","error","-y","-ss",str(timestamp),
            "-i",str(out/"SQL-paper-classroom-v2.mp4"),"-frames:v","1",str(path)],check=True)
        with Image.open(path) as im:sheet.paste(im.resize((540,675)),((i%2)*540,(i//2)*675))
        offset+=s["duration_seconds"]
    sheet.save(out/"final-contact-sheet.jpg",quality=95)
    motion_sheet=Image.new("RGB",(1080,900),renderer.P["paper"])
    motion=[]
    for k,(i,keyword,default) in enumerate([(3,"IN giúp",7),(4,"sắp xếp số phút",6),(5,"Sang trang hai",12)]):
        cues=captions[i]["cues"]
        at=renderer.beat(cues,keyword,default)
        offset=sum(s["duration_seconds"] for s in scenes[:i])
        images=[]
        for j,local in enumerate((max(0,at-.2),at+1.6)):
            path=out/"previews"/f"motion-{i+1:02}-{j}.png"
            subprocess.run([renderer.FF,"-v","error","-y","-ss",str(offset+local),
                "-i",str(out/"SQL-paper-classroom-v2.mp4"),"-frames:v","1",str(path)],check=True)
            with Image.open(path) as im:images.append(im.convert("RGB").copy())
            motion_sheet.paste(images[-1].resize((360,450)),(k*360,j*450))
        delta=ImageStat.Stat(ImageChops.difference(
            images[0].crop((0,350,1080,1100)),images[1].crop((0,350,1080,1100)))).mean
        motion.append({"scene":i+1,"beat_seconds":at,"mean_rgb_difference":delta})
        if max(delta)<.1:errors.append(f"Scene {i+1}: expected motion absent")
    motion_sheet.save(out/"encoded-motion-before-after.jpg",quality=95)
    levels=subprocess.run([renderer.FF,"-hide_banner","-i",str(out/"SQL-paper-classroom-v2.mp4"),
        "-vn","-af","volumedetect","-f","null","-"],capture_output=True,text=True)
    (out/"audio-levels.txt").write_text(levels.stderr,encoding="utf-8")
    report={"passed":not errors,"errors":errors,"script_preserved":True,
            "encoded_motion_samples":motion,"caption_checks":"all cues",
            "visual_contact_sheet":"final-contact-sheet.jpg"}
    (out/"delivery-check.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if errors:raise SystemExit(1)


if __name__=="__main__":
    main()
