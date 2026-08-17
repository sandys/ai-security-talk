"""garak ``function`` target wrapping the *constrained* workshop agent.

Same contract as ``vulnerable_target.py`` (must return a ``list`` of strings).
Point garak at both targets and compare attack-success rates: the scan is only
meaningful as a *diff* between two versions of the same system.
"""
from __future__ import annotations

from demo_agent import SecureSupportAgent

_agent = SecureSupportAgent(max_auto_refund=500)


def single(prompt: str, **kwargs) -> list[str]:
    return [_agent.answer(prompt)["response"]]


def multiple(prompt: str, generations: int = 1, **kwargs) -> list[str]:
    return [_agent.answer(prompt)["response"] for _ in range(generations)]
