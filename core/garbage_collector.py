from os import listdir, remove, unlink
from os.path import isdir, isfile, islink, join
from pathlib import Path
from shutil import rmtree

from loguru import logger

from .context import InstaminerContext, InstaminerState


def update_garbage_collector(ctx: InstaminerContext, post_id: str, path: str):
    if len(ctx.last_images) > ctx.max_saved_memory_images-1:
        drain_images(ctx)

    ctx.last_images[post_id] = path


def drain_images(ctx: InstaminerContext):
    logger.warning("cleaning files data directory")

    previous_state = ctx.state
    ctx.state = InstaminerState.DRAINING

    to_delete = ctx.last_images.values()

    for img_path in to_delete:
        try:
            final_path = str(Path(img_path).resolve())
            remove(final_path)
        except BaseException as e:
            logger.error(f"error at try to remove '{final_path}', [error={e}]")

    ctx.last_images.clear()
    ctx.state = previous_state


def purge_all_data_dir(ctx: InstaminerContext):
    data_dir = str(Path(ctx.data_dir).resolve())

    for filename in listdir(data_dir):

        file_path = join(data_dir, filename)
        try:
            if isfile(file_path) or islink(file_path):
                unlink(file_path)
            elif isdir(file_path):
                rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
