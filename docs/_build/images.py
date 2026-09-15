"""Web-sized copies of the repository's images for the site's galleries.

The originals stay where they are and are linked at full resolution; the site
shows a WebP copy scaled down to fit a bounding square. Nothing is ever scaled
up. An existing copy newer than its original is reused rather than re-encoded.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageOps

WEBP_QUALITY = 82
WEBP_METHOD = 6
TRANSPARENT_MODES = frozenset({"RGBA", "LA", "P", "PA"})

_UNSAFE = re.compile(r"[^a-z0-9]+")


@dataclass(frozen=True, slots=True)
class Thumb:
    url: str
    width: int
    height: int


class Thumbnails:
    def __init__(self, repo: Path, docs: Path, url_prefix: str) -> None:
        self._repo = repo
        self._docs = docs
        self._prefix = url_prefix
        self._made: dict[tuple[str, int], Thumb] = {}
        self.written: set[str] = set()

    def get(self, repo_path: str, max_edge: int) -> Thumb:
        key = (repo_path, max_edge)
        if key in self._made:
            return self._made[key]
        stem = _UNSAFE.sub("-", Path(repo_path).with_suffix("").as_posix().lower())
        url = f"{self._prefix}{stem.strip('-')}-{max_edge}.webp"
        source = self._repo / repo_path
        dest = self._docs / url
        if dest.exists() and dest.stat().st_mtime >= source.stat().st_mtime:
            with Image.open(dest) as existing:
                width, height = existing.size
        else:
            width, height = self._encode(source, dest, max_edge)
        thumb = Thumb(url, width, height)
        self._made[key] = thumb
        self.written.add(url)
        return thumb

    @staticmethod
    def _encode(source: Path, dest: Path, max_edge: int) -> tuple[int, int]:
        with Image.open(source) as original:
            image = ImageOps.exif_transpose(original)
            mode = "RGBA" if image.mode in TRANSPARENT_MODES else "RGB"
            image = image.convert(mode)
            image.thumbnail((max_edge, max_edge), Image.Resampling.LANCZOS)
            dest.parent.mkdir(parents=True, exist_ok=True)
            image.save(dest, "WEBP", quality=WEBP_QUALITY, method=WEBP_METHOD)
            return image.size
