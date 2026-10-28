"""Run the application checks explicitly configured by the operator."""
import json
import subprocess
import sys
from pathlib import Path

def run(config, root):
    checks = config.get('checks')
    if not isinstance(checks, list) or not checks:
        raise ValueError('Configure at least one application check in project.json.')
    if not all(isinstance(cmd, list) and cmd and all(isinstance(x, str) and x for x in cmd) for cmd in checks):
        raise ValueError('Checks must be non-empty argument arrays, not shell strings.')
    source = config.get('source_directory')
    if not isinstance(source, str) or not source:
        raise ValueError('Configure source_directory.')
    directory = (root / source).resolve()
    if not directory.is_dir():
        raise ValueError(f'Application directory not found: {directory}')
    timeout = config.get('timeout_seconds', 300)
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or timeout <= 0:
        raise ValueError('timeout_seconds must be positive.')
    for command in checks:
        print('Running: ' + json.dumps(command), flush=True)
        subprocess.run(command, cwd=directory, timeout=timeout, check=True, shell=False)

if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    try:
        run(json.loads((root / 'project.json').read_text()), root)
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print(f'Verification failed: {error}', file=sys.stderr)
        raise SystemExit(1)
