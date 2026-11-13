import { Composition } from 'remotion';
import { Motion3D } from './Composition';
import { WorkAI } from './longform/Composition';
import { VisualWorkAI } from './visualstory/Composition';
import {DirectionFilm} from './directions';
import type {DirectionTimeline} from './directions';
import longDirection from '../public/directions/long/data.json';
import hiddenDirection from '../public/directions/hidden/data.json';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition id="Motion3D" component={Motion3D} width={1920} height={1080} fps={30} durationInFrames={1500}/>
      <Composition id="WorkAI5min" component={WorkAI} width={1920} height={1080} fps={30} durationInFrames={9000}/>
      <Composition id="WorkAIVisual5min" component={VisualWorkAI} width={1920} height={1080} fps={30} durationInFrames={9000}/>
      <Composition id="LongDirection" component={DirectionFilm} width={1920} height={1080} fps={30} durationInFrames={longDirection.frames}
        defaultProps={{data:longDirection as unknown as DirectionTimeline}}
        calculateMetadata={({props})=>({durationInFrames:props.data.frames,fps:props.data.fps})}/>
      <Composition id="HiddenDirection" component={DirectionFilm} width={1920} height={1080} fps={30} durationInFrames={hiddenDirection.frames}
        defaultProps={{data:hiddenDirection as unknown as DirectionTimeline}}
        calculateMetadata={({props})=>({durationInFrames:props.data.frames,fps:props.data.fps})}/>
    </>
  );
};
