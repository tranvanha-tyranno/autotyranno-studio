import type {CSSProperties} from 'react';
import {AbsoluteFill, CanvasImage, Sequence, interpolate, spring, staticFile, useCurrentFrame} from 'remotion';
import {Audio, Video} from '@remotion/media';
import {Gallery3D} from './Gallery3D';
import type {DirectionImage, DirectionName, DirectionShot, DirectionTimeline} from './types';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const palette = {
  long: {paper: '#f1ebdf', ink: '#1c1b18', accent: '#ee5f3f', muted: '#69645a', dark: '#161716', font: 'Bahnschrift,Arial,sans-serif'},
  hidden: {paper: '#e8e7dd', ink: '#0c1c28', accent: '#86c7c0', muted: '#8ea2ad', dark: '#091620', font: 'Times New Roman,serif'},
};

const headingSize = (text = '') => text.length > 68 ? 59 : text.length > 44 ? 70 : 87;

const Photo: React.FC<{
  image: DirectionImage;
  duration: number;
  reverse?: boolean;
  style?: CSSProperties;
}> = ({image, duration, reverse = false, style}) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [0, Math.max(1, duration - 1)], [0, 1], clamp);
  const [x, y] = image.focus ?? [50, 50];
  const portrait = image.aspect !== undefined && image.aspect < 1.2;
  if (image.mediaType === 'video') {
    return <AbsoluteFill style={{overflow: 'hidden', background: '#111513', ...style}}>
      <Video src={staticFile(image.file)} muted trimBefore={image.trimBeforeFrames ?? 0} style={{width: '100%', height: '100%', objectFit: portrait ? 'contain' : 'cover', objectPosition: `${x}% ${y}%`}}/>
    </AbsoluteFill>;
  }
  return <AbsoluteFill style={{overflow: 'hidden', ...style}}>
    {portrait ? <CanvasImage src={staticFile(image.file)} style={{position: 'absolute', width: '100%', height: '100%', objectFit: 'cover', objectPosition: `${x}% ${y}%`, scale: 1.15, filter: 'blur(30px) brightness(.54) saturate(.7)'}}/> : null}
    <CanvasImage src={staticFile(image.file)} style={{position: 'absolute', width: '100%', height: '100%', objectFit: portrait ? 'contain' : 'cover', objectPosition: `${x}% ${y}%`, scale: portrait ? 1 + p * .01 : reverse ? 1.055 - p * .035 : 1.018 + p * .045, translate: portrait ? undefined : `${(reverse ? 1 : -1) * (p - .5) * 14}px 0`, filter: 'saturate(.94) contrast(1.015)'}}/>
  </AbsoluteFill>;
};

const Eyebrow: React.FC<{text?: string; color: string; style?: CSSProperties}> = ({text, color, style}) => text ? <div style={{fontFamily: 'Arial,sans-serif', fontSize: 23, lineHeight: 1.2, letterSpacing: 3.5, fontWeight: 700, textTransform: 'uppercase', color, ...style}}>{text}</div> : null;

const Headline: React.FC<{text?: string; direction: DirectionName; style?: CSSProperties}> = ({text, direction, style}) => {
  const frame = useCurrentFrame();
  const p = spring({frame: Math.max(0, frame - 3), fps: 30, config: {damping: direction === 'long' ? 24 : 30, stiffness: direction === 'long' ? 140 : 95}});
  const normalized = text?.normalize('NFC');
  if (!normalized) return null;
  return <div style={{fontFamily: palette[direction].font, fontSize: headingSize(normalized), fontWeight: direction === 'long' ? 700 : 400, lineHeight: 1.09, letterSpacing: direction === 'long' ? -1.8 : -1.4, overflowWrap: 'break-word', opacity: interpolate(frame, [1, 11], [0, 1], clamp), translate: `0 ${(1 - p) * (direction === 'long' ? 35 : 17)}px`, ...style}}>{normalized}</div>;
};

const Source: React.FC<{shot: DirectionShot; dark?: boolean; style?: CSSProperties}> = ({shot, dark = true, style}) => {
  const credit = shot.sourceNote ?? [...new Set(shot.images.map(i => i.credit).filter(Boolean))].join(' / ');
  return credit ? <div style={{position: 'absolute', left: 88, bottom: 145, right: 88, font: '18px Arial,sans-serif', letterSpacing: .5, lineHeight: 1.3, overflowWrap: 'anywhere', color: dark ? '#f6f4ec' : '#575e60', opacity: dark ? .77 : .8, textShadow: dark ? '0 1px 5px #000' : undefined, ...style}}>{credit}</div> : null;
};

const Full: React.FC<{shot: DirectionShot; direction: DirectionName; duration: number}> = ({shot, direction, duration}) => {
  const frame = useCurrentFrame();
  const p = palette[direction];
  const hasType = Boolean(shot.headline || shot.body);
  return <AbsoluteFill>
    <Photo image={shot.images[0]} duration={duration}/>
    <AbsoluteFill style={{background: hasType ? 'linear-gradient(0deg,rgba(3,10,15,.93),rgba(3,10,15,.68) 22%,transparent 63%)' : 'linear-gradient(0deg,rgba(3,10,15,.73),transparent 25%)'}}/>
    <Eyebrow text={shot.eyebrow} color={p.paper} style={{position: 'absolute', left: 88, top: 72, paddingLeft: 18, borderLeft: `4px solid ${p.accent}`, textShadow: '0 2px 8px #000', opacity: interpolate(frame, [0, 8, Math.max(9, duration - 20), Math.max(10, duration - 8)], [0, 1, 1, 0], clamp)}}/>
    {hasType ? <div style={{position: 'absolute', left: 88, bottom: 235, width: direction === 'long' ? 1450 : 1390, color: p.paper}}>
      <div style={{width: interpolate(frame, [0, 24], [0, 80], clamp), height: 4, background: p.accent, marginBottom: 23}}/>
      <Headline text={shot.headline} direction={direction}/>
      {shot.body ? <div style={{font: '29px Arial,sans-serif', maxWidth: 1360, lineHeight: 1.45, marginTop: 18, color: '#e1e4df'}}>{shot.body}</div> : null}
    </div> : null}
    <Source shot={shot}/>
  </AbsoluteFill>;
};

const Disclaimer: React.FC<{shot: DirectionShot; direction: DirectionName; duration: number}> = ({shot, direction, duration}) => {
  const p = palette[direction];
  const long = direction === 'long';
  return <AbsoluteFill style={{background: long ? p.paper : p.dark, color: long ? p.ink : p.paper}}>
    <div style={{position: 'absolute', left: long ? 1085 : 1050, top: 0, right: 0, bottom: 0, overflow: 'hidden'}}>
      <Photo image={shot.images[0]} duration={duration} reverse/>
      <AbsoluteFill style={{background: long ? 'linear-gradient(90deg,#f1ebdf,rgba(241,235,223,.03) 28%)' : 'linear-gradient(90deg,#091620,rgba(9,22,32,.05) 40%)'}}/>
    </div>
    <div style={{position: 'absolute', left: 100, top: 150, width: 975}}>
      <Eyebrow text={shot.eyebrow ?? 'LƯU Ý TRƯỚC KHI BẮT ĐẦU'} color={long ? p.muted : p.accent}/>
      <div style={{width: 80, height: 5, background: p.accent, margin: '34px 0 35px'}}/>
      <Headline text={shot.headline ?? 'Một góc nhìn để tham khảo.'} direction={direction} style={{fontSize: 72, maxWidth: 940}}/>
      {shot.body ? <div style={{font: '34px Arial,sans-serif', lineHeight: 1.5, marginTop: 32, maxWidth: 900, color: long ? '#56534e' : '#c1cdd2'}}>{shot.body}</div> : null}
    </div>
    <Source shot={shot} dark={!long} style={{left: 100, maxWidth: 960}}/>
  </AbsoluteFill>;
};

const Diptych: React.FC<{shot: DirectionShot; direction: DirectionName; duration: number}> = ({shot, direction, duration}) => {
  const p = palette[direction];
  const long = direction === 'long';
  const split = long ? 1110 : 960;
  return <AbsoluteFill style={{background: p.dark}}>
    <Photo image={shot.images[0]} duration={duration} style={{width: split - 4}}/>
    <Photo image={shot.images[1] ?? shot.images[0]} duration={duration} reverse style={{left: split + 4, width: 1920 - split - 4}}/>
    <div style={{position: 'absolute', left: split - 4, width: 8, top: 0, bottom: 0, background: long ? p.paper : p.dark}}/>
    <AbsoluteFill style={{background: 'linear-gradient(0deg,rgba(3,10,15,.91),rgba(3,10,15,.40) 24%,transparent 65%)'}}/>
    {shot.eyebrow ? <Eyebrow text={shot.eyebrow} color={p.paper} style={{position: 'absolute', left: 88, top: 72, background: long ? p.ink : p.dark, padding: '15px 22px', borderLeft: `4px solid ${p.accent}`}}/> : null}
    <div style={{position: 'absolute', left: 88, bottom: 238, maxWidth: 1550, color: p.paper}}>
      <Headline text={shot.headline} direction={direction} style={{fontSize: headingSize(shot.headline) - 3}}/>
      {shot.body ? <div style={{font: '29px Arial,sans-serif', lineHeight: 1.4, marginTop: 16, maxWidth: 1400}}>{shot.body}</div> : null}
    </div>
    <Source shot={shot}/>
  </AbsoluteFill>;
};

const Gallery: React.FC<{shot: DirectionShot; direction: DirectionName; duration: number}> = ({shot, direction, duration}) => {
  const p = palette[direction];
  const long = direction === 'long';
  return <AbsoluteFill style={{background: long ? 'radial-gradient(ellipse at 50% 40%,#fcf8ee,#e1dbce)' : 'radial-gradient(ellipse at 50% 44%,#20394a,#091620 76%)'}}>
    <Gallery3D images={shot.images} direction={direction} duration={duration}/>
    <div style={{position: 'absolute', left: 88, right: 88, top: 60, display: 'flex', alignItems: 'center', gap: 25, color: long ? p.ink : p.paper}}>
      <Eyebrow text={shot.eyebrow} color={long ? p.muted : p.accent} style={{fontSize: 20, maxWidth: 380}}/>
      {shot.eyebrow ? <div style={{width: 1, height: 28, background: long ? '#bbb4a6' : '#3d5969'}}/> : null}
      <Headline text={shot.headline} direction={direction} style={{fontSize: 43, maxWidth: 1340, lineHeight: 1.15}}/>
    </div>
    {shot.body ? <div style={{position: 'absolute', left: 88, right: 88, bottom: 195, font: '29px Arial,sans-serif', lineHeight: 1.4, textAlign: 'center', color: long ? p.ink : '#d6e1e2'}}>{shot.body}</div> : null}
    <Source shot={shot} dark={!long} style={{fontSize: 17}}/>
  </AbsoluteFill>;
};

const Evidence: React.FC<{shot: DirectionShot; direction: DirectionName; duration: number}> = ({shot, direction, duration}) => {
  const p = palette[direction];
  const long = direction === 'long';
  return <AbsoluteFill style={{background: long ? p.paper : p.dark, color: long ? p.ink : p.paper}}>
    <div style={{position: 'absolute', left: 0, top: 0, width: 1130, bottom: 0, overflow: 'hidden'}}>
      <Photo image={shot.images[0]} duration={duration}/>
      <AbsoluteFill style={{background: 'linear-gradient(0deg,rgba(3,10,15,.82),transparent 30%)'}}/>
      <Source shot={shot} style={{left: 65, right: 55, bottom: 150, fontSize: 17}}/>
    </div>
    <div style={{position: 'absolute', left: 1194, right: 75, top: 150}}>
      <Eyebrow text={shot.eyebrow} color={long ? p.muted : p.accent} style={{fontSize: 21, lineHeight: 1.4}}/>
      <div style={{width: 66, height: 4, background: p.accent, margin: '30px 0'}}/>
      <Headline text={shot.headline} direction={direction} style={{fontSize: 65, lineHeight: 1.14}}/>
      {shot.body ? <div style={{font: '30px Arial,sans-serif', lineHeight: 1.45, marginTop: 26, color: long ? '#5f5c54' : '#bbcad0'}}>{shot.body}</div> : null}
    </div>
  </AbsoluteFill>;
};

const Closing: React.FC<{shot: DirectionShot; direction: DirectionName; duration: number}> = ({shot, direction, duration}) => {
  const frame = useCurrentFrame();
  const p = palette[direction];
  const long = direction === 'long';
  return <AbsoluteFill style={{background: p.dark}}>
    <Photo image={shot.images[0]} duration={duration} reverse/>
    <AbsoluteFill style={{background: long ? 'linear-gradient(90deg,rgba(15,18,17,.94),rgba(15,18,17,.73) 46%,rgba(15,18,17,.12))' : 'linear-gradient(90deg,rgba(8,20,30,.96),rgba(8,20,30,.76) 55%,rgba(8,20,30,.25))'}}/>
    <div style={{position: 'absolute', left: 100, top: 198, width: 1220, color: p.paper}}>
      <Eyebrow text={shot.eyebrow ?? 'THỬ MỘT BƯỚC TIẾP THEO'} color={p.accent}/>
      <Headline text={shot.headline} direction={direction} style={{marginTop: 35, fontSize: 89}}/>
      {shot.body ? <div style={{font: '33px Arial,sans-serif', lineHeight: 1.45, marginTop: 29, maxWidth: 1070, color: '#d5dedc'}}>{shot.body}</div> : null}
      <div style={{marginTop: 37, width: interpolate(frame, [10, 38], [0, 94], clamp), height: 5, background: p.accent}}/>
    </div>
    <Source shot={shot}/>
  </AbsoluteFill>;
};

const Graphic: React.FC<{shot: DirectionShot; direction: DirectionName}> = ({shot, direction}) => <AbsoluteFill style={{background: palette[direction].paper}}>
  <CanvasImage src={staticFile(shot.images[0].file)} style={{width: '100%', height: '100%', objectFit: 'contain'}}/>
</AbsoluteFill>;

const Scene: React.FC<{shot: DirectionShot; direction: DirectionName; first: boolean}> = ({shot, direction, first}) => {
  const frame = useCurrentFrame();
  const duration = shot.end - shot.start;
  if (!shot.images.length) throw new Error(`Direction shot at ${shot.start} needs a real image.`);
  const content = shot.phase === 'disclaimer' ? <Disclaimer shot={shot} direction={direction} duration={duration}/> : shot.layout === 'graphic' ? <Graphic shot={shot} direction={direction}/> : shot.layout === 'gallery3d' ? <Gallery shot={shot} direction={direction} duration={duration}/> : shot.layout === 'diptych' ? <Diptych shot={shot} direction={direction} duration={duration}/> : shot.layout === 'evidence' ? <Evidence shot={shot} direction={direction} duration={duration}/> : shot.layout === 'closing' ? <Closing shot={shot} direction={direction} duration={duration}/> : <Full shot={shot} direction={direction} duration={duration}/>;
  return <AbsoluteFill style={{opacity: first ? 1 : interpolate(frame, [0, direction === 'long' ? 4 : 7], [0, 1], clamp)}}>{content}</AbsoluteFill>;
};

/** Both art directions share exact-take audio/timing while retaining distinct art direction. */
export const DirectionFilm: React.FC<{data: DirectionTimeline}> = ({data}) => {
  const frame = useCurrentFrame();
  const time = frame / data.fps;
  // Keep the last exact-take caption through the end card's tail. It must not
  // vanish or fade while the final spoken word is still being pronounced.
  const caption = data.captions.find((c, index) => time >= c.start && time < (index === data.captions.length - 1 ? Math.max(c.end, data.frames / data.fps) : c.end));
  return <AbsoluteFill style={{background: palette[data.direction].dark, overflow: 'hidden'}}>
    {data.shots.map((shot, index) => <Sequence key={`${index}-${shot.start}`} from={shot.start} durationInFrames={Math.min(shot.end - shot.start + 7, data.frames - shot.start)} name={`${shot.phase}: ${shot.headline ?? shot.eyebrow ?? shot.layout}`}>
      <Scene shot={shot} direction={data.direction} first={index === 0}/>
    </Sequence>)}
    {caption ? <div style={{position: 'absolute', left: 185, right: 185, bottom: 51, display: 'flex', justifyContent: 'center'}}>
      <div style={{padding: '10px 21px 12px', background: 'rgba(5,12,18,.83)', color: '#f6f5ef', font: '35px Arial,sans-serif', fontWeight: 400, textAlign: 'center', lineHeight: 1.25, maxWidth: 1530, borderRadius: data.direction === 'long' ? 2 : 7}}>{caption.text}</div>
    </div> : null}
    {data.audio ? <Audio src={staticFile(data.audio)}/> : null}
  </AbsoluteFill>;
};
