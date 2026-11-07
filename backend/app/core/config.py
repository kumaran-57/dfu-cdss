"""
Application configuration for DFU-XAI.
Uses environment variables with secure defaults for local development.
"""

import os
import json
from typing import List
from pydantic import BaseModel, Field

class Settings(BaseModel):
    APP_NAME: str = Field(default="DFU-XAI Research Decision Support")
    APP_VERSION: str = Field(default="1.0.0")
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=True)
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)

    # Security
    SECRET_KEY: str = Field(
        default="development-insecure-secret-key-change-in-production-32chars"
    )
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=120)

    # Database
    DATABASE_URL: str = Field(default="sqlite:///./dfu_xai.db")

    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"]
    )

    # File Upload & Storage
    UPLOAD_DIR: str = Field(default="./data/uploads")
    MAX_UPLOAD_SIZE_MB: int = Field(default=25)

    # Clinical Safety Boundary Notice
    CLINICAL_DISCLAIMER: str = Field(
        default=(
            "Research decision-support prototype. Not for autonomous diagnosis or treatment. "
            "Clinical decisions must be made by qualified healthcare professionals."
        )
    )

    @classmethod
    def load_from_env(cls) -> "Settings":
        env = os.environ
        cors_raw = env.get("CORS_ORIGINS")
        if cors_raw:
            try:
                cors_list = json.loads(cors_raw)
            except Exception:
                cors_list = [c.strip() for c in cors_raw.split(",") if c.strip()]
        else:
            cors_list = ["http://localhost:3000", "http://127.0.0.1:3000"]

        return cls(
            APP_NAME=env.get("APP_NAME", "DFU-XAI Research Decision Support"),
            APP_VERSION=env.get("APP_VERSION", "1.0.0"),
            ENVIRONMENT=env.get("ENVIRONMENT", "development"),
            DEBUG=env.get("DEBUG", "true").lower() in ("true", "1", "yes"),
            HOST=env.get("HOST", "0.0.0.0"),
            PORT=int(env.get("PORT", 8000)),
            SECRET_KEY=env.get(
                "SECRET_KEY",
                "development-insecure-secret-key-change-in-production-32chars",
            ),
            ALGORITHM=env.get("ALGORITHM", "HS256"),
            ACCESS_TOKEN_EXPIRE_MINUTES=int(
                env.get("ACCESS_TOKEN_EXPIRE_MINUTES", 120)
            ),
            DATABASE_URL=env.get("DATABASE_URL", "sqlite:///./dfu_xai.db"),
            CORS_ORIGINS=cors_list,
            UPLOAD_DIR=env.get("UPLOAD_DIR", "./data/uploads"),
            MAX_UPLOAD_SIZE_MB=int(env.get("MAX_UPLOAD_SIZE_MB", 25)),
            CLINICAL_DISCLAIMER=env.get(
                "CLINICAL_DISCLAIMER",
                (
                    "Research decision-support prototype. Not for autonomous diagnosis or treatment. "
                    "Clinical decisions must be made by qualified healthcare professionals."
                ),
            ),
        )

settings = Settings.load_from_env()
