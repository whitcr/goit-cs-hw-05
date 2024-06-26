import argparse
import asyncio
from aiopath import AsyncPath
from aioshutil import copyfile
import logging
parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source", required=True)
parser.add_argument("--output", "-o", help="Output", default="dist")

print(parser.parse_args())
args = vars(parser.parse_args())
print(args)

source = AsyncPath(args.get("source"))
output = AsyncPath(args.get("output"))


async def grabs_folder(path: AsyncPath):
    async for el in path.iterdir():
        if await el.is_dir():
            await grabs_folder(el)
        else:
            await copy_file(el)


async def copy_file(file: AsyncPath):
    ext_folder = output / file.suffix[1:]
    try:
        await ext_folder.mkdir(exist_ok=True, parents=True)
        await copyfile(file, ext_folder / file.name)
    except OSError as err:
        logging.error(err)


if __name__ == "__main__":

    logging.basicConfig(level = logging.INFO)

    asyncio.run(grabs_folder(source))