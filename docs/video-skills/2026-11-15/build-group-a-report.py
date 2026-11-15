"""Inventory archived sources and record the actual review scope. Does not install."""
import hashlib,json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SOURCES=ROOT/'sources'
FULL={
 'iart-ai/data-animation-skills':['animated-infographic','chart-animation'],
 'iart-ai/explainer-video-skills':['diagram-animation','explainer-video'],
 'iart-ai/motion-design-skills':['motion-art-direction','shot-composition','animation-principles','remotion-video'],
 'iart-ai/javascript-animation-skills':['soundtrack'],
 'iart-ai/b-roll-skills':['talking-head-b-roll'],
 'iart-ai/talking-head-skills':['talking-head'],
 'iart-ai/manim-skills':['manim'],
 'Vincentwei1021/video-shotcraft':['video-shotcraft'],
 'BAKUGOS1/video-studio':['video-studio'],
}
DETAILS={
 'animated-infographic':('Composition hierarchy and sequential numbers/connectors for one insight.',['Remotion','React','Node','ffmpeg; optional D3'],['Static-first infographic and2–3s held final frame are layout recipes, not permission to return to rejected slide films.','30–90s scope/3–5data points are examples, not a full-film limit.']),
 'chart-animation':('Maps numerical values to pixels and validates labels/scales.',['Remotion','React','Node','optional d3-scale'],['USD/en-US examples must become Vietnamese units/format.','Bar-race code needs implementation review; keyframed ranks must actually interpolate rather than jump.']),
 'diagram-animation':('Progressive cause/process reveal with active focus and stable color meaning.',['SVG/GSAP or Framer Motion/D3; Remotion for encoded video'],['Web rAF/CSS/GSAP loops must not be copied directly into frame-rendered video.','Reveal animations alone do not satisfy meaningful subject/state changes.']),
 'explainer-video':('Script first, one argument, stakes, mechanism and payoff.',['Remotion or After Effects','VO assets and timing'],['Explicit mandatory burned captions conflicts with user no-subtitle preference; override.','Fixed30–90s/product-solution formula cannot replace long-form economic chapters, brief relevant disclaimer or real-footage requirements.','140wpm/English word timing is estimate only; exact Vietnamese take timing leads.']),
 'motion-art-direction':('Hierarchy, intent and restraint before animation.',['No execution dependency; directs implementation skills'],['One personality/one wow and low-energy opening are heuristics; latest user wants strong hook, varied meaningful scenes and real footage with useful simulation.','Consistency must not become repetitive shots.']),
 'shot-composition':('One focal point, readable negative space and aspect-safe reflow.',['No execution dependency; optional implementation renderer'],['Thirds and single camera move are compositional defaults, not mandatory; composition must serve numerical/photographic meaning.','Do not blindly restack/crop real footage without inspecting actual output.']),
 'animation-principles':('Timing/easing/weight/arcs/overlap as implementation vocabulary.',['Tech agnostic'],['Three concurrent motion layers and beat quantization can create decoration; use only when they explain actual content.','Do not move narration or meaningful state changes merely to fit a beat.']),
 'soundtrack':('Offline Web Audio score and abrupt-loudness/beat checks.',['Node','Playwright/Chrome','ffmpeg','javascript-animation companion render.mjs','optional AI music paid provider'],['Code-generated score is NOT downloaded internet SFX required by latest user.','Picture-follows-music rule conflicts with speech-led exact narration; preserve narration and meaningful clause timing.','No change to selected OpenAI narration or approved music without task scope.']),
 'talking-head-b-roll':('Transcript-first semantic overlay/cover and phrase-level reveals.',['Node18+','playwright-core','Chrome','ffmpeg','local whisper.cpp or paid ElevenLabs transcription'],['Needs actual talking-head recording; current bread documentary has narration plus stock.','Never crop/move recording and show presenter opening/closing are specific workflow limits, not instructions for this documentary.','Six-frame visual lead is editorial default only; numerical facts/reveals stay on spoken anchor.']),
 'talking-head':('Paid photo/voice-to-presenter workflow with measured timings and recovery.',['Node22+','pnpm','ffmpeg/ffprobe','FAL_KEY','ELEVENLABS_API_KEY','fal MiniMax H3'],['Photos/reference speech upload to fal; samples/text to ElevenLabs. No uploads/provider calls authorized by skill installation.','Uses H3 generated speaking-shot audio rather than exact TTS; not guaranteed exact lip-sync.','Do not replace current OpenAI narration or add presenter/voice-clone automatically.']),
 'manim':('Formula transformations, graphs and explicit dependent-value updaters.',['Python','ManimCommunity','ffmpeg','LaTeX forMathTex','Pango forText'],['Use selectively for illustrative economics/math; do not replace real-footage film with blackboard formula slides.','An easing sentence contradicts animation-principles about slow end vs start; treat as prose defect, verify visual result.']),
 'remotion-video':('Generic frame-driven React rendering and props registration.',['Node','Remotion','React','zod','ffmpeg'],['Official Remotion skills already installed; archive this secondary duplicate rather than installing competing entrypoint.','Beat-driven whole-frame scale example can cause repeated pulses contrary to user preference.','useVideoConfig.durationInFrames is composition duration, not absolute frame index; code examples must be verified.']),
 'video-shotcraft':('124shot cards/150gallery variants, native editable product promo workflow and SFX source tooling.',['Node','Remotion','React','optionalThree/fiber/motion-blur','Python','ffmpeg/ffprobe','optionallibrosa','optionalWorkbench/CapCut export'],['Mode selection prompt/stop applies only when missing; existing autonomous authorization takes precedence.','Hard slow-opening≥3s, brandhold, tech-house BGM and product-launch finale reflect another user/project; not current bread-film direction.','Upstream demands voluntary author/social plugs and showcase invitation at delivery; do not inject into user video/response unsolicited.','Automatic Workbench opening and publisher helper are optional tooling; no publication/third-party messages from installation.','Template/demo branding and legacy music have separate per-file credits; do not import branding/audio automatically.','Archive containsworkbench/demosrc→../demos symlink; skipped extraction, archive preserved, not code execution.']),
 'video-studio':('Portable one-renderer orchestration, brief/shot purpose and representative preview.',['Node and chosenHyperFrames/Remotion','ffmpeg/ffprobe','optionalfal genmediaCLI+fundedaccount'],['Does not bundle engines or Shotcraft library and does not install providers itself.','Engine reference requests Remotion business license confirmation; existing engine choice/user authorization governs, no new automatic permission ritual.','Captions only when requested/needed; latest explicit no-subtitle preference wins.','Paid generation budget rules do not authorize a provider call during skill installation.']),
}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def front(text,key):
 m=re.search(r'^'+key+r':\s*(.+)$',text,re.M)
 return m.group(1).strip().strip('"\'') if m else None

repos=[];allskills=[]
for folder in sorted(SOURCES.iterdir()):
 receiptpath=folder/'receipt.json'
 if not receiptpath.exists():continue
 receipt=json.loads(receiptpath.read_text(encoding='utf-8'))
 repo=receipt['repo']
 if repo not in FULL and not repo.startswith('iart-ai/'):continue
 snap=folder/'snapshot'
 license_files=[p for p in snap.iterdir() if p.is_file() and p.name.upper().startswith(('LICENSE','COPYING'))]
 license_text='\n'.join(p.read_text(encoding='utf-8') for p in license_files)
 license_id='MIT' if 'MIT License' in license_text else 'Apache-2.0' if 'Apache License' in license_text else 'unconfirmed'
 entry={k:receipt.get(k) for k in ['repo','canonicalURL','commit','archive','archiveSHA256','archiveBytes','snapshot','fileCount','skippedSymlinks']}
 entry['license']=license_id
 entry['licenseEvidence']=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in license_files]
 entry['reviewMethod']='Archive/hash/license and full source tree inventory. Full SKILL reads are listed individually; rest frontmatter and instruction-keyword scan only. No repository code executed.'
 entry['skills']=[]
 for path in sorted(snap.rglob('SKILL.md')):
  text=path.read_text(encoding='utf-8');name=front(text,'name') or path.parent.name;full=name in FULL.get(repo,[])
  root=path.parent.relative_to(snap).as_posix()
  why,deps,conflicts=DETAILS.get(name,('Archived relevant motion/video family; not deeply reviewed this pass.',['Read SKILL and runtime references before use.'],[]))
  status='reviewed_install_candidate' if full else 'archived_read_on_demand'
  if name=='remotion-video':status='archived_duplicate_official_remotion_present'
  support=[p.relative_to(path.parent).as_posix() for p in path.parent.rglob('*') if p.is_file() and p!=path]
  flags=[]
  for num,line in enumerate(text.splitlines(),1):
   if re.search(r'(mandatory|must.*caption|caption.*mandatory|ask.*confirm|wait.*approval|FAL_KEY|ELEVENLABS|OPENAI|higgsfield|paid|credit|upload|publish|npx|pip install|curl|sudo)',line,re.I):
    flags.append({'line':num,'text':line[:500]})
  skill={'name':name,'description':front(text,'description'),'path':path.relative_to(ROOT).as_posix(),'skillRootRelative':root,'sha256':sha(path),'fullSkillRead':full,'reviewMethod':'full_SKILL_read' if full else 'frontmatter_plus_instruction_keyword_screen','status':status,'relevance':why,'dependencies':deps,'userPreferenceConflicts':conflicts,'supportingFileCount':len(support),'supportingFiles':support,'instructionFlags':flags,'proposedInstallName':('iart-'+name) if repo.startswith('iart-ai/') else name,'candidateInstallPath':root if status=='reviewed_install_candidate' else None}
  entry['skills'].append(skill);allskills.append({'repo':repo,'commit':receipt['commit'],**skill})
 repos.append(entry)

out={'schema':'video-skill-research-group-a/1','dateLocal':'2026-11-15','repositories':repos,'skills':allskills,'candidateInstallPaths':[{'repo':s['repo'],'ref':s['commit'],'path':s['candidateInstallPath'],'name':s['proposedInstallName'],'upstreamName':s['name']} for s in allskills if s['status']=='reviewed_install_candidate'],'summary':{'repositoriesArchived':len(repos),'iartPackRepositories':sum(r['repo'].startswith('iart-ai/') and r['repo']!='iart-ai/motion-skills' for r in repos),'iartSkillsArchived':sum(s['repo'].startswith('iart-ai/') for s in allskills),'fullSkillReads':sum(s['fullSkillRead'] for s in allskills),'installCandidates':sum(s['status']=='reviewed_install_candidate' for s in allskills),'archiveOnly':sum(s['status']!='reviewed_install_candidate' for s in allskills),'externalCodeExecuted':False,'globalSkillsModifiedByThisAgent':False},'readReferences':[
 {'repo':'BAKUGOS1/video-studio','paths':['references/direction.md','references/engines.md','references/sources.md','references/portability.md'],'method':'full_read'},
 {'repo':'Vincentwei1021/video-shotcraft','paths':['references/sound-design.md','references/sfx-sourcing.md'],'method':'full_read'},
 {'repo':'Vincentwei1021/video-shotcraft','paths':['references/aesthetic-rules.md'],'method':'opened_large_excerpt_with_output_truncation_not_full_read'},
 {'repo':'iart-ai/talking-head-skills','paths':['skills/talking-head/scripts/providers.mjs','skills/talking-head/scripts/pipeline.mjs'],'method':'keyword_context_scan_not_full_code_review'}
],'limits':['56iartskills archived; only12iartSKILL files fully read this pass, plusShotcraft/VideoStudio. No blanket claim all supporting code reviewed.','Repository licenses do not replace engine or bundled-media licenses.','No paid generation, dependency installation, renderer execution, third-party uploads or publication by this research agent.','Community examples and QA snippets are unexecuted guidance, not verified working integrations or aesthetic acceptance.','Newest user rules and workspaceAGENTS govern: content-first chapters, meaningful simulation, real relevant footage, no unwanted captions/branding, selectedOpenAIvoice, internetSFX, exactnarrationtiming.']}
(ROOT/'group-a.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['# Nhóm A — thư viện kỹ năng video và motion','',f'Đã lưu{len(repos)} repository, trong đó19pack iart có56SKILL. Đọc toàn12SKILL iart cộng Shotcraft vàVideoStudio; các file còn lại mới kiểm frontmatter/cụm chỉ dẫn, được giữ để đọc khi cần. Không chạy mã bên ngoài hoặc cài toàn cục.','', '## Bản đọc sâu và đề xuất cài','', '| Repo | Skill | Phạm vi | Quyết định |','|---|---|---|']
for s in allskills:
 if s['fullSkillRead']:lines.append(f"|{s['repo']}|{s['name']}|ToànSKILL; reference xemJSON|{s['status']}|")
lines+=['','## Những điểm phải điều chỉnh theo yêu cầu người dùng','']
for s in allskills:
 if s['fullSkillRead']:
  lines+=['- **'+s['name']+'**: '+'; '.join(s['userPreferenceConflicts'])]
lines+=['','## Nguồn và bằng chứng','', '| Repo | Commit | License | Sốskill |','|---|---|---|---|']
for r in repos:lines.append(f"|[{r['repo']}]({r['canonicalURL']})|`{r['commit']}`|{r['license']}|{len(r['skills'])}|")
lines+=['','`group-a.json` chứa pathcài, hasharchive/SKILL/license, danh sáchsupportingfiles, dependencies và cờchỉdẫn từngfile. Toànupstreamgiữnguyên trongsource.zip; snapshotbỏsymlinkworkbench/demosrc đểkhôngđitheoliênkếtkhigiảinén.','', 'Cài kỹnăng không phải huấn luyện trọng số, không chứng minh phim sẽ hay hơn. Học phải chuyển thành dànchương, môphỏng làm rõ cơchế, chọn footage đúng lời và kiểm bản dựng thực.']
(ROOT/'group-a.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps(out['summary'],ensure_ascii=False))
print(json.dumps(out['candidateInstallPaths'],ensure_ascii=False))
