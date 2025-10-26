"""Input validation utilities."""
from typing import Optional
from src.utils.exceptions import ValidationError


def validate_topic(topic: str) -> None:
    """
    Validate topic input.

    Args:
        topic: Topic string to validate

    Raises:
        ValidationError: If validation fails
    """
    if not topic or len(topic.strip()) < 5:
        raise ValidationError("Topic must be at least 5 characters long")

    if len(topic) > 500:
        raise ValidationError("Topic cannot exceed 500 characters")

    # Check for common spam patterns
    spam_patterns = ["http://", "https://", "www.", "buy now", "click here"]
    topic_lower = topic.lower()
    for pattern in spam_patterns:
        if pattern in topic_lower:
            raise ValidationError(f"Topic contains invalid pattern: {pattern}")


def validate_style(style: str) -> None:
    """
    Validate style input.

    Args:
        style: Style string to validate

    Raises:
        ValidationError: If validation fails
    """
    valid_styles = ["educational", "entertaining", "inspirational"]
    if style not in valid_styles:
        raise ValidationError(f"Style must be one of: {', '.join(valid_styles)}")


def validate_duration(duration: str) -> None:
    """
    Validate duration input.

    Args:
        duration: Duration string to validate

    Raises:
        ValidationError: If validation fails
    """
    valid_durations = [
        "5-8 minutes",
        "8-10 minutes",
        "10-15 minutes",
        "15-20 minutes",
        "20-30 minutes"
    ]
    if duration not in valid_durations:
        raise ValidationError(f"Duration must be one of: {', '.join(valid_durations)}")


def validate_research_depth(depth: str) -> None:
    """
    Validate research depth input.

    Args:
        depth: Depth string to validate

    Raises:
        ValidationError: If validation fails
    """
    valid_depths = ["quick", "medium", "deep"]
    if depth not in valid_depths:
        raise ValidationError(f"Research depth must be one of: {', '.join(valid_depths)}")


def validate_brand_voice(brand_voice: Optional[str]) -> None:
    """
    Validate brand voice input.

    Args:
        brand_voice: Brand voice string to validate

    Raises:
        ValidationError: If validation fails
    """
    if brand_voice and len(brand_voice) > 1000:
        raise ValidationError("Brand voice cannot exceed 1000 characters")
