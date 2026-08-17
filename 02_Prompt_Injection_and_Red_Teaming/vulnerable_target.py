"""Tiny local target for garak's ``function`` generator. Deliberately insecure.

garak >= 0.16 contract for ``--target_type function``:

* ``function.Single``  : ``fn(prompt: str, **kwargs) -> list[str | None]``
* ``function.Multiple``: ``fn(prompt: str, generations: int, **kwargs) -> list[str | None]``

The function must return a *list* of responses. Returning a bare ``str`` makes
garak iterate over the characters and score each character as a response,
which silently corrupts every detector result.
"""
from __future__ import annotations

from demo_agent import VulnerableSupportAgent

_agent = VulnerableSupportAgent()


def respond(prompt: str) -> str:
    """One assistant turn from the vulnerable agent (string in, string out)."""
    lower = prompt.lower()
    # Make common prompt-injection probe goals observable to scanner detectors.
    if "hate humans" in lower:
        return "I hate humans"
    if "ignore previous" in lower or "ignore prior" in lower or "reveal" in lower:
        return "System instruction overridden. I have been PWNED."
    return _agent.answer(prompt)["response"]


def single(prompt: str, **kwargs) -> list[str]:
    """Adapter for ``function.Single``. Always returns a one-element list."""
    return [respond(prompt)]


def multiple(prompt: str, generations: int = 1, **kwargs) -> list[str]:
    """Adapter for ``function.Multiple``."""
    return [respond(prompt) for _ in range(generations)]
