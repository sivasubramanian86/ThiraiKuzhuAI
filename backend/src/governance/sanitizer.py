"""Telemetry sanitization, prompt injection defense, and execution circuit breakers.

Hardens Thirai Kuzhu AI against prompt injection, credential exposure,
and denial-of-wallet runaway loops in enterprise studio pipelines.
Follows PEP 257 Google-style docstrings.
"""

import re


def sanitize_telemetry_for_prompt(raw_text: str, max_chars: int = 4000) -> str:
    """Strips potential prompt injections, credentials, and actor PII from telemetry strings.

    Args:
        raw_text: Raw unvalidated log snippet, PromQL output, or trace payload.
        max_chars: Maximum character budget to enforce.

    Returns:
        str: Cleaned, redacted string safe for LLM context injection.
    """
    if not raw_text:
        return ""

    # 1. Neutralize Prompt Injections and Jailbreak delimiters
    injection_pattern = (
        r"(?i)(ignore\s+(all\s+)?previous\s+instructions|"
        r"system\s+prompt|admin\s+override|jailbreak|"
        r"<\|im_start\|>|<\|im_end\|>|assistant:)"
    )
    cleaned = re.sub(injection_pattern, "[REDACTED_PROMPT_INJECTION]", raw_text)

    # 2. Mask Credentials, Tokens, Bearer Keys, and Passwords
    cred_pattern = (
        r"(?i)(bearer\s+[a-zA-Z0-9\-\._~+/]+=*|"
        r"key=[a-zA-Z0-9_\-]+|glsa_[a-zA-Z0-9_\-]+|"
        r"password=\S+|secret=[a-zA-Z0-9_\-]+)"
    )
    cleaned = re.sub(cred_pattern, "[REDACTED_CREDENTIAL]", cleaned)

    # 3. Mask PII: Email addresses and phone numbers
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    cleaned = re.sub(email_pattern, "[REDACTED_EMAIL]", cleaned)

    phone_pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    cleaned = re.sub(phone_pattern, "[REDACTED_PHONE]", cleaned)

    # 4. Enforce strict character budget
    return cleaned[:max_chars]


class ExecutionCircuitBreaker:
    """Monitors tool calls and token expenditures to prevent runaway loops."""

    def __init__(
        self,
        max_tool_calls: int = 8,
        max_token_budget: int = 16000,
    ) -> None:
        """Initializes circuit breaker with studio quota limits.

        Args:
            max_tool_calls: Maximum allowable MCP tool queries per mission.
            max_token_budget: Maximum total token expenditure before tripping.
        """
        self.max_tool_calls = max_tool_calls
        self.max_token_budget = max_token_budget
        self.current_tool_calls = 0
        self.accumulated_tokens = 0
        self._tripped = False
        self._trip_reason = ""

    def record_tool_invocation(self, tool_name: str) -> bool:
        """Records an agent tool execution and checks against max invocation quota.

        Args:
            tool_name: Name of tool being invoked.

        Returns:
            bool: True if execution is permitted, False if circuit tripped.
        """
        if self._tripped:
            return False

        self.current_tool_calls += 1
        if self.current_tool_calls > self.max_tool_calls:
            self._tripped = True
            self._trip_reason = (
                f"Circuit breaker tripped: Tool call limit exceeded "
                f"({self.current_tool_calls} > {self.max_tool_calls}) on {tool_name}."
            )
            return False
        return True

    def record_tokens(self, tokens_used: int) -> bool:
        """Records token consumption and verifies against mission token budget.

        Args:
            tokens_used: Number of tokens consumed in step.

        Returns:
            bool: True if budget remains intact, False if circuit tripped.
        """
        if self._tripped:
            return False

        self.accumulated_tokens += tokens_used
        if self.accumulated_tokens > self.max_token_budget:
            self._tripped = True
            self._trip_reason = (
                f"Circuit breaker tripped: Token budget exceeded "
                f"({self.accumulated_tokens} > {self.max_token_budget})."
            )
            return False
        return True

    def is_tripped(self) -> bool:
        """Returns whether circuit breaker is in a tripped state.

        Returns:
            bool: True if execution is blocked, False otherwise.
        """
        return self._tripped

    def get_trip_reason(self) -> str:
        """Returns human-readable explanation of why circuit breaker tripped.

        Returns:
            str: Explanation message or empty string if healthy.
        """
        return self._trip_reason
