import { Composition } from 'remotion';
import { Motion3D } from './Composition';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition id="Motion3D" component={Motion3D} width={1920} height={1080} fps={30} durationInFrames={1500}/>
    </>
  );
};
