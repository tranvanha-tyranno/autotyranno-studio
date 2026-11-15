import React, {useEffect, useState} from 'react';
import {Audio, Video} from '@remotion/media';
import {AbsoluteFill, cancelRender, continueRender, delayRender, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {ChapterSignpost, EditorialPoint} from './Editorial';
import {MathOverlay} from './MathOverlay';
import {font, palette as P} from './theme';
import type {BreadDocumentaryProps, BreadPlan, BreadShot} from './types';
import './fonts.css';

export type {BreadDocumentaryProps, BreadPlan, BreadShot} from './types';

const LocalFonts: React.FC = () => {
  const [handle] = useState(() => delayRender('Loading local Vietnamese documentary fonts'));
  useEffect(() => {
    Promise.all([400, 600, 700].map(weight => document.fonts.load(`${weight} 32px "Bread Be Vietnam Pro"`, 'Tiếng Việt Ắ ầ ệ Ữ ỹ')))
      .then(() => document.fonts.ready).then(() => continueRender(handle)).catch(cancelRender);
  }, [handle]);
  return null;
};

export const validateBreadPlan = (plan: BreadPlan) => {
  if (plan.fps !== 30 || !Number.isInteger(plan.durationFrames) || plan.durationFrames < 1) throw new Error('Bread plan requires fps=30 and positive integer durationFrames.');
  let expected = 0;
  const seen = new Set<string>();
  for (const shot of plan.shots) {
    if (seen.has(shot.id)) throw new Error(`Duplicate bread shot: ${shot.id}`);
    seen.add(shot.id);
    if (!Number.isInteger(shot.from) || shot.from !== expected || !Number.isInteger(shot.duration) || shot.duration < 16) throw new Error(`Bread shot ${shot.id} has a gap/overlap or invalid frame duration. Expected from=${expected}.`);
    if (!shot.file || !Number.isFinite(shot.sourceStartSeconds) || shot.sourceStartSeconds < 0) throw new Error(`Bread shot ${shot.id} needs a local moving MP4 file and sourceStartSeconds >= 0.`);
    if (!shot.chapterId || !shot.chapterTitle) throw new Error(`Bread shot ${shot.id} needs an editorial chapter.`);
    if (shot.media === 'graphic' && !shot.kind) throw new Error(`Bread graphic ${shot.id} is missing its explanation kind.`);
    if (shot.cueFrames?.some((n, i, cues) => !Number.isInteger(n) || n < 0 || n >= shot.duration || (i > 0 && n <= cues[i - 1]))) throw new Error(`Bread shot ${shot.id} cueFrames must strictly increase inside the shot.`);
    expected += shot.duration;
  }
  if (plan.shots.length && expected !== plan.durationFrames) throw new Error(`Bread shots cover ${expected} frames, plan declares ${plan.durationFrames}.`);
};

const DocumentaryShot: React.FC<{shot: BreadShot; fps: number; firstInChapter: boolean; chapterIndex: number}> = ({shot, fps, firstInChapter, chapterIndex}) => {
  const frame = useCurrentFrame();
  const graphic = shot.media === 'graphic';
  const darkSide = shot.graphicSide === 'left' ? 'to right' : 'to left';
  return <AbsoluteFill style={{backgroundColor: P.ink, overflow: 'hidden'}}>
    <Video src={staticFile(shot.file)} trimBefore={Math.round(shot.sourceStartSeconds * fps)} muted
      objectFit="cover" style={{position: 'absolute', inset: 0, width: '100%', height: '100%',
        filter: `brightness(${shot.exposure ?? 1}) contrast(1.025) saturate(.94)`}}/>
    <AbsoluteFill style={{background: 'linear-gradient(180deg,rgba(65,36,10,.035),transparent 60%,rgba(17,12,7,.055))', pointerEvents: 'none'}}/>
    {(firstInChapter || shot.headline || shot.emphasis) && <AbsoluteFill style={{background: `linear-gradient(180deg,rgba(0,0,0,${firstInChapter && frame < 104 ? '.55' : '.12'}) 0%,transparent 33%,transparent 48%,rgba(0,0,0,${graphic ? '.3' : shot.headline || shot.emphasis ? '.7' : '.16'}) 100%)`}}/>}
    {graphic && <AbsoluteFill style={{background: `linear-gradient(${darkSide},rgba(10,10,8,.91) 0%,rgba(10,10,8,.77) 35%,rgba(10,10,8,.27) 63%,rgba(10,10,8,.02) 89%)`}}/>}
    {firstInChapter && <ChapterSignpost title={shot.chapterTitle} index={chapterIndex} duration={shot.duration}/>}
    {graphic ? <MathOverlay shot={shot}/> : <EditorialPoint shot={shot}/>}
  </AbsoluteFill>;
};

/** Footage cuts directly on the speech timeline. Only the explanatory overlays
 * fade over ~6 frames. We never fade both clips to black, loop footage, move a
 * photograph to masquerade as live action, or display automatic subtitles. */
export const BreadDocumentary: React.FC<BreadDocumentaryProps> = ({plan, startFrame = 0, frames}) => {
  validateBreadPlan(plan);
  const length = frames ?? plan.durationFrames - startFrame;
  const chapterIds = [...new Set(plan.shots.map(shot => shot.chapterId))];
  return <AbsoluteFill style={{background: P.ink, fontFamily: font, color: P.white, overflow: 'hidden', fontVariantNumeric: 'tabular-nums'}}>
    <LocalFonts/>
    {plan.shots.filter(shot => shot.from < startFrame + length && shot.from + shot.duration > startFrame).map(shot => {
      const index = plan.shots.findIndex(item => item.id === shot.id);
      const firstInChapter = index > 0 && plan.shots[index - 1].chapterId !== shot.chapterId;
      return <Sequence key={shot.id} name={`${shot.chapterId} / ${shot.id}`} from={shot.from - startFrame} durationInFrames={shot.duration} premountFor={30}>
        <DocumentaryShot shot={shot} fps={plan.fps} firstInChapter={firstInChapter} chapterIndex={chapterIds.indexOf(shot.chapterId)}/>
      </Sequence>;
    })}
    {plan.audio ? <Audio src={staticFile(plan.audio)} trimBefore={startFrame} durationInFrames={length}/> : null}
  </AbsoluteFill>;
};
