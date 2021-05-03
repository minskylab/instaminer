from core.core import InstaminerContext, InstaminerState
from os import remove
from pathlib import Path


def update_garbage_collector(ctx: InstaminerContext, post_id: str, path: str):
    if len(ctx.last_images) > ctx.max_saved_memory_images:
        drain_images(ctx)

    ctx.last_images[post_id] = path


def drain_images(ctx: InstaminerContext):
    previous_state = ctx.state

    ctx.state = InstaminerState.DRAINING
    for img, img_path in ctx.last_images.items():
        final_path = str(Path(img_path).resolve())
        remove(final_path)
        ctx.last_images.pop(img)

    ctx.state = previous_state
