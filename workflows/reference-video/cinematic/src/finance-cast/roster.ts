/** Original, fictional adult characters. Roles describe story use, not financial expertise. */
export type Hair = 'side'|'bob'|'curly'|'bun'|'crop'|'quiff'|'long'|'afro'|'bald'|'pigtail'|'wave'|'braid'|'spiky'|'cap'|'beanie';
export type Outfit = 'tee'|'shirt'|'blazer'|'apron'|'cardigan'|'hoodie'|'vest'|'overall'|'tunic'|'sweater';
export type Accessory = 'none'|'round-glasses'|'square-glasses'|'earrings'|'scarf'|'headphones'|'watch'|'necklace'|'moustache'|'beard';
export type CastMember = {
  id:number; name:string; role:string; description:string;
  hair:Hair; outfit:Outfit; accessory:Accessory;
  skin:string; hairColor:string; top:string; pants:string; accent:string;
  build:'slim'|'regular'|'broad';
};
export const roster:CastMember[] = [
  {id:1,name:'Minh',role:'Người mới đi làm',description:'Nam trưởng thành, tóc rẽ lệch, áo thun xanh, dáng gọn',hair:'side',outfit:'tee',accessory:'none',skin:'#F6D2B3',hairColor:'#302D36',top:'#38A99C',pants:'#354658',accent:'#F0BF57',build:'slim'},
  {id:2,name:'Lan',role:'Người bạn hay hỏi',description:'Nữ trưởng thành, tóc xoăn tròn, áo hồng đất, khuyên tai',hair:'curly',outfit:'sweater',accessory:'earrings',skin:'#E8B48F',hairColor:'#44312D',top:'#DE887B',pants:'#3E4163',accent:'#F4CD68',build:'broad'},
  {id:3,name:'Chi',role:'Người lập kế hoạch',description:'Tóc bob, kính tròn, áo khoác vàng',hair:'bob',outfit:'cardigan',accessory:'round-glasses',skin:'#F4CCB2',hairColor:'#222D38',top:'#E9B850',pants:'#344F59',accent:'#F9F0DB',build:'regular'},
  {id:4,name:'Dũng',role:'Chủ quán nhỏ',description:'Tóc ngắn, tạp dề dài màu gạch',hair:'crop',outfit:'apron',accessory:'watch',skin:'#D9A582',hairColor:'#342A2A',top:'#CA7458',pants:'#2B4C51',accent:'#EBD6AF',build:'broad'},
  {id:5,name:'Hà',role:'Người mua có cân nhắc',description:'Tóc búi cao, sơ mi xanh, khuyên tai',hair:'bun',outfit:'shirt',accessory:'earrings',skin:'#F4C7AA',hairColor:'#49332B',top:'#689DAE',pants:'#324D5A',accent:'#F1BC51',build:'slim'},
  {id:6,name:'Huy',role:'Người mê công nghệ',description:'Tóc dựng, hoodie tím và tai nghe',hair:'spiky',outfit:'hoodie',accessory:'headphones',skin:'#E4B799',hairColor:'#343345',top:'#8E83B8',pants:'#3D4054',accent:'#DCD4F0',build:'regular'},
  {id:7,name:'Mai',role:'Người lo cho gia đình',description:'Tóc dài, áo cổ tròn và vòng cổ',hair:'long',outfit:'tunic',accessory:'necklace',skin:'#EFBE9D',hairColor:'#2D2A32',top:'#D48A5E',pants:'#38564D',accent:'#F1CE6E',build:'regular'},
  {id:8,name:'Hùng',role:'Người thích thử nghiệm',description:'Tóc hất cao, áo ghi lê sáng',hair:'quiff',outfit:'vest',accessory:'none',skin:'#F3D1B6',hairColor:'#6B4633',top:'#729888',pants:'#3A4D55',accent:'#EEE3C8',build:'slim'},
  {id:9,name:'Ngọc',role:'Người bán hàng',description:'Tóc tết, quần yếm xanh',hair:'braid',outfit:'overall',accessory:'earrings',skin:'#DDAA88',hairColor:'#332A2A',top:'#629AA3',pants:'#355D67',accent:'#F0CA78',build:'regular'},
  {id:10,name:'Phúc',role:'Người giữ sổ thu chi',description:'Đầu thưa tóc, kính vuông, blazer',hair:'bald',outfit:'blazer',accessory:'square-glasses',skin:'#E7B28F',hairColor:'#5C473E',top:'#526B74',pants:'#34434E',accent:'#DDA753',build:'broad'},
  {id:11,name:'Quỳnh',role:'Người làm tự do',description:'Tóc sóng ngắn, cardigan xanh rêu',hair:'wave',outfit:'cardigan',accessory:'scarf',skin:'#F0C7AC',hairColor:'#744B36',top:'#849C70',pants:'#474E62',accent:'#E1A372',build:'slim'},
  {id:12,name:'Sơn',role:'Người giao hàng',description:'Mũ lưỡi trai, áo khoác rộng',hair:'cap',outfit:'hoodie',accessory:'watch',skin:'#C99170',hairColor:'#302D2D',top:'#C89150',pants:'#3D4857',accent:'#596D77',build:'broad'},
  {id:13,name:'Thảo',role:'Người học nghề',description:'Hai đuôi tóc thấp, áo thun tím',hair:'pigtail',outfit:'tee',accessory:'none',skin:'#F4D1B8',hairColor:'#362E33',top:'#B294BF',pants:'#455A67',accent:'#F5D37C',build:'slim'},
  {id:14,name:'Tuấn',role:'Người trồng cây',description:'Tóc xoăn lớn, quần yếm màu đất',hair:'afro',outfit:'overall',accessory:'moustache',skin:'#C98D68',hairColor:'#352C2D',top:'#A78062',pants:'#516955',accent:'#E8C890',build:'broad'},
  {id:15,name:'Vy',role:'Người so sánh giá',description:'Mũ len, áo nỉ màu san hô',hair:'beanie',outfit:'sweater',accessory:'round-glasses',skin:'#E8BDA1',hairColor:'#51372E',top:'#D78276',pants:'#485066',accent:'#6F9D9C',build:'regular'},
  {id:16,name:'Yến',role:'Người đặt mục tiêu',description:'Tóc bob mái dài, blazer xanh ngọc',hair:'bob',outfit:'blazer',accessory:'earrings',skin:'#DFAF91',hairColor:'#5B3930',top:'#418F8E',pants:'#34485A',accent:'#EEE0C0',build:'slim'},
  {id:17,name:'Bảo',role:'Người sửa đồ',description:'Tóc ngắn bạc, áo sơ mi xắn tay',hair:'crop',outfit:'shirt',accessory:'moustache',skin:'#D3A082',hairColor:'#A8A19B',top:'#88A6A6',pants:'#56604E',accent:'#E8CA87',build:'broad'},
  {id:18,name:'Cẩm',role:'Người quản lý cửa hàng',description:'Búi tóc lớn, tạp dề xanh',hair:'bun',outfit:'apron',accessory:'square-glasses',skin:'#F3CEAF',hairColor:'#3A3135',top:'#5D9B8D',pants:'#484657',accent:'#EFCC83',build:'broad'},
  {id:19,name:'Đạt',role:'Người thích số liệu',description:'Tóc rẽ lệch, ghi lê tím và kính',hair:'side',outfit:'vest',accessory:'round-glasses',skin:'#E5B99A',hairColor:'#332B34',top:'#857D9F',pants:'#394451',accent:'#F2E0BB',build:'regular'},
  {id:20,name:'Giang',role:'Người sống xa nhà',description:'Tóc dài gợn, áo len cổ khăn',hair:'long',outfit:'sweater',accessory:'scarf',skin:'#E5B08C',hairColor:'#85563F',top:'#6B8BAF',pants:'#3E4C55',accent:'#E9B65C',build:'slim'},
  {id:21,name:'Khải',role:'Người đầu tư mới',description:'Tóc quiff, blazer đỏ gạch',hair:'quiff',outfit:'blazer',accessory:'watch',skin:'#EEC3A1',hairColor:'#2D2E32',top:'#B26E58',pants:'#3B4555',accent:'#EAD8AD',build:'regular'},
  {id:22,name:'Linh',role:'Người viết nội dung',description:'Tóc sóng, sơ mi vàng nhạt',hair:'wave',outfit:'shirt',accessory:'necklace',skin:'#F4D1B7',hairColor:'#433A35',top:'#DDBB67',pants:'#4F5C67',accent:'#709B95',build:'regular'},
  {id:23,name:'Nam',role:'Người nấu ăn',description:'Mũ mềm, tạp dề và bộ râu ngắn',hair:'beanie',outfit:'apron',accessory:'beard',skin:'#D29A76',hairColor:'#302C2B',top:'#9D8D76',pants:'#3B5457',accent:'#D9C092',build:'broad'},
  {id:24,name:'Oanh',role:'Người thích tối giản',description:'Tóc tết dài, áo cổ dài màu kem',hair:'braid',outfit:'tunic',accessory:'none',skin:'#E7B99A',hairColor:'#32343B',top:'#DDC9A9',pants:'#5B7770',accent:'#D38A63',build:'slim'},
  {id:25,name:'Phong',role:'Người bạn phản biện',description:'Tóc xoăn thấp, kính vuông, áo cam',hair:'curly',outfit:'tee',accessory:'square-glasses',skin:'#E5B090',hairColor:'#5A3C32',top:'#DDA05D',pants:'#465972',accent:'#D0D8C7',build:'regular'},
  {id:26,name:'Thư',role:'Người tự kinh doanh',description:'Tóc ngắn dựng, áo khoác mềm',hair:'spiky',outfit:'cardigan',accessory:'earrings',skin:'#CFA184',hairColor:'#34303B',top:'#AD839A',pants:'#3C575B',accent:'#E9CE96',build:'regular'},
  {id:27,name:'Trí',role:'Người nghỉ hưu',description:'Đầu thưa tóc bạc, cardigan đậm',hair:'bald',outfit:'cardigan',accessory:'moustache',skin:'#E3B696',hairColor:'#A9AAA6',top:'#648981',pants:'#595C6A',accent:'#E9CCA0',build:'slim'},
  {id:28,name:'Vân',role:'Người làm thủ công',description:'Tóc xù tròn, áo yếm tím nhạt',hair:'afro',outfit:'overall',accessory:'earrings',skin:'#BE8667',hairColor:'#2E2B30',top:'#A29AB8',pants:'#69617D',accent:'#E9C582',build:'regular'},
  {id:29,name:'Việt',role:'Người đi làm ca',description:'Mũ lưỡi trai ngược, hoodie xanh',hair:'cap',outfit:'hoodie',accessory:'none',skin:'#E0AF8D',hairColor:'#47332C',top:'#5C94AF',pants:'#3F485F',accent:'#DDC484',build:'slim'},
  {id:30,name:'Xuân',role:'Người hỗ trợ cộng đồng',description:'Hai búi tóc thấp, áo ghi lê ấm',hair:'pigtail',outfit:'vest',accessory:'necklace',skin:'#EAC1A7',hairColor:'#695047',top:'#C09C5C',pants:'#536774',accent:'#ECE0C4',build:'broad'},
];
export const getCharacter = (id:number):CastMember => roster.find((c)=>c.id===id) ?? roster[0];
