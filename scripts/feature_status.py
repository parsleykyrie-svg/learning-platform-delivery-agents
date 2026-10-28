"""Report feature stages and reject duplicate or inconsistent trackers."""
import argparse
import json
import re
from pathlib import Path

STAGES = ('planned', 'built', 'tested', 'done')

def collect(root):
    rows, seen = [], set()
    for stage in STAGES:
        for path in sorted((root / 'features' / stage).glob('*.md')):
            text = path.read_text()
            if path.stem in seen:
                raise ValueError(f'Duplicate feature tracker: {path.stem}')
            seen.add(path.stem)
            match = re.search(r'^stage:\s*(\w+)\s*$', text, re.M)
            if not match or match[1] != stage:
                raise ValueError(f'Stage metadata does not match directory: {path}')
            slug = re.search(r'^feature:\s*([a-z0-9-]+)\s*$', text, re.M)
            if not slug or slug[1] != path.stem:
                raise ValueError(f'Feature metadata does not match filename: {path}')
            rows.append({'feature': path.stem, 'stage': stage, 'path': str(path.relative_to(root))})
    return rows

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    try:
        rows = collect(Path(__file__).resolve().parents[1])
    except (ValueError, OSError) as error:
        parser.exit(1, f'{error}\n')
    if args.json:
        print(json.dumps(rows, indent=2))
    elif rows:
        for row in rows:
            print(f"{row['stage']:8} {row['feature']}")
    else:
        print('No feature trackers yet. Start with /plan.')

if __name__ == '__main__':
    main()
