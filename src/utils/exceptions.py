"""Custom exceptions."""


class ScriptGenerationError(Exception):
    """Raised when script generation fails."""
    pass


class ResearchError(Exception):
    """Raised when research phase fails."""
    pass


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


class ConfigurationError(Exception):
    """Raised when configuration is invalid."""
    pass
