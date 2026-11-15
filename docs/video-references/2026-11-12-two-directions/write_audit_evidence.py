"""Keep reviewed observations separate from acquisition metadata."""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / '2026-11-11'
identities = json.loads((HERE / 'channel-identities.json').read_text(encoding='utf-8'))
channels = {item['channel']: {k: item[k] for k in ['channel_id', 'channel_url', 'uploader_url']} for item in identities}
reviews = [
    ('JlfAd_OaFek', [0, 34.52], [34.52, 43.68], [43.68, 47.8], [1070.82, 1075.70],
     'Situational AI use leads into dependence and work question; source/personal-opinion caveat and invitation to correct; sponsor disclosure; closing subscribe CTA.',
     'Illustrated street and mascot plus three real-image cards; purple caveat scene; source document highlights and diagrams in body; sponsor marks and subscribe graphic.', True),
    ('podWgLH4b3M', [0, 61.7], [61.7, 68.6], [68.6, 73.9], [977.4, 987.4],
     'Low prices and buyer behavior lead to changing business conditions; source/personal-experience caveat; mechanism explanation; topic question, comments and subscription.',
     'Ecommerce photographs, illustrated clothes and mascot, customs/store pictures; purple caveat scene; factory and highlighted document samples; subscribe graphic.', True),
    ('w3z43Hlzq3c', [0, 60.4], [60.4, 70.2], [70.2, 75.3], [1246.4, 1251.0],
     'Multiple local protest examples lead to question; scope clarification says separate places have separate problems; country-by-country explanation; subscribe CTA. This is not the same generic disclaimer as two other samples.',
     'Actual protest imagery in opening; purple mascot scene around clarification; flags, hospital, icons and chapter title in body; subscribe graphic.', False),
    ('29B8-FtuC6U', [0.56, 84.4], None, [129.17, 137.01], [879.94, 893.0],
     'Paradox and restaurant analogy; brand introduction at 84.4s and logo at sampled 94s; promotional segment from 96.28s; return to argument around 129s; closing synthesis, visual subscribe end screen. No spoken disclaimer found in inspected opening transcript.',
     'Real-life background imagery, dark overlay, mic/waveform/player repeated; logo bumper; promotional shot; end screen at 892s.', False),
    ('5zqAMK2qsfM', [0, 81.32], None, [124.652, 130.252], [1261.99, 1289.0],
     'Saved articles, videos and books become consumption-versus-output conflict; brand at 81.32s, logo around sampled 87/91s, promotion from 92.8s, main argument at 124.652s. Closing asks for a concrete practice and comment; visual subscribe end screen. No spoken disclaimer found in inspected opening transcript.',
     'Laptop/phone, books and writing/work imagery under repeated dark podcast overlay; logo; promotional image; plant imagery on comment prompt; end screen.', False),
    ('5uTC396kCs4', [0.4, 94.32], None, [137.53, 145.33], [1299.35, 1320.0],
     'Same dollar amount contrasts two groups, then water metaphor and five-part promise; brand at 94.32s, logo at sampled 100/104s and promotion from 106.08s; mechanism begins at 137.53s; metaphorical closing, black sampled frame at 1319s. No spoken disclaimer found in inspected opening transcript.',
     'Money, calculator, production, port and finance imagery; repeated dark podcast overlay; logo and promotional image; black last sampled frame.', False),
]
sources = []
for video_id, hook, disclaimer, main, closing, text_observation, visual_observation, generic in reviews:
    source_dir = HERE / video_id
    if not (source_dir / 'evidence.json').exists():
        source_dir = OLD / video_id
    metadata = json.loads((source_dir / 'evidence.json').read_text(encoding='utf-8'))
    times = json.loads((HERE / 'targeted-samples' / video_id / 'sample-times.json').read_text(encoding='utf-8'))
    sources.append({
        'id': video_id,
        'url': metadata['url'],
        'title': metadata['title'],
        'channel': metadata['channel'],
        'channel_identity': channels[metadata['channel']],
        'duration_seconds': metadata['duration'],
        'source_directory': str(source_dir.relative_to(HERE.parent)).replace('\\', '/'),
        'media': metadata.get('media'),
        'transcript': metadata.get('transcript'),
        'inspected_contact_sheet': str((source_dir / 'contact-sheet.jpg').relative_to(HERE.parent)).replace('\\', '/'),
        'inspected_targeted_sheet': f'targeted-samples/{video_id}/targeted-contact-sheet.jpg',
        'targeted_sample_seconds': times,
        'approximate_structure_seconds': {'hook': hook, 'disclaimer_or_scope': disclaimer, 'main_entry': main, 'closing': closing},
        'generic_disclaimer_observed': generic,
        'transcript_observation': text_observation,
        'visual_observation': visual_observation,
        'claims_not_made': ['full continuous viewing', 'listening by ear', 'fact-check of content claims', 'license to reuse source visuals', 'measured shot density'],
    })
report = {
    'date': '2026-11-12',
    'timezone': 'Asia/Saigon',
    'status': 'sampled_visual_and_transcript_review_complete',
    'scope': 'Six sparse full-runtime contact sheets and six targeted opening/transition/ending sheets opened and inspected; opening/closing/caveat transcripts read. No full audiovisual viewing or auditory assessment.',
    'user_requested_structure': ['hook', 'disclaimer', 'main_content', 'call_to_action'],
    'structure_application': 'Apply all four stages to both new directions as user request; do not claim this exact four-part order occurs in every source.',
    'production_guide': 'REFERENCE_AUDIT.md',
    'sources': sources,
    'proposed_not_observed': {
        'long_inspired': 'Conversational situational explanation; real photos/documents in depth, comparisons and useful 3D cause-paths. Original identity and images.',
        'hidden_self_inspired': 'Narration-led curiosity and layered causes; real photographs in a spatial archive, meaningful near/far moves and short diagrams. Preserve project narrator; remove recurring podcast mic/player.',
    },
}
(HERE / 'evidence.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Wrote review evidence for {len(sources)} sources.')
