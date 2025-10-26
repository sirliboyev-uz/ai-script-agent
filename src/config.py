"""Application configuration."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings."""

    # API Keys
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # AI Provider Selection
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "openai")  # "openai" or "anthropic"

    # Application
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite+aiosqlite:///./data/scripts.db"
    )

    # Claude Configuration
    CLAUDE_MODEL: str = "claude-3-5-sonnet-20241022"

    # OpenAI Configuration
    OPENAI_MODEL: str = "gpt-4o"

    # Common Configuration
    MAX_TOKENS: int = 4096

    # Authentication
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production-min-32-chars")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Project paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"

    def validate(self) -> None:
        """Validate required settings."""
        if self.AI_PROVIDER == "anthropic" and not self.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY is required when using Anthropic provider")

        if self.AI_PROVIDER == "openai" and not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required when using OpenAI provider")

        if self.AI_PROVIDER not in ["openai", "anthropic"]:
            raise ValueError("AI_PROVIDER must be 'openai' or 'anthropic'")

        # Ensure data directory exists
        self.DATA_DIR.mkdir(exist_ok=True)

settings = Settings()
