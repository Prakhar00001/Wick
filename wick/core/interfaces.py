from typing import Protocol, runtime_checkable
from .models import Example, TargetResult, EvaluationResult

@runtime_checkable
class EvalTarget(Protocol):
    """
    Protocol for evaluating any LLM system (single-call, RAG, Agent).
    """
    async def run(self, example: Example, *, trace: bool = False) -> TargetResult:
        ...

@runtime_checkable
class Scorer(Protocol):
    """
    Protocol for scoring a TargetResult against an Example.
    """
    @property
    def name(self) -> str: ...

    async def score(self, example: Example, result: TargetResult) -> float | dict[str, float]:
        ...