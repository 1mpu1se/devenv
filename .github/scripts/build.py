import zipfile
from os import environ as env
from pathlib import Path

ITEMS = [
    './docker-compose.yaml',
    './README.md',
]


def main() -> None:
    name = '{}-{}'.format(
        env.get('NAME', 'artifact'),
        env.get('VERSION', 'local')
    )

    out_dir = Path('./.build/')
    out_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(out_dir / f'{name}.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        for item in ITEMS:
            p = Path(item)
            if not p.is_file():
                raise Exception(f'File {p.as_posix()} not found')
            z.write(p, name / p)


if __name__ == '__main__':
    main()
