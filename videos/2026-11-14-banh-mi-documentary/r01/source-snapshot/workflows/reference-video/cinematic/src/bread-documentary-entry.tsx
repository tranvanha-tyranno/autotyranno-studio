import React from 'react';
import {Composition, registerRoot} from 'remotion';
import {BreadDocumentary, validateBreadPlan, type BreadDocumentaryProps} from './bread-documentary';

const empty: BreadDocumentaryProps = {plan: {fps: 30, durationFrames: 300, title: '', shots: [], audio: ''}};

const Root: React.FC = () => <Composition id="BreadDocumentary" component={BreadDocumentary} defaultProps={empty}
  width={1920} height={1080} fps={30} durationInFrames={300}
  calculateMetadata={({props}) => {
    validateBreadPlan(props.plan);
    const from = props.startFrame ?? 0;
    const length = props.frames ?? props.plan.durationFrames - from;
    if (!Number.isInteger(from) || from < 0 || !Number.isInteger(length) || length < 1 || from + length > props.plan.durationFrames) throw new Error('Bread proof range must be integer frames inside the plan timeline.');
    return {durationInFrames: length, fps: props.plan.fps};
  }}/>
;

registerRoot(Root);
