from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data: Path
    unzip_dir: Path

@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    status_file_dir: Path
    req_files: list

@dataclass(frozen=True)
class ModelTrainerConfig:
    model: str
    epochs: int
    batch: int
    imgsz: int