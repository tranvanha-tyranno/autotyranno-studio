"""Retain the exact reviewed take; upgrade the pilot's local imagery and motion."""
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / 'production-v4.json').read_text(encoding='utf-8'))
candidates = json.loads((ROOT / 'source-vietnam.json').read_text(encoding='utf-8'))
manifest['id'] = 'di-sieu-thi-vietnam-motion-r05'
manifest['visualPolicy'] = {'preferredCountry': 'VN', 'requireLocationEvidence': True,
                            'explicitDisclaimer': True}
manifest['renderOptions'] = {'memoryProfile': 'bounded'}
for row in candidates:
    note = row['inspection']
    manifest['assets'].append({
        'id': row['id'], 'file': row['file'], 'sha256': row['sha256'],
        'source': {'url': row['page'], 'creator': row['creator'], 'license': row['license'],
                   'licenseURL': row['licenseURL'].replace('http://creativecommons.org/', 'https://creativecommons.org/'), 'kind': 'stock'},
        'location': row['location'],
        'observed': {'subject': note['observedSubjectAction'],
                     'action': note['observedSubjectAction'],
                     'objects': note['supports'], 'limits': note['doesNotEstablish']},
        'inspection': {'status': 'inspected', 'reviewer': 'vietnam_assets agent + Codex root',
                       'sha256': row['sha256'],
                       'observations': note['observedSubjectAction'] + ' ' + note['doesNotEstablish']
                       + ' Root opened the three actual contact sheets. Individual rendered crops still require QA.'},
        'focus': row['recommendedFocus'], 'fit': row['recommendedFit']})

assets = {a['id']: a for a in manifest['assets']}
shots = {s['id']: s for section in manifest['sections'] for s in section['shots']}

def change(shot_id, images, *, layout=None, motion=None, headline=None, eyebrow=None,
           body=None, view, role='context'):
    shot = shots[shot_id]
    shot['images'] = images
    if layout: shot['layout'] = layout
    if motion: shot['motion'] = motion
    if headline is not None: shot['headline'] = headline
    if eyebrow is not None: shot['eyebrow'] = eyebrow
    if body is not None: shot['body'] = body
    shot['needToSee'] = view
    shot['supports'] = view
    shot['mediaRole'] = role
    limits = ('Illustrative context and/or original 3D mechanism, not proof of a photographed person\'s intent, '
              'overspending, waste or causal response. Vietnam photos are archival source-documented locations; '
              'visible prices are not current offers. The arithmetic is explicitly hypothetical.')
    shot['limits'] = limits
    shot['review'] = {'status': 'inspected', 'reviewer': 'Codex root',
                     'observations': view + ' ' + limits + ' Source pixels inspected; rendered crop/motion QA follows separately.',
                     'assetHashes': {i: assets[i]['sha256'] for i in images}}
    credits = []
    for i in images:
        a = assets[i]
        if a.get('location', {}).get('countryCode') == 'VN':
            c = next(x for x in candidates if x['id'] == i)
            credits.append(f"{c['creator']} · {c['license']} · {c['capturedDate'][:4]}")
    shot['sourceNote'] = ('Ảnh tư liệu Việt Nam · ' + ' / '.join(dict.fromkeys(credits))) if credits else 'Hình minh họa gốc · Ví dụ giả định'
    return shot

change('h1a', ['vn-noodle-aisle'], layout='object3d',
       motion={'kind': 'basket', 'revealFrames': [0, 16, 33]},
       headline='Đi mua một món. Về với cả giỏ?', eyebrow='QUYẾT ĐỊNH NHỎ / ĐỜI SỐNG',
       view='A documented Vietnam aisle alongside original cartons visibly dropping into a 3D basket. The growth is an illustrative situation, not a claim about the photographed shoppers.', role='mechanism')
change('h1b', ['vn-vinmart-cocacola'], headline='',
       view='A Vietnamese promotion label is visible beneath Coca-Cola bottles. Preserve the full portrait photograph; its old date and source credit identify archival context, not an applicable current selling price.')
change('h2', ['price-example'], layout='object3d',
       motion={'kind': 'price', 'stage': 'total', 'revealFrames': [0, 44, 100]},
       headline='Rẻ mỗi hộp. Tổng tiền vẫn tăng.',
       view='Original 3D one-carton versus two-carton example: totals 30,000 and 50,000 VND with a visible hypothetical-price label. A clear total-change line explains that lower unit price can increase total spending.', role='mechanism')
change('h3', ['vn-vinmart-times', 'vn-noodle-aisle', 'vn-bigc-interior'], layout='gallery3d',
       headline='Ba quyết định trước quầy tính tiền',
       view='Three clearly separated Vietnam photo planes show produce, aisle browsing and checkout context, introducing the journey rather than implying a specific person overspent.')
d = change('d1', ['vn-vinmart-times'], eyebrow='MIỄN TRỪ TRÁCH NHIỆM',
       headline='Phân tích để tham khảo.',
       body='Tình huống và số tiền dùng để minh họa. Mua thêm không luôn là lãng phí; cách bố trí cửa hàng có thể khác nhau.',
       view='A distinct calm disclaimer section after the hook, with the literal Vietnamese heading and two short scope statements beside archival Vietnam grocery context.')
change('c4', ['vn-noodle-aisle', 'vn-vinmart-cocacola'], layout='diptych',
       headline='02 / Nhìn thấy rồi mới nghĩ tới',
       view='An actual dense noodle shelf and an actual bright Vietnamese promotion tag, illustrating available choices and visual salience without asserting that the shopper was manipulated.')
change('c5', ['vn-noodle-aisle'], layout='object3d',
       motion={'kind': 'basket', 'revealFrames': [6, 102, 190]},
       headline='Một món vừa được thêm vào giỏ.', eyebrow='CÙNG MỘT HÀNH ĐỘNG / KHÁC LÝ DO',
       body='Nhớ ra đang thiếu — hay vừa nảy ra mong muốn?',
       view='A source-documented Vietnam grocery aisle next to animated original cartons being added to a basket. A short question distinguishes a remembered need from a newly formed desire, without assigning either motive to a real pictured person.', role='mechanism')
change('c6', ['fridge-check', 'vn-noodle-aisle'], layout='diptych',
       headline='Nhớ ra đang thiếu — hay vừa muốn có?',
       view='A genuinely open refrigerator with a person checking it is paired with a Vietnam grocery-basket context. These illustrate two decision contexts, not private intentions inferred from photos.')
change('c7', ['vn-noodle-aisle'],
       view='Actual grocery-aisle browsing and a red basket at a documented Vietnam location. The narrated research relationship rests on the cited study, not on photographed people.')
shots['c7']['sourceNote'] += ' · Nghiên cứu: Inman và cộng sự (2009)'
change('c8', ['vn-vinmart-cocacola'], headline='',
       view='A real bright promotion tag in a Vietnam shop. Retain the whole portrait image and make no inference about control or a shopper\'s willpower.')
change('c9', ['vn-sauce-prices', 'vn-seed-prices'], layout='diptych', headline='',
       view='Two actual Vietnam product shelves with legible VND price/weight labels, preserved using contain. They introduce what to compare; no old displayed price is presented as a current offer.')
change('c10', ['price-example'], layout='object3d',
       motion={'kind': 'price', 'stage': 'unit', 'revealFrames': [48, 99, 195]},
       headline='Một hộp 30.000đ. Hai hộp 50.000đ.',
       view='Original 3D cartons arrive at measured narration cues: one carton then two cartons, followed by 25,000 VND per carton. Display a persistent hypothetical example label and both total and unit prices.', role='mechanism')
change('c11', ['total-change'], layout='object3d',
       motion={'kind': 'price', 'stage': 'total', 'revealFrames': [0, 21, 107]},
       headline='Giá mỗi hộp giảm. Tổng tiền tăng.',
       view='Original one-versus-two 3D carton comparison with totals 30,000/50,000 and an explicit extra-spending label of 20,000. It must say extra spending, not total spending equals20,000.', role='mechanism')
change('c13', ['vn-noodle-aisle', 'vn-vinmart-times', 'vn-bigc-interior'], layout='gallery3d',
       headline='Giỏ đầy chưa nói lên lý do mua.',
       view='Three Vietnam grocery contexts in actual 3D photo planes. No photo establishes waste, what was planned or future use; the headline states this exact limitation.')
change('c14', ['fridge-kitchen', 'vn-noodle-aisle', 'vn-bigc-interior'], layout='object3d',
       motion={'kind': 'journey', 'revealFrames': [52, 95, 150]},
       headline='Ở nhà → Trên kệ → Tại quầy', body='Đồ đang có · Lựa chọn gặp phải · Tổng tiền phải trả',
       view='A home, grocery shelf and basket made from real Three.js geometry, with a carton traveling from shelf to basket at narration cues. Three corresponding photo contexts remain visible, including Vietnam aisle/checkout. The domestic fridge is explicitly generic stock, not claimed to be located in Vietnam.', role='mechanism')
change('c16', ['vn-vinmart-times'],
       view='Real grocery and produce-shopping context at VinMart Times City in Vietnam, supporting the everyday shopping setting rather than inferring intent.')
change('a3', ['vn-noodle-aisle'], layout='closing',
       headline='Bạn thường mua thêm món gì?',
       view='Actual Vietnam aisle and visible shopping basket behind the original question inviting comments. Preserve the entire last spoken sentence and narration tail.')

# Keep detailed source/attribution records, but stage only sources used by this revision.
used = {i for s in shots.values() for i in s['images']}
manifest['assets'] = [a for a in manifest['assets'] if a['id'] in used]
(ROOT / 'production-v5.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'manifest': 'production-v5.json', 'shots': len(shots), 'assets': len(manifest['assets']),
                  'object3d': [s['id'] for s in shots.values() if s['layout'] == 'object3d']}, ensure_ascii=False))
