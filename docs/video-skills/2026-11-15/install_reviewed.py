"""Install reviewed, pinned snapshots using the official skill-installer helpers.

Only this local wrapper runs. Downloaded scripts and runtime installers do not.
The official helper validates and copies each skill; its download stage reuses
the hash-verified archive already saved for review.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import shutil
import sys
import yaml

BASE = Path(__file__).resolve().parent
DEST = Path('C:/Users/tyranno/.codex/skills')
HELPER = DEST / '.system/skill-installer/scripts/install-skill-from-github.py'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def install(manifest):
    sys.path.insert(0, str(HELPER.parent))
    spec = importlib.util.spec_from_file_location('official_skill_installer', HELPER)
    helper = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = helper
    spec.loader.exec_module(helper)
    receipts = []
    for item in manifest:
        snapshot = Path(item['snapshot']).resolve()
        archive = Path(item['archive']).resolve()
        assert archive.is_relative_to(BASE), 'Archive outside source library'
        assert sha(archive) == item['archiveSHA256'], 'Archive hash changed'
        assert snapshot.is_relative_to(BASE / 'sources'), 'Snapshot outside source library'
        source = snapshot / item['path']
        assert sha(source / 'SKILL.md') == item['skillSHA256'], 'Reviewed SKILL changed'
        alias = item['alias']
        assert re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}', alias), 'Invalid alias'
        target = DEST / alias
        if target.exists():
            previous = target / '_codex_source.json'
            if previous.exists() and json.loads(previous.read_text(encoding='utf-8')).get('commit') == item['commit']:
                receipts.append(json.loads(previous.read_text(encoding='utf-8')))
                continue
            raise ValueError(f'Existing skill preserved, choose another alias: {alias}')
        # Reuse the official validation/copy/CLI, replacing only network acquisition.
        helper._prepare_repo = lambda source, method, tmp_dir: str(snapshot)
        status = helper.main(['--repo', item['repo'], '--ref', item['commit'], '--path', item['path'],
                              '--name', alias, '--dest', str(DEST), '--method', 'download'])
        if status:
            raise ValueError(f'Official installer rejected {alias}')
        installed_md = target / 'SKILL.md'
        text = installed_md.read_text(encoding='utf-8-sig')
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.S)
        if not match:
            raise ValueError(f'No frontmatter: {alias}')
        meta = yaml.safe_load(match.group(1))
        original_meta = dict(meta)
        meta['name'] = alias
        description = item.get('description', meta.get('description', ''))
        description = re.sub(r'\s+', ' ', str(description)).strip()
        if len(description) > 1024:
            description = description[:1021] + '...'
        if not description:
            raise ValueError(f'No description: {alias}')
        meta['description'] = description
        changed = meta != original_meta
        if changed:
            shutil.copy2(installed_md, target / 'SKILL.upstream.md')
            installed_md.write_text('---\n' + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False).strip() +
                                    '\n---\n\n' + text[match.end():], encoding='utf-8')
        # Preserve the upstream legal notices even when the skill lives in a subfolder.
        for name in ('LICENSE', 'LICENSE.md', 'LICENSE.txt', 'COPYING'):
            license_path = snapshot / name
            if license_path.exists():
                shutil.copy2(license_path, target / ('UPSTREAM_' + name))
        receipt = {**item, 'installedPath': str(target), 'installedSkillSHA256': sha(installed_md),
                   'metadataAdjusted': changed, 'upstreamBodyPreserved': True,
                   'method': 'official helper validation/copy with verified cached archive',
                   'officialInstallerSHA256': sha(HELPER), 'externalCodeExecuted': False,
                   'runtimeDependenciesInstalled': False, 'runtimeEndToEndTested': False,
                   'available': 'next_turn'}
        (target / '_codex_source.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
        receipts.append(receipt)
    return receipts


if __name__ == '__main__':
    manifest_file = Path(sys.argv[1])
    receipts = install(json.loads(manifest_file.read_text(encoding='utf-8')))
    out = manifest_file.with_name(manifest_file.stem + '-installed.json')
    out.write_text(json.dumps(receipts, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'INSTALLED_VERIFIED {len(receipts)}')
