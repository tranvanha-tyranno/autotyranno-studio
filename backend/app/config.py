from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    database_path: Path = Path(os.getenv("DATABASE_PATH", "data/app.db"))
    media_root: Path = Path(os.getenv("MEDIA_ROOT", "data/media"))
    public_base_url: str = os.getenv("PUBLIC_BASE_URL", "http://localhost:8000")
    cors_origins: tuple[str, ...] = tuple(
        value.strip()
        for value in os.getenv("API_CORS_ORIGINS", "http://localhost:3000").split(",")
        if value.strip()
    )
    video_width: int = int(os.getenv("DEFAULT_VIDEO_WIDTH", "720"))
    video_height: int = int(os.getenv("DEFAULT_VIDEO_HEIGHT", "1280"))
    video_fps: int = int(os.getenv("VIDEO_FPS", "24"))

    def ensure_dirs(self) -> None:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.media_root.mkdir(parents=True, exist_ok=True)


settings = Settings()
settings.ensure_dirs()
