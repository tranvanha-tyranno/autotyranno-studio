import {Composition,registerRoot} from 'remotion';
import {CastSheet,CastMotion} from './CastSheet';
const CastPreview=()=> <>
 <Composition id="FinanceCastSheet" component={CastSheet} width={1920} height={1080} fps={30} durationInFrames={1}/>
 <Composition id="FinanceCastMotion" component={CastMotion} width={1920} height={1080} fps={30} durationInFrames={360}/>
</>;
registerRoot(CastPreview);
