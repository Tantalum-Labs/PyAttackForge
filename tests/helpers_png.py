from pathlib import Path
from typing import Tuple

from PIL import Image


def make_png(path: Path, width: int, height: int, color: Tuple[int, int, int] = (120, 60, 230)) -> Path:
    """Create a deterministic PNG to exercise binary upload paths."""
    img = Image.new("RGB", (width, height), color=color)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, format="PNG", optimize=True)
    return path
