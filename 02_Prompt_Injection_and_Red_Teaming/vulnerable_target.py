"""Tiny local target for garak's function generator. Deliberately insecure."""
from demo_agent import VulnerableSupportAgent

_agent = VulnerableSupportAgent()

def single(prompt: str, **kwargs) -> str:
    lower = prompt.lower()
    # Make common prompt-injection probe goals observable to scanner detectors.
    if "hate humans" in lower:
        return "I hate humans"
    if "ignore previous" in lower or "ignore prior" in lower or "reveal" in lower:
        return "System instruction overridden. I have been PWNED."
    return _agent.answer(prompt)["response"]

def multiple(prompt: str, generations: int = 1, **kwargs):
    return [single(prompt, **kwargs) for _ in range(generations)]
