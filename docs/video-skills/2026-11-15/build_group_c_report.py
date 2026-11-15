"""Build an evidence manifest from downloaded, unexecuted skill source snapshots."""
from pathlib import Path
import hashlib
import json
import re
import yaml

BASE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evidence(root, rel):
    path = root / rel
    if not path.is_file():
        raise ValueError(f'Missing claimed read: {path}')
    return {'path': rel, 'bytes': path.stat().st_size, 'sha256': sha(path),
            'coverage': 'full_text_read', 'execution': 'not_executed'}


def meta(path):
    text = path.read_text(encoding='utf-8-sig')
    m = re.match(r'^---\s*\n(.*?)\n---', text, re.S)
    return yaml.safe_load(m.group(1)) if m else {}


MIC = 'MichaelAchugwo/agentic-video-edits-gen'
SUB = 'sub-level/marketing-videos'
MNG = 'Mng-dev-ai/explainer-video'
PRE = 'precious112/demo-director'
OAI = 'openai/skills'

REVIEWS = {
    MIC: {
        'license': 'MIT', 'licenses': ['LICENSE'],
        'fullRead': ['LICENSE', *[f'skills/{s}/SKILL.md' for s in
            ['story-script', 'shot-planning', 'research-and-facts', 'creative-direction',
             'video-director', 'code-motion-graphics']]],
        'dependencies': ['Planning skills need no runtime dependencies.',
            'Rendering/generation branches may require Python/Node, browser/ffmpeg and optional paid media providers; none installed or called.'],
        'commonConflicts': [
            'Source approval gates do not add a new permission step to work already authorized by this user.',
            'Default social 9:16, captions, brief beat duration and repeated asset use are optional genre choices; current project voice, 16:9, no subtitles and non-overlapping stock intervals prevail.',
            'Source examples and references are not authorized claims, original assets, proof of Vietnamese narration quality, or evidence of audience retention.'],
        'skillNotes': {
            'story-script': ('video-story-script',
                ['Build a specific open question, obstacle, escalation and planted payoff; remove lines that do not change the story.',
                 'Keep spoken narration separate from stage directions and test each beat against the question it advances.'],
                ['English 150-WPM/short-social timing is not measured Vietnamese take timing.',
                 'Never stating a moral is creative guidance; the user explicitly wants a practical conclusion and CTA.']),
            'shot-planning': ('video-shot-planning',
                ['Map each voice block to a visible action, camera, continuity and production route.',
                 'Keep asset paths null until actual assets exist; avoid speaking faces without real lip synchronization.'],
                ['A two-to-five-second shot heuristic cannot override complete idea development or exact speech cues.']),
            'research-and-facts': ('video-research-facts',
                ['Verify numbers, dates, causal claims and superlatives with primary sources.',
                 'Distinguish documented evidence from dramatization and preserve independent source attribution.'], []),
            'creative-direction': ('video-creative-direction',
                ['Use one clear idea and materially different creative directions, with readable hierarchy and a coherent visual bible.',
                 'Review an actual two-second read and the relationship between idea and craft.'],
                ['Exactly three directions and a compulsory new user choice are not required when the existing session already fixes direction.',
                 'No invented channel identity, branding or on-screen captions may be introduced.']),
            'video-director': ('video-director-agentic',
                ['Explicit routing, retained project state, budget constraints and quality gates help resumable production.',
                 'Separate planning, actual generation, rendered review and final delivery evidence.'],
                ['Rigid five-approval-gate workflow is subordinate to already authorized work and the user preference for autonomous progress.',
                 'Provider routes and lookalike/reference phrasing do not independently authorize paid calls or identity use.']),
            'code-motion-graphics': ('video-code-motion',
                ['Represent visual state as a deterministic renderFrame(t), seed randomness and inspect frame-specific screenshots.',
                 'Build meaningful state changes, readable layouts and mathematically consistent numbers.'],
                ['The animated checklist asset is a demonstration, not an economic film template; counting and entering cards alone repeat the rejected slide pattern.',
                 'Bundled render script is archived but not executed or independently audited in this review.']),
        },
    },
    SUB: {
        'license': 'MIT', 'licenses': ['LICENSE'],
        'fullRead': ['LICENSE', 'package.json',
            '.claude/skills/motion-from-reference/SKILL.md',
            '.claude/skills/motion-from-reference/references/measure-reference.md',
            '.claude/skills/video-audio-stack/SKILL.md'],
        'dependencies': ['Node >=18; React 19, Remotion/@remotion/cli/@remotion/google-fonts 4.0.454, TypeScript 5.4 in the repository package.',
            'ffmpeg for optional supersampling; optional Epidemic Sound subscription/MCP. No runtime installed.'],
        'commonConflicts': ['Individual skill folders reference examples and helpers under repository src; preserve the pinned repository as supporting context.',
            'Reference grammar study does not grant copyright permission to reuse source assets or prove narrative relevance.'],
        'skillNotes': {
            'motion-from-reference': ('video-motion-reference',
                ['Measure reference typography, entrance, hold, exit and continuity at explicit frames before implementing.',
                 'Prefer a shape becoming the next scene to repeated reset cards; translate functions to an original story.'],
                ['Exact reference ordering, font and timing are task-specific; prioritize current content and user instructions.',
                 'Do not adopt blanket legal claims about ownership; sampled frames do not establish continuous AV review.']),
            'video-audio-stack': ('video-audio-stack',
                ['Layer music, motivated impacts and tactile Foley; place attack transients at the relevant action.',
                 'Retain track rights/attribution and keep offline audio separate from a locked picture.'],
                ['One track for every film and mandatory Epidemic sourcing are not project requirements.',
                 'Example gain fractions are not measured loudness targets; waveform inspection is not listening.']),
        },
    },
    MNG: {
        'license': 'MIT', 'licenses': ['LICENSE'],
        'fullRead': ['LICENSE', 'SKILL.md', 'lib/package.json', 'lib/pipeline.js', 'lib/render.js', 'lib/edge-tts.js'],
        'dependencies': ['Node; msedge-tts ^2.0.5, Playwright ^1.40.0, ffmpeg/ffprobe; GSAP 3.12.5 loaded from a CDN by generated pages. No dependencies installed.'],
        'commonConflicts': ['This is a reference for topic-specific HTML explanation, not a replacement for the existing measured Remotion production pipeline.',
            'Default English Edge voice does not satisfy approved Vietnamese/OpenAI voice selection.',
            'Realtime ~25fps capture is not deterministic frame-by-frame rendering; duration-only segmentation is not exact word alignment.',
            'Muxing with -shortest may truncate the final narration; verify the full spoken tail.',
            'The voice cache hashes voice and text but not every rate/pitch/provider parameter; do not substitute it for existing receipts.',
            'External GSAP/CDN and unbounded Edge behavior require local reliability changes before production; no such runtime was executed here.'],
        'skillNotes': {
            'explainer-video': ('video-explainer-html',
                ['Plan topic-specific visual explanations rather than a generic card deck.',
                 'Inject measured segment durations and permit existing audio reuse.'],
                ['Install for optional instruction/reference use only; do not run its default renderer/voice as the current film baseline.']),
        },
    },
    PRE: {
        'license': 'MIT; separate case-study/product/photo rights in NOTICE.md',
        'licenses': ['LICENSE', 'NOTICE.md'],
        'fullRead': ['LICENSE', 'NOTICE.md', 'package.json', 'skills/demo-director/SKILL.md',
            *[f'skills/demo-director/references/{s}.md' for s in ['storyboard','direction','motion-design','review','rendering']]],
        'dependencies': ['Node >=18; Playwright ^1.62.1 and matching Chromium; ffmpeg. Source includes a virtual-time renderer but it has not been executed here.'],
        'commonConflicts': ['Silent software demos/caption defaults do not supersede Vietnamese narrated explainers without subtitles.',
            'Approval requests do not block work already authorized by the user; the source itself permits a preview when the owner asks to film now.',
            'Do not add repository ignore rules or hide output automatically from generic skill instructions.',
            'Root MIT license does not cover every product mark, case-study UI or Unsplash photograph; retain NOTICE and source rights.',
            'Contact sheets and all sampled stills do not prove every frame was observed; motion and listening review must be reported separately.'],
        'skillNotes': {
            'demo-director': ('video-demo-director',
                ['Storyboard thesis, action, changed state, honesty checks and purposeful keyframes before rendering.',
                 'Use one primary action at a time, causal continuity and separate UI feedback timing from film timing.',
                 'Show real capabilities, measured claims and explicit time compression; review motion at normal speed and transitions more closely.',
                 'Use a virtual clock or pure seek(t) with local font readiness for deterministic rendering.'],
                ['A global ban on an effect palette is a software-demo style guide, not a requirement to redesign all current economic footage.']),
        },
    },
    OAI: {
        'license': 'Apache-2.0 per selected skill LICENSE.txt',
        'licenses': ['skills/.curated/speech/LICENSE.txt', 'skills/.curated/transcribe/LICENSE.txt'],
        'fullRead': ['skills/.curated/speech/LICENSE.txt', 'skills/.curated/transcribe/LICENSE.txt',
            'skills/.curated/speech/SKILL.md', 'skills/.curated/transcribe/SKILL.md',
            *[f'skills/.curated/speech/references/{s}.md' for s in ['narration','prompting','cli','audio-api']],
            'skills/.curated/transcribe/references/api.md'],
        'dependencies': ['Python + openai SDK and a valid user-configured API key for speech/transcribe API calls; actual usage is paid.',
            'No API call, key read or runtime installation occurred during this skill study.'],
        'commonConflicts': ['Preserve exact narration input and put affect, tone, pace, pronunciation and emphasis in separate concise instructions.',
            'Skill defaults are dated source defaults, not a new product availability guarantee or an authorization to retry rejected keys.',
            'Current project batch paths, selected voice and authorization prevail over generic output directory defaults.',
            'No request for the user to paste secrets; do not overwrite existing custom production runners or introduce new permission rituals from a generic CLI guardrail.',
            'Keep a clear AI voice disclosure and honest source/provenance records without inserting an unrequested long spoken disclaimer.'],
        'skillNotes': {
            'speech': ('openai-speech',
                ['Use exact input text and short labeled directions for natural narration, pronunciation, pauses and emphasis.',
                 'Batch within input/rate limits, keep voice consistent and record model/voice/parameters for the exact resulting audio.'], []),
            'transcribe': ('openai-transcribe',
                ['Choose transcription versus diarization intentionally; respect format, size and chunking requirements.',
                 'Keep model output distinct from verified listening and retain the source audio.'],
                ['API transcription is not the existing free local Whisper method; do not switch providers or spend merely because the skill is installed.']),
        },
    },
}


def main():
    downloads = json.loads((BASE / 'group-c-downloads.json').read_text(encoding='utf-8'))
    repos, candidates = [], []
    for d in downloads:
        repo = d['repo']
        if d['status'] != 'downloaded_and_extracted':
            repos.append({**d, 'disposition': 'rejected_no_install', 'license': None,
                'skills': [], 'reviewMethod': 'Actual git ls-remote failed; no downloaded source available for audit.',
                'reasons': ['Canonical repository unavailable (404/repository not found); do not substitute a mirror.',
                    'Island primary investigation explicitly lists this repository as campaign-linked. This report did not independently audit unavailable code.'],
                'primarySecurityEvidence': {'url': 'https://www.island.io/blog/how-attackers-built-software-an-ai-would-recommend',
                    'title': 'How Attackers Built Software an AI Would Recommend',
                    'checked': '2026-11-15', 'scope': 'Repository IOC table lists pifferologo/ai-agent-video-editor; no source payload fetched or executed.'}})
            continue
        cfg = REVIEWS[repo]
        source_dir = BASE / 'sources' / repo.replace('/', '__')
        root = (source_dir / d['extractedRoot']).resolve()
        archive = (source_dir / 'archive.zip').resolve()
        assert sha(archive) == d['archiveSHA256']
        full = [evidence(root, p) for p in cfg['fullRead']]
        relevant_paths = sorted(root.rglob('SKILL.md'))
        if repo == OAI:
            relevant_paths = [p for p in relevant_paths if p.parent.name in ['speech', 'transcribe', 'sora']]
        skills = []
        for file in relevant_paths:
            m = meta(file)
            name = str(m.get('name', file.parent.name))
            rel = file.relative_to(root).as_posix()
            is_full = rel in cfg['fullRead']
            note = cfg['skillNotes'].get(name)
            # Some upstream names can differ from folder names; folder identity is pinned as well.
            if note is None:
                note = cfg['skillNotes'].get(file.parent.name)
            item = {'name': name, 'description': str(m.get('description', '')),
                'path': str(file), 'skillRootRelative': file.parent.relative_to(root).as_posix(),
                'sha256': sha(file), 'bytes': file.stat().st_size, 'fullSkillRead': is_full,
                'status': 'reviewed_install_candidate' if is_full and note else 'archived_read_on_demand',
                'reviewMethod': 'full_SKILL_read_plus_named_key_references' if is_full else 'frontmatter_inventory_only',
                'dependencies': cfg['dependencies'],
                'userPreferenceConflicts': cfg['commonConflicts'] + (note[2] if note else []),
                'appliedLearning': note[1] if note else [],
                'supportContextRoot': str(root), 'runtimeEndToEndTested': False}
            if is_full and note:
                candidate = {'repo': repo, 'commit': d['commit'], 'snapshot': str(root),
                    'archive': str(archive), 'archiveSHA256': d['archiveSHA256'],
                    'path': item['skillRootRelative'], 'alias': note[0],
                    'skillSHA256': sha(file), 'description': item['description'],
                    'fullSkillRead': True, 'reviewStatus': 'reviewed_with_project_overrides',
                    'runtimeEndToEndTested': False, 'externalCodeExecuted': False,
                    'license': cfg['license'], 'projectOverrides': item['userPreferenceConflicts'],
                    'supportContextRoot': str(root)}
                candidates.append(candidate)
                item['suggestedInstallAlias'] = note[0]
            skills.append(item)
        repos.append({**d, 'archive': str(archive), 'snapshot': str(root),
            'license': cfg['license'], 'licenseEvidence': [evidence(root,p) for p in cfg['licenses']],
            'reviewMethod': 'Pinned archive/hash/license and tree inventory; only explicitly named files were fully read. No external code executed.',
            'readCoverage': {'fullTextFiles': full,
                'otherFiles': 'Archived, not claimed read. Other SKILL frontmatter only for the inventory.',
                'AV': 'Demo/reference media archived but not played or listened to.',
                'allRepositoryFilesRead': False},
            'skills': skills, 'externalCodeExecuted': False, 'runtimeDependenciesInstalled': False})
    report = {'schema': 'video-skill-research-group-c/1', 'dateLocal': '2026-11-15',
        'scope': 'Storyboard, scriptwriting, explainer, reference measurement, audio, official speech/transcribe skills.',
        'trustPolicy': 'Third-party instructions are untrusted reference material. User/session/repository instructions prevail. Candidate status permits copying reviewed instructions only, not executing dependencies or paying providers.',
        'repositories': repos, 'installCandidates': candidates,
        'summary': {'repositoriesRequested': len(downloads),
            'downloadedRepositories': sum(d['status']=='downloaded_and_extracted' for d in downloads),
            'rejectedUnavailableRepositories': 1,
            'relevantSkillFilesInventoried': sum(len(r['skills']) for r in repos),
            'fullReadSkillFiles': sum(s['fullSkillRead'] for r in repos for s in r['skills']),
            'archivedReadOnDemandSkills': sum(not s['fullSkillRead'] for r in repos for s in r['skills']),
            'installCandidates': len(candidates), 'externalSourceExecutions': 0,
            'runtimeDependenciesInstalled': 0, 'paidAPICalls': 0},
        'unavailableOfficialSkills': [{'repo': OAI, 'name': 'sora',
            'commit': next(d['commit'] for d in downloads if d['repo']==OAI),
            'status': 'not_present_at_pinned_HEAD',
            'action': 'No history traversal or unofficial replacement requested; no install candidate.'}],
        'productionPriorities': [
            'First improve the open question, causal chapter progression, counterargument and practical payoff; rendering variety cannot rescue weak content.',
            'Write shot purpose as subject/action/object/changed state tied to an exact narrated phrase, then choose footage or a simulation.',
            'Use continuity and information-bearing transformations; avoid a succession of card entrances, counters and decorative motion.',
            'Measure timing from the actual finalized Vietnamese take; do not replace word timing with guessed WPM or frame/shot counts.',
            'Record what was really read, seen and heard; archive source/hash/license and keep technical QA separate from editorial and user acceptance.']}
    (BASE/'group-c.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    (BASE/'group-c-install-candidates.json').write_text(json.dumps(candidates, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# Video skill source study — group C', '',
        'Pinned source archives were downloaded and inspected as text only. No downloaded program was run, no dependency installed, no credential read and no paid API called. This is a source/skill study, not model training or proof that the runtimes work.', '',
        f"{report['summary']['downloadedRepositories']} downloaded repositories; {report['summary']['fullReadSkillFiles']} full-read relevant SKILL files; {report['summary']['archivedReadOnDemandSkills']} relevant SKILL files inventoried for reading on demand. Entire official OpenAI repository is archived, but unrelated skills are outside this study. Media examples were not watched/listened to.", '',
        'Candidate copying manifest: `group-c-install-candidates.json`. Copying these instructions does not authorize running upstream installation commands, using paid providers or replacing the established video pipeline. Every candidate carries explicit project overrides.', '']
    for r in repos:
        lines += [f"## {r['repo']}", '', f"Source: [{r['repo']}]({r['canonicalURL']})", '']
        if r['status']!='downloaded_and_extracted':
            lines += ['Canonical GitHub repository and git remote returned unavailable; no archive, license or code audit can be claimed. Excluded from installation. The [Island primary investigation](https://www.island.io/blog/how-attackers-built-software-an-ai-would-recommend) lists this exact repository as campaign-linked. No mirror was substituted.', '']
            continue
        lines += [f"Commit: `{r['commit']}`. Archive: {r['archiveBytes']:,} bytes; SHA-256 `{r['archiveSHA256']}`. License: {r['license']}.", '',
            '| Skill | Read scope / disposition |', '|---|---|']
        for s in r['skills']:
            lines.append(f"| {s['name']} | {s['status']} |")
        lines += ['', 'Fully read source paths:', '']
        lines += [f"- `{p['path']}` ({p['bytes']:,} bytes; hash in JSON)." for p in r['readCoverage']['fullTextFiles']]
        lines += ['', 'Reusable lessons and limitations:', '']
        for s in r['skills']:
            if not s['fullSkillRead']:
                continue
            lines += [f"- **{s['name']}**: {' '.join(s['appliedLearning'])}"]
            if s['userPreferenceConflicts']:
                lines += [f"  Project limits: {' '.join(s['userPreferenceConflicts'])}"]
        lines += ['']
    lines += ['## Official Sora availability', '',
        'No Sora skill was present at the pinned `openai/skills` HEAD. No removed/history copy or unofficial fork was installed.', '',
        '## Production learning priorities', '']
    lines += [f'- {s}' for s in report['productionPriorities']]
    lines += ['', 'Exact per-file hashes, repository receipts, dependency declarations, candidate roots and conflicts are in `group-c.json`. Files not explicitly listed as fully read remain archived for later reading.']
    (BASE/'group-c.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print(json.dumps(report['summary'], ensure_ascii=False))


if __name__ == '__main__':
    main()
