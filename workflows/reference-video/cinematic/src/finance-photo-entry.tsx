import React from 'react';
import {Composition, registerRoot} from 'remotion';
import {FinancePhotoClean, FinancePhotoComic, type FinancePhotoProps} from './finance-photo';

const empty: FinancePhotoProps = {plan: {fps: 30, durationFrames: 18000, segments: [], shots: [], captions: [], words: [], assets: {}, photoShots: []}};
const Root: React.FC = () => <>
  <Composition id="FinancePhotoComic" component={FinancePhotoComic} defaultProps={empty} width={1920} height={1080} fps={30} durationInFrames={18000} calculateMetadata={({props}) => ({durationInFrames: props.frames ?? props.plan.durationFrames, fps: props.plan.fps})}/>
  <Composition id="FinancePhotoClean" component={FinancePhotoClean} defaultProps={empty} width={1920} height={1080} fps={30} durationInFrames={18000} calculateMetadata={({props}) => ({durationInFrames: props.frames ?? props.plan.durationFrames, fps: props.plan.fps})}/>
</>;
registerRoot(Root);
