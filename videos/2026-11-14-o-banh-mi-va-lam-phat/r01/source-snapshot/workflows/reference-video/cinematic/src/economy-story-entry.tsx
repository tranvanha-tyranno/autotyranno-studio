import React from 'react';
import {Composition, registerRoot} from 'remotion';
import {EconomyStory, type EconomyStoryProps} from './economy-story';

const empty: EconomyStoryProps = {plan: {fps: 30, durationFrames: 18000, title: '', segments: [], captions: [], assets: {}}};
const Root: React.FC = () => <Composition id="EconomyStory" component={EconomyStory} defaultProps={empty} width={1920} height={1080} fps={30} durationInFrames={18000} calculateMetadata={({props}) => ({durationInFrames: props.frames ?? props.plan.durationFrames, fps: props.plan.fps})}/>;
registerRoot(Root);
