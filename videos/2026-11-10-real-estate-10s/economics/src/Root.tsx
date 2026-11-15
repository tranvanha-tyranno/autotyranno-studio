import React from 'react';
import {AbsoluteFill, Audio, OffthreadVideo, Composition, Sequence, staticFile, useCurrentFrame} from 'remotion';
import captions from '../public/captions.json';
import envelope from '../public/waveform.json';

const Mic = () => <svg width="180" height="230" viewBox="0 0 180 230" fill="none" style={{filter:'drop-shadow(0 5px 18px #0008)'}}>
  <g transform="rotate(-12 90 95)">
    <rect x="55" y="12" width="70" height="122" rx="35" stroke="white" strokeWidth="7" />
    {[38,53,68,83,98].map(y=><path key={y} d={`M56 ${y}H78 M102 ${y}H124`} stroke="white" strokeWidth="5" strokeLinecap="round"/>)}
    <path d="M39 94V105C39 166 141 166 141 105V94" stroke="white" strokeWidth="7" strokeLinecap="round"/>
  </g>
  <path d="M90 155V202 M60 207H120" stroke="white" strokeWidth="8" strokeLinecap="round"/>
</svg>;

const Economics: React.FC = () => {
 const frame=useCurrentFrame();const t=frame/30;
 const cue=captions.find(c=>t>=c.start&&t<c.end);
 return <AbsoluteFill style={{background:'#101617',fontFamily:'Arial, sans-serif',color:'white'}}>
   <Sequence from={0} durationInFrames={114}>
     <OffthreadVideo muted src={staticFile('housing.mp4')} startFrom={24} style={{width:'100%',height:'100%',objectFit:'cover'}}/>
   </Sequence>
   <Sequence from={114} durationInFrames={186}>
     <OffthreadVideo muted src={staticFile('budget.mp4')} startFrom={100} style={{width:'100%',height:'100%',objectFit:'cover'}}/>
   </Sequence>
   <AbsoluteFill style={{background:'linear-gradient(180deg,rgba(0,8,12,.56),rgba(0,8,12,.51) 58%,rgba(0,8,12,.78))'}}/>
   <div style={{position:'absolute',top:151,left:0,right:0,textAlign:'center',fontSize:70,fontWeight:500,letterSpacing:1}}>GÓC NHÌN KINH TẾ</div>
   <div style={{position:'absolute',top:295,left:870}}><Mic/></div>
   <svg width="1030" height="150" viewBox="0 0 1030 150" style={{position:'absolute',left:445,top:488}}>
    <path d="M0 124H1030" stroke="white" strokeWidth="3" opacity=".8"/>
    {Array.from({length:206},(_,i)=>{
      const index=Math.round(t*100-190+i*.92);
      const amp=index>=0&&index<envelope.length?envelope[index]:0;
      const h=3+amp*96;
      return <rect key={i} x={i*5} y={124-h} width="3" height={h} fill="white" opacity=".95"/>;
    })}
   </svg>
   <div style={{position:'absolute',left:680,top:709,width:560,height:4,background:'#ffffff55'}}>
    <div style={{width:`${t*10}%`,height:4,background:'white'}}/>
    <div style={{position:'absolute',top:-7,left:560*t/10-9,width:18,height:18,borderRadius:20,background:'white'}}/>
   </div>
   <svg width="172" height="44" viewBox="0 0 172 44" style={{position:'absolute',left:874,top:742}} fill="white">
    <path d="M30 15L17 23L30 31ZM43 15L30 23L43 31Z"/>
    <circle cx="86" cy="23" r="17" fill="none" stroke="white" strokeWidth="2"/>
    <path d="M81 16V30M91 16V30" stroke="white" strokeWidth="4"/>
    <path d="M129 15L142 23L129 31ZM142 15L155 23L142 31Z"/>
   </svg>
   <div style={{position:'absolute',left:140,right:140,top:904,minHeight:65,textAlign:'center',fontSize:48,lineHeight:1.3,fontWeight:500,textShadow:'0px 2px 6px #000'}}>
    {cue?.words.map((w,i)=><React.Fragment key={i}><span style={{color:t>=w.start&&(i===cue.words.length-1||t<cue.words[i+1].start)?'#3edab4':'white'}}>{w.text}</span>{' '}</React.Fragment>)}
   </div>
   <Audio src={staticFile('voice.wav')}/>
 </AbsoluteFill>;
};
export const RemotionRoot: React.FC = () => <Composition id="RealEstate" component={Economics} durationInFrames={300} fps={30} width={1920} height={1080}/>;
