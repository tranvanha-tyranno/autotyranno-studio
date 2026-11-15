"""Normalize source-review records into concrete install manifests."""
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def source_item(repo, path, alias, review, conflicts, category):
    folder = BASE / 'sources' / repo.replace('/', '__')
    receipt = read(folder / 'receipt.json')
    snapshot = Path(receipt['snapshot'])
    archive = folder / 'source.zip'
    if not archive.exists():
        archive = folder / 'archive.zip'
    return dict(repo=repo, canonicalURL=f'https://github.com/{repo}', commit=receipt['commit'],
                snapshot=str(snapshot), archive=str(archive),
                archiveSHA256=hashlib.sha256(archive.read_bytes()).hexdigest(),
                path=path, alias=alias,
                skillSHA256=hashlib.sha256((snapshot / path / 'SKILL.md').read_bytes()).hexdigest(),
                review=review, userPreferenceConflicts=conflicts, category=category)


if __name__ == '__main__':
    a = read(BASE / 'group-a.json')
    sources = {r['repo']: r for r in a['repositories']}
    skills = {(s['repo'], s['skillRootRelative']): s for s in a['skills']}
    manifest = []
    for candidate in a['candidateInstallPaths']:
        repo = sources[candidate['repo']]
        skill = skills[(candidate['repo'], candidate['path'])]
        assert skill['fullSkillRead']
        manifest.append(dict(repo=repo['repo'], canonicalURL=repo['canonicalURL'], commit=repo['commit'],
                             snapshot=repo['snapshot'], archive=str(ROOT / repo['archive']),
                             archiveSHA256=repo['archiveSHA256'], path=candidate['path'], alias=candidate['name'],
                             skillSHA256=skill['sha256'], review=skill['reviewMethod'],
                             userPreferenceConflicts=skill['userPreferenceConflicts'],
                             category='motion, simulation and video direction'))
    save(BASE / 'install-a.json', manifest)
    root_choices = [
        ('win4r/video-director', 'video-director', 'video-director', 'direction',
         'Full SKILL and references/quality.md; other refs retained for task-specific reading.',
         ['Use autonomous mode already authorized by user.', 'No forced hook text/subtitles/first-3s CTA in this project.',
          'Use exact narration clock and recorded SFX; no automatic synthesized score or house palette.',
          'QA metrics and critic scores do not establish user approval.']),
        ('ishuagrawal/skills', 'skills/video-by-reference', 'video-by-reference', 'reference study',
         'Full SKILL and references/story-and-pacing.md; engine/scripts retained, not executed.',
         ['Downloads and reversible work already authorized.', 'Do not replace real footage with generated drawings.',
          'Originality is causal/narrative, not copying reference shots.', 'Use actual recorded SFX; no automatic oscillator score.',
          'Rendered moving scenes must be inspected; stills alone are insufficient.']),
        ('Barty-Bart/motion-graphics', 'skills/motion-broll', 'motion-broll', 'phrase-aligned cutaways',
         'Full SKILL; bundled engine reference is retained, not runtime tested.',
         ['User already authorized storyboard/drawing work; no extra plan-approval pause.',
          'Motion graphics are supplementary explanations, not real B-roll.',
          'No presenter requirement for bread documentary; no fixed shape/cursor style for whole film.']),
        ('Barty-Bart/motion-graphics', 'skills/object-separation', 'object-separation', 'local compositing',
         'Full SKILL including code examples, static only.',
         ['SAM model/runtime not downloaded or tested.', 'Use batch-isolated outputs and inspect mask motion before adoption.']),
        ('Barty-Bart/motion-graphics', 'skills/sound-effects', 'sound-effects', 'sound design',
         'Full SKILL; source manifest and code retained for task-specific audit.',
         ['Recorded Foley must match physical meaning and measured narration, not every camera move.',
          'Existing licensed music and user choices do not require asking again.',
          'Each actual source/license must be checked before use; archive claims are not new license verification.',
          'Mix measurements cannot establish auditory taste or user acceptance.']),
        ('Aaryan-Kapoor/video-production-skill', 'skills/video-production', 'video-production', 'production and QC',
         'Full SKILL and references/production-standards.md; scripts not executed.',
         ['Keep project videos/<batch> instead of ~/video-productions.', 'Current voice/provider selection overrides Kokoro default.',
          'No Tailscale publication or remote hosting from installation.',
          'Do not default to dark glowing diagram slides or call frame QA aesthetic acceptance.']),
        ('smixs/visual-skills', 'video', 'ai-video-prompt-direction', 'storyboard and generation prompts',
         'Full SKILL; dramaturgy.md lines1-210 and universal-rules.md lines1-100; model files retained, not fact-verified.',
         ['Credit Serge Shima under CC-BY-4.0 when adapting/distributing skill material.',
          'Current API capabilities/pricing/model-specific syntax require primary documentation verification before use.',
          'No paid model calls or uploads from skill installation; no new presenter in bread film.']),
    ]
    root_manifest = [source_item(repo, path, alias, review, conflicts, category)
                     for repo, path, alias, category, review, conflicts in root_choices]
    save(BASE / 'install-root.json', root_manifest)
    save(BASE / 'group-root-review.json', {
        'installedCandidates': root_manifest,
        'additionalFullSkillReadsArchived': ['Yusuke710/manim-skill/skills/manim-skill',
                                           'TashanGKD/tashan-research-skills/skills/manim-agent',
                                           'liangdabiao/math-concept-film'],
        'partialReadsArchived': ['Barty-Bart/explainer-engaging (all prose, inline renderer output truncated)',
                                 'Clipwing/skills/skills/real-sfx (partial, output truncation)',
                                 'Clipwing/skills/skills/hyperframes-to-after-effects (full SKILL; AE not needed)'],
        'archiveOnlyReasons': {
            'Barty-Bart/explainer-default/explainer-high-energy': 'Specialized ad presets retained for reading; not deeply reviewed.',
            'Clipwing/skills': 'No top-level license found in snapshot; source retained for research, no active installation.',
            'Yusuke710/manim-skill': 'Competing voice/subtitle/storage defaults; iart-manim selected as active entrypoint.',
            'TashanGKD/tashan-research-skills': 'Manim agent needs external paid Qwen pipeline; other19skills unrelated to video.',
            'liangdabiao/math-concept-film': 'Chinese/480p/subtitle/fixed-style defaults and soft-defect dismissal conflict with this project.',
            'smixs/visual-skills/image': 'General image prompting archived; existing imagegen skill remains available.'},
        'externalCodeExecuted': False, 'runtimeTested': False})
    print('MANIFESTS_READY', len(manifest), len(root_manifest))
