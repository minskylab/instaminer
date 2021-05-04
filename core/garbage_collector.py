from .core import InstaminerContext, InstaminerState
from os import remove
from pathlib import Path
from loguru import logger


def update_garbage_collector(ctx: InstaminerContext, post_id: str, path: str):
    if len(ctx.last_images) > ctx.max_saved_memory_images-1:
        drain_images(ctx)

    ctx.last_images[post_id] = path


def drain_images(ctx: InstaminerContext):
    logger.warning("cleaning files data directory")

    previous_state = ctx.state

    ctx.state = InstaminerState.DRAINING

    to_delete = ctx.last_images.values()
    # logger.info(to_delete)
    for img_path in to_delete:
        try:
            final_path = str(Path(img_path).resolve())
            remove(final_path)
        except BaseException as e:
            logger.error(f"error at try to remove '{final_path}', [error={e}]")

    ctx.last_images.clear()
    ctx.state = previous_state
