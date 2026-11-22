"""Check the explicit package inventory; update hashes only after reviewing changes."""
import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / 'SHA256SUMS.txt'
ROOT_FILES = (
    '.gitattributes', '.gitignore', 'FYP_SETUP_CHECKLIST.md',
    'README.md', 'CITATION.cff',
    'requirements.txt', 'requirements-lock.txt', 'quick_check.py',
    'run_supplement.py', 'verify_manifest.py',
)


def inventory():
    names = set(ROOT_FILES)
    for directory, pattern in (('docs', '*.md'), ('scripts', '*.py'), ('expected', '*.json')):
        names.update(p.relative_to(ROOT).as_posix() for p in (ROOT / directory).glob(pattern))
    return sorted(names)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--update', action='store_true', help='replace hashes after an intentional package change')
    args = parser.parse_args()
    names = inventory()
    if args.update:
        content = ''.join(f'{hashlib.sha256((ROOT / name).read_bytes()).hexdigest()}  {name}\n' for name in names)
        MANIFEST.write_text(content, encoding='utf-8', newline='\n')
    entries = {}
    for line in MANIFEST.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        digest, name = line.split('  ', 1)
        if name in entries:
            raise ValueError(f'Duplicate manifest entry: {name}')
        if name not in names:
            raise ValueError(f'Unexpected manifest path: {name}')
        entries[name] = digest
    if set(entries) != set(names):
        raise ValueError(f'Missing manifest entries: {sorted(set(names) - set(entries))}')
    for name, digest in entries.items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != digest:
            raise ValueError(f'SHA-256 mismatch: {name}')
    print(f'PASS SHA-256: {len(entries)} package files; exact inventory coverage (manifest excludes itself).')


if __name__ == '__main__':
    main()
