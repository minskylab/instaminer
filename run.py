from asyncio import run

from dotenv import load_dotenv

from core.core import new_context
from core.looper import looper
from load import default_context_options
from settings.env import load_search_configuration
from loguru import logger


async def main():
    load_dotenv()

    opts = default_context_options()
    print(opts)
    ctx = await new_context(opts)

    # search = load_search_configuration()

    # logger.info(search)

    # await looper(ctx, search)

run(main())
