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
    save_path: Path
    epochs: int
    batch: int
    imgsz: int

@dataclass(frozen=True)
class MlflowConfig:
    mlflow_uri: str
    experiment_name: str
    model_name: str