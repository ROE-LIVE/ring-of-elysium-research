"""Проверяет только отслеживаемый Git состав; не открывает исключённые private-файлы."""
from pathlib import Path
import json
import hashlib
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DENIED = {'.key', '.pem', '.pfx', '.exe', '.dll', '.bin', '.zip', '.7z', '.rar', '.dmp', '.pcap', '.pcapng'}


def main():
    paths = subprocess.check_output(['git', '-C', str(ROOT), 'ls-files', '-z']).decode().split('\0')
    paths = [p for p in paths if p]
    if not paths:
        raise SystemExit('Сначала git add: нет отслеживаемых файлов')
    errors = []
    for name in paths:
        path = ROOT/name
        if (path.is_symlink() or path.suffix.lower() in DENIED or
                name.startswith(('runtime/', 'runs/', 'reports/', '.tools/')) or
                name.startswith('private/') and name != 'private/README.md'):
            errors.append(f'Запрещённый путь: {name}')
            continue
        if path.stat().st_size > 10*1024*1024:
            errors.append(f'Слишком большой файл: {name}')
            continue
        text = path.read_text(encoding='utf-8-sig')
        if re.search(r'a\.Data\s*=\s*"[0-9a-fA-F\s]+"\.ToArr', text):
            errors.append(f'Встроенный CK payload: {name}')
        if '-----BEGIN ' + 'PRIVATE KEY-----' in text:
            errors.append(f'PEM private key: {name}')
    manifest_path = ROOT/'SOURCE-MANIFEST.json'
    if manifest_path.is_file():
        for row in json.loads(manifest_path.read_text()):
            name = row['path']
            if name not in paths:
                errors.append('Manifest ссылается на неотслеживаемый путь: '+name)
                continue
            if hashlib.sha256((ROOT/name).read_bytes()).hexdigest() != row['sha256']:
                errors.append('SHA не совпала: '+name)
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'OK: {len(paths)} отслеживаемых текстовых файлов; запрещённые пути/CK/PEM не найдены.')
    print('Это проверка состава и хешей, а не полная гарантия отсутствия любых секретов или проверка прав.')


if __name__ == '__main__':
    main()
