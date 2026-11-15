"""Build this pilot's authored clause/asset contracts, keeping the original assets."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).parent
FILM = ROOT / 'long'


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


draft = load(ROOT / 'pilot-content.json')
catalog = load(FILM / 'source-candidates.json')
research = load(FILM / 'research.json')
assets = []
for row in catalog:
    observation = row['inspection']['observedSubjectAction']
    assets.append({
        'id': row['id'], 'file': 'long/' + row['file'], 'sha256': row['sha256'],
        'source': {'url': row['page'], 'creator': row['creator'], 'license': row['license'],
                   'licenseURL': row['licenseURL'], 'kind': 'stock'},
        'observed': {'subject': observation, 'action': observation,
                     'objects': row['sourceDescription'],
                     'limits': row['inspection']['doesNotEstablish']},
        'inspection': {'status': 'inspected', 'reviewer': 'Codex root',
            'sha256': row['sha256'],
            'observations': observation + ' Root opened both contact sheets of all sixteen actual files; also opened phone-list, fridge-kitchen, sale-shelf and phone-plan-couple at native size. These are illustrative stock subjects, not people asserted to overspend.'},
        'focus': row.get('recommendedFocus', [50, 50]),
    })

for key, description in {
    'shopping-list': 'Original cream note with three blank checklist prompts: item, quantity, and stock at home. It does not show a real shopper completing a list.',
    'price-example': 'Original explicitly hypothetical price comparison. One illustrated carton:30,000VND, two matching cartons:50,000VND; per-unit30,000 versus25,000. Not a store price.',
    'total-example': 'Same hypothetical comparison with the total-spending difference explicitly labeled +20,000VND. Both identical carton counts and arithmetic were visually inspected.',
    'total-change': 'Same hypothetical comparison, revised to label the difference CHI THÊM20.000VND instead of an ambiguous total label. One-versus-two quantities and arithmetic remain unchanged.'
}.items():
    file = FILM / 'assets' / (key + '.jpg')
    assets.append({'id': key, 'file': file.relative_to(ROOT).as_posix(), 'sha256': sha(file),
        'source': {'url': 'original:make_pilot_graphics.py', 'creator': 'TYRANNO original illustration',
                   'license': 'Original project graphic', 'licenseURL': 'original:project', 'kind': 'original'},
        'observed': {'subject': description, 'action': 'Static explanatory illustration, not filmed action.',
                     'objects': description, 'limits': 'A teaching example only; no real shop, transaction or price is established.'},
        'inspection': {'status': 'inspected', 'reviewer': 'Codex root', 'sha256': sha(file),
                       'observations': description + ' Opened full1920/1600pixel file and checked Vietnamese text/counts/arithmetic.'}})

video_rows = load(FILM / 'video-candidates.json')
for row in video_rows:
    if not row.get('derivative'):
        continue
    derivative = row['derivative']
    file = FILM / derivative['file']
    description = row['inspection']['observed']
    key = row['id']
    assets.append({'id': key, 'file': file.relative_to(ROOT).as_posix(), 'sha256': sha(file),
        'mediaType': 'video', 'availableFrames': derivative['availableFrames'],
        'trimBeforeFrames': 240 if key == 'clip-choose' else 0,
        'source': {'url': row['page'], 'creator': row['creator'], 'license': row['license'],
                   'licenseURL': row['licenseURL'], 'kind': 'stock'},
        'observed': {'subject': description, 'action': description, 'objects': 'Grocery shelf, products, shopper/cart or checkout.',
                     'limits': 'Illustrative foreign stock footage. Does not establish the shopper intention, overspending, impulse or payment; original audio is muted.'},
        'inspection': {'status': 'inspected', 'reviewer': 'Codex root', 'sha256': sha(file),
            'observations': description + ' Root inspected six timed frames across the complete source; bounded derivative retains original speed and visible action.'}})

by_id = {a['id']: a for a in assets}
needs = {
    'h1': 'A visibly filled grocery cart, with the hypothetical planned-versus-actual question over it.',
    'h2': 'Promotion labels beside a checkout setting, distinguishing unit-price cue from total spending; no invented price is attached to the real label.',
    'h3': 'People physically moving and choosing in a grocery store; broad trip context, not proof of a purchase motive.',
    'd1': 'A shopper and a clear caveat, without alleging anything about this stock subject.',
    'c1': 'An open refrigerator and a person reaching to look at the contents.',
    'c2': 'Readable original prompts for item, amount and stock at home; not a fabricated screen or a claimed real completed list.',
    'c3': 'A phone visibly held by a shopper; do not claim its unreadable screen contains our list.',
    'c4': 'Many product options on a shelf and actual bright promotional tags.',
    'c5': 'A shopper reaches for a jar and inspects it; her private motive remains unknown.',
    'c6': 'A home refrigerator and a grocery cart representing the two questions; these are illustrative alternatives, not a before/after biography.',
    'c7': 'A store context with a precise research citation; the photo does not depict research participants.',
    'c8': 'A visible offer sign as an example of a cue, without treating all shoppers as controlled.',
    'c9': 'A real multi-unit promotional label; numeric explanation follows in a separate hypothetical graphic.',
    'c10': 'One carton versus two identical cartons,30,000 versus50,000 total and30,000 versus25,000 unit price, explicitly hypothetical.',
    'c11': 'The same quantities and prices, with +20,000 total spending clearly visible.',
    'c12': 'Food at home representing planned consumption; do not claim these particular foods were purchased on promotion.',
    'c13': 'A filled basket that establishes quantity only; no judgment about the person.',
    'c14': 'Three distinct stages in the retained3D gallery: fridge, shelf offer, checkout unloading.',
    'c15': 'A basket at the checkout while the narrator proposes a pause; footage does not claim the shopper actually follows the advice.',
    'c16': 'An ordinary checkout scene, with no implication of guilt or measured savings.',
    'a1': 'Original list prompts beside groceries at home; an invitation to compare, not proof of a real household experiment.',
    'a2': 'Groceries at home as context for reflecting on motives, no asserted waste.',
    'a3': 'A grocery basket and a short, readable comment/subscribe CTA.'
}
sections = []
for raw in draft['sections']:
    shots = []
    clauses = []
    for clause in raw['clauses']:
        if clause['id'] == 'h1':
            clauses += [{**clause, 'id': 'h1a', 'text': 'Một món cần mua, cả giỏ mang về.'},
                        {**clause, 'id': 'h1b', 'text': 'Chuyện có thể bắt đầu từ một bảng giá rất hấp dẫn.',
                         'images': ['sale-shelf'], 'headline': ''}]
        else:
            clauses.append(clause)
    for clause in clauses:
        key = clause['id']
        images = clause['images']
        if key == 'c14':
            images = ['fridge-kitchen', 'sale-shelf', 'total-change']
        if key == 'c11':
            images = ['total-change']
        if key == 'c12':
            images = ['price-example', 'vegetables-home']
        if key == 'h3' and 'clip-aisle' in by_id:
            images = ['clip-aisle']
        if key == 'c5' and 'clip-choose' in by_id:
            images = ['clip-choose']
        if key == 'c15' and 'clip-checkout' in by_id:
            images = ['clip-checkout']
        graphic = key in ['c2', 'c10', 'c11']
        row = {k: v for k, v in clause.items() if k not in ['text', 'images']}
        row.update({'phrase': ' '.join(clause['text'].split()[:6]), 'narrationClause': clause['text'],
            'layout': 'graphic' if graphic else 'diptych' if key == 'c12' else clause.get('layout', 'full'), 'images': images,
            'needToSee': needs.get(key, needs['h1']), 'mediaRole': 'mechanism' if graphic else 'context',
            'supports': needs.get(key, needs['h1']),
            'limits': 'The spoken situation is illustrative. Stock pictures show only the observed visible action; they do not establish private intent or causal effects. Research claims depend on cited sources, and the price arithmetic is hypothetical.',
            'review': {'status': 'inspected', 'reviewer': 'Codex root',
                'observations': needs.get(key, needs['h1']) + ' Selected files reviewed against this whole narrated clause; subject identity and hypothetical status are not misrepresented.',
                'assetHashes': {name: by_id[name]['sha256'] for name in images}}})
        if graphic:
            row.pop('headline', None)
        row.setdefault('sourceNote', 'Minh họa · Pexels' if not graphic else 'Minh họa nguyên bản · TYRANNO')
        if key == 'c7':
            row['sourceIds'] = ['inman2009']
            row['sourceNote'] = 'Ảnh minh họa · Pexels | Nghiên cứu: Inman, Winer & Ferraro (2009)'
        if key in ['a1', 'c12', 'c14']:
            row['sourceNote'] = 'Ảnh minh họa · Pexels | Minh họa nguyên bản · TYRANNO'
        if key == 'c14':
            row['needToSee'] = row['supports'] = 'Three stages: actual home fridge, actual shelf cue, and a labeled hypothetical total-spending illustration. The graphic is not a real checkout receipt.'
            row['review']['observations'] = row['supports'] + ' Revised after independent review found the previous checkout-scale photo did not show a total.'
        if key == 'h1b':
            row['needToSee'] = row['supports'] = 'Actual promotional price tags immediately when the narrator mentions a price board; no hypothetical Vietnamese price is attributed to these foreign tags.'
            row['review']['observations'] = row['supports']
        shots.append(row)
    sections.append({'phase': raw['phase'], 'text': ' '.join(c['text'] for c in raw['clauses']), 'shots': shots})

used = {name for section in sections for shot in section['shots'] for name in shot['images']}
manifest = {'schema': 'reference-video-production/1', 'id': 'di-sieu-thi-pilot-2026-11-13',
    'direction': 'long', **{key: draft[key] for key in ['title', 'editorialAngle', 'audience', 'hookPromise', 'payoff']},
    'sections': sections, 'assets': [a for a in assets if a['id'] in used],
    'researchSources': research['sources'],
    'claims': [{'id': 'in-store-planning',
        'text': next(c['text'] for s in draft['sections'] for c in s['clauses'] if c['id'] == 'c7'),
        'sourceIds': ['inman2009'], 'scope': 'Observed shopper/store/activity associations in the source study.',
        'limitations': 'Not a randomized proof; not a universal rate or claim about stock subjects or Vietnamese stores.'}],
    'status': 'pilot-awaiting-render-review-and-user-feedback',
    'reviewPolicy': 'Integrity checks and actual editor observations remain separate from human user approval.',
    'referenceLearning': 'workflows/reference-video/REFERENCE_LEARNING.md',
    'audio': {
        'music': [{'file': file, 'sha256': sha(ROOT.parents[1] / file)} for file in [
            'videos/2026-11-11-cinematic-reset/audio/motion-score.mp3',
            'videos/2026-11-11-ai-va-cong-viec-5phut/audio/analysis-score.mp3',
            'videos/2026-11-11-ai-va-cong-viec-5phut/audio/agency-score.mp3']],
        'cues': [{'file': 'videos/2026-11-13-di-sieu-thi/long/audio/grocery-handling.mp3',
                  'sha256': sha(FILM / 'audio/grocery-handling.mp3'),
                  'phrase': 'Trước khi trả tiền, dừng một', 'offsetSeconds': 0.6,
                  'role': 'Quiet grocery-handling texture under actual basket-unloading footage; no false scanner or payment sound.'}]
    }}
destination = ROOT / (sys.argv[1] if len(sys.argv) > 1 else 'production-v3.json')
manifest['id'] += '-r03'
destination.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print({'assets': len(manifest['assets']), 'shots': sum(len(s['shots']) for s in sections),
       'words': len('\n\n'.join(s['text'] for s in sections).split()),
       'clips': [a['id'] for a in manifest['assets'] if a.get('mediaType') == 'video']})
