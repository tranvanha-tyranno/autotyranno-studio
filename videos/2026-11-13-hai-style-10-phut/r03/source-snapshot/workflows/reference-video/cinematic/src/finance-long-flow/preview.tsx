/** Local visual fixture for inspecting every mechanism before a full render. */
import React from 'react';
import {Composition, registerRoot} from 'remotion';
import {FlowLongFilm, LongPlan} from './index';
const kinds=['hook','disclaimer','budget_before','budget_after','daily','dinner','essentials','audit','recurring','annual','calendar','buffer','choice','automate','review','cta'];
const names=['Lương tăng, khoản dư đứng yên','Trước khi áp dụng','Ngân sách ban đầu','Sau khi tăng lương','Từng ngày cộng lại','Thêm một bữa ăn','Tính khoản thiết yếu trước','Chia lại giao dịch','Khoản chi lặp lại','Đến kỳ không còn bất ngờ','Nhìn đúng ngày đến hạn','Một lớp đệm cho bất ngờ','So cả chi phí sau mua','Tự động nhưng vẫn kiểm tra','Đối chiếu cuối kỳ','Một thử nghiệm trong 30 ngày'];
const Sheet:React.FC=()=> <div style={{width:3840,height:2160,background:'#ddd'}}>{kinds.map((kind,i)=>{
 const plan:LongPlan={fps:30,durationFrames:360,segments:[{id:kind,kind,from:-270,duration:360,text:'Tình huống minh họa với các khoản thiết yếu và số tiền đến hạn.',headline:names[i],cueFrame:80,chapterTitle:'KIỂM HÌNH • DỮ LIỆU MINH HỌA'}],captions:[]};
 return <div key={kind} style={{position:'absolute',left:i%4*960,top:Math.floor(i/4)*540,width:960,height:540,overflow:'hidden'}}><div style={{position:'absolute',width:1920,height:1080,transform:'scale(.5)',transformOrigin:'0 0'}}><FlowLongFilm plan={plan}/></div></div>;
})}</div>;
registerRoot(()=> <Composition id="FlowMechanisms" component={Sheet} durationInFrames={1} fps={30} width={3840} height={2160}/>);
