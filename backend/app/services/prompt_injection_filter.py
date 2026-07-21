from fastapi import HTTPException


class PromptInjectionFilter:
    """
    Detects common prompt injection attempts before
    sending user input to the LLM.
    """

    BLOCKED_PATTERNS = [
        "ignore previous instructions",
        "ignore all previous instructions",
        "forget previous instructions",
        "forget everything",
        "system prompt",
        "reveal your prompt",
        "show your prompt",
        "reveal hidden instructions",
        "developer instructions",
        "act as system",
        "act as developer",
        "pretend to be",
        "override instructions",
        "disable safety",
        "ignore safety",
        "repeat the hidden prompt",
        "print your instructions",
        "leak prompt",
        "jailbreak",
        "bypass safety",
        "bypass guardrails",
    ]

    @classmethod
    def validate(cls, message: str) -> None:
        """
        Raise an exception if the message appears to contain
        a prompt injection attempt.
        """

        # Normalize whitespace and convert to lowercase.
        # This prevents simple bypasses using multiple spaces,
        # tabs, or newlines.
        text = " ".join(message.lower().split())

        for pattern in cls.BLOCKED_PATTERNS:
            if pattern in text:
                raise HTTPException(
                    status_code=400,
                    detail="Prompt injection attempt detected.",
                )