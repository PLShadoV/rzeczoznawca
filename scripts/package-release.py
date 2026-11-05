#!/usr/bin/env python3
"""Create portable GitHub and static-hosting ZIPs without platform identity or secrets."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, re, subprocess, zipfile

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path, default=ROOT / 'releases')
args = parser.parse_args()
output = args.output.resolve()
output.mkdir(parents=True, exist_ok=True)
version = json.loads((ROOT / 'package.json').read_text())['version']
if not re.fullmatch(r'\d+\.\d+\.\d+(?:-[a-z0-9.-]+)?', version):
    raise SystemExit('Invalid release version')

try:
    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT, stderr=subprocess.DEVNULL).decode().split('\0')
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, stderr=subprocess.DEVNULL).decode().strip()
except (OSError, subprocess.CalledProcessError):
    exported_manifest = ROOT / 'RELEASE-MANIFEST.json'
    if not exported_manifest.exists():
        raise SystemExit('Use a Git checkout or an exported release containing RELEASE-MANIFEST.json.')
    previous = json.loads(exported_manifest.read_text())
    tracked = list(previous['files'])
    commit = previous.get('sourceCommit')

forbidden_parts = {'.git', '.openai', 'node_modules', '__pycache__', '.venv', 'releases'}
secret = re.compile(rb'art_v2_[A-Za-z0-9_-]{12,}|gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{25,}|-----BEGIN [A-Z ]*PRIVATE KEY-----')
files = {}
for name in sorted(set(tracked)):
    if not name:
        continue
    rel = Path(name)
    if rel.is_absolute() or '..' in rel.parts:
        raise SystemExit('Unsafe archive path: ' + name)
    if any(part in forbidden_parts for part in rel.parts):
        continue
    if tuple(rel.parts[:2]) == ('dist', 'downloads'):
        continue  # Hosted release archives are not part of the portable application.
    if tuple(rel.parts[:3]) == ('data', 'legal', 'sources'):
        continue
    if rel.name.startswith('.env') or rel.suffix.lower() in {'.pdf', '.zip', '.gz', '.pyc'}:
        continue
    if re.search(r'pracownia-postep|postep.*\.json$', rel.name, re.I):
        continue
    source = ROOT / rel
    if source.is_symlink():
        raise SystemExit('Symbolic links are not allowed in the portable release: ' + name)
    if not source.is_file():
        continue
    body = source.read_bytes()
    if secret.search(body):
        raise SystemExit('Potential credential detected; release aborted: ' + name)
    files[rel.as_posix()] = body

required = {'dist/index.html', 'dist/app.js', 'dist/enhancements.js', 'dist/questions.json', 'dist/legal-bases.json', '.github/workflows/pages.yml', 'README.md', 'docs/GITHUB.md', 'package.json', 'LICENSE', 'scripts/package-release.py'}
if not required.issubset(files):
    raise SystemExit('Missing tracked release files: ' + ', '.join(sorted(required-set(files))))

manifest = {
    'project': 'Pracownia Rzeczoznawcy',
    'version': version,
    'createdAt': datetime.now(timezone.utc).isoformat(timespec='seconds'),
    'sourceCommit': commit,
    'files': {name: hashlib.sha256(body).hexdigest() for name, body in files.items()},
}
manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2)+'\n').encode()
checksums = {**manifest['files'], 'RELEASE-MANIFEST.json': hashlib.sha256(manifest_bytes).hexdigest()}
sums_bytes = ''.join(f'{digest}  {name}\n' for name, digest in sorted(checksums.items())).encode()
base = 'pracownia-rzeczoznawcy'
repo_zip = output / f'{base}-github-v{version}.zip'
static_zip = output / f'{base}-strona-v{version}.zip'
with zipfile.ZipFile(repo_zip, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for name, body in files.items():
        archive.writestr(base + '/' + name, body)
    archive.writestr(base + '/RELEASE-MANIFEST.json', manifest_bytes)
    archive.writestr(base + '/SHA256SUMS.txt', sums_bytes)
with zipfile.ZipFile(static_zip, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for name, body in files.items():
        if name.startswith('dist/'):
            archive.writestr(name[5:], body)

# Validate what is actually distributed, not just the input checkout.
with zipfile.ZipFile(repo_zip) as archive:
    assert archive.testzip() is None
    names = archive.namelist()
    assert not any(any(p in forbidden_parts for p in Path(n).parts) for n in names)
    for name, digest in manifest['files'].items():
        assert hashlib.sha256(archive.read(base + '/' + name)).hexdigest() == digest, name
with zipfile.ZipFile(static_zip) as archive:
    assert archive.testzip() is None
    assert 'index.html' in archive.namelist() and 'questions.json' in archive.namelist()
    assert all(not n.startswith('/') and '..' not in Path(n).parts for n in archive.namelist())
for archive in [repo_zip, static_zip]:
    print(f'{archive.name}: {archive.stat().st_size:,} bytes')
(output / f'{base}-v{version}-SHA256SUMS.txt').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in [repo_zip, static_zip]))
print(f'Validated {len(files)} source files; platform identity, Git history, source PDFs, and credentials excluded.')
