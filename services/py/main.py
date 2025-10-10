import asyncio
from pathlib import Path

from src.infrastructure.di.bootstrap import Bootstrap

BASE_DIR = Path(__file__).resolve().parent


async def main() -> None:
    boostrap = Bootstrap()
    await boostrap.boot(BASE_DIR / "config.yml")


if __name__ == '__main__':
    asyncio.run(main())
