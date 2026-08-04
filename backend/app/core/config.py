from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DATABASE_URL: str

    MODEL_PATH: str = "models/yolo11n.pt"

    CONFIDENCE_THRESHOLD: float = 0.5

    LINE_Y: int = 300

    CAMERA_ID: str = "Gate-1"

    TRACKER_CONFIG: str = "bytetrack.yaml"

    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()