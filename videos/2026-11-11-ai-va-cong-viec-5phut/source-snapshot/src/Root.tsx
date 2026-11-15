import { Composition } from 'remotion';
import { Motion3D } from './Composition';
import { WorkAI } from './longform/Composition';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition id="Motion3D" component={Motion3D} width={1920} height={1080} fps={30} durationInFrames={1500}/>
      <Composition id="WorkAI5min" component={WorkAI} width={1920} height={1080} fps={30} durationInFrames={9000}/>
    </>
  );
};
