export type Product={id:string;name:string;description:string;features:string[];image_url:string};
export type Clip={id:string;title:string;dialogue:string;opening_prompt:string;shot_prompts:string[];scene_count:number;visual_speed:number;approved:boolean;scenes_ready:number;assets:Record<string,string>;verification?:Record<string,unknown>};
export type Job={id:string;project_id:string;clip_id:string|null;stage:string;status:string;message:string;created_at:string;started_at?:string;finished_at?:string};
export type Project={id:string;name:string;profile:string;products:Product[];clips:Clip[];jobs:Job[];pinned?:boolean;archived?:boolean};
export type Summary={id:string;name:string;profile:string;products:number;clips:number;ready:number;awaiting_review:number;thumbnail:string|null;pinned:boolean;archived:boolean;updated_at:string};
export type Connections={muse:{online:boolean};gemini:{configured:boolean};elevenlabs:{configured:boolean};storage:string};
export type Media={id:string;title:string;project_name:string;project_id?:string;url:string;poster_url:string;profile:string;size_bytes:number;created_at:string;favorite:boolean};
export type Overview={projects:number;archived:number;products:number;clips:number;videos:number;active_jobs:number;needs_review:number;failed_jobs:number;completed_jobs:number;activity:{date:string;jobs:number;videos:number}[];recent_jobs:Job[];recent_media:Media[]};
export type Plan={counts:Record<string,number>;new_provider_calls_upper_bound:number;notes:string;rows:{clip_id:string;calls:number;pending:number;existing_or_cached:number}[]};
export type Suggestion={text:string;field:string;scene:number;model:string;cache_hit:boolean};
export type Edit={dialogue:string;opening_prompt:string;shot_prompts:string[]};
export type Template={id:string;number:number;title:string;category:string;seconds:number;hands:number;requires:string[];text:string;summary:string};
export type Account={id:string;label:string;enabled:boolean;ok:boolean|null;use_count:number;last_used:number|null;expires_at:number|null;expires_estimated:boolean;essential_ok:boolean;cookie_count:number};
export type Pool={online:boolean;accounts:Account[];worker_count:number;note:string};
export const labels:Record<string,string>={images:"Tạo ảnh",voices:"Tạo thoại",videos:"Sinh video",render:"Ghép & kiểm tra",all:"Toàn quy trình",queued:"Trong hàng đợi",running:"Đang xử lý",completed:"Hoàn tất",failed:"Cần kiểm tra",needs_review:"Chờ duyệt ảnh",interrupted:"Bị gián đoạn",cancelled:"Đã hủy"};
export async function api<T>(url:string,options:RequestInit={}):Promise<T>{const response=await fetch("/api/studio"+url,{...options,headers:options.body instanceof FormData?options.headers:{"Content-Type":"application/json",...options.headers}});const data=await response.json().catch(()=>({detail:"Không kết nối được Studio. Kiểm tra server local."}));if(!response.ok)throw new Error(typeof data.detail==="string"?data.detail:JSON.stringify(data.detail));return data;}
export const body=(data:unknown={},method="POST")=>({method,body:JSON.stringify(data)});
export function date(value:string){return new Date(value).toLocaleString("vi-VN",{timeZone:"Asia/Saigon",hour:"2-digit",minute:"2-digit",day:"2-digit",month:"2-digit"});}
export function size(bytes:number){return `${(bytes/1024/1024).toFixed(1)} MB`;}
export function profileName(profile:string){return profile==="mica"?"Mica POV":"Product Review";}
