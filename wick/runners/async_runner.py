import asyncio
import logging
from typing import List, Sequence
from tenacity import retry, stop_after_attempt, wait_exponential

from wick.core.models import Example, EvaluationResult, Score, TargetResult
from wick.core.interfaces import EvalTarget, Scorer

logger = logging.getLogger("wick.runner")

class AsyncEvalRunner:
    def __init__(
        self, 
        target: EvalTarget, 
        scorers: Sequence[Scorer], 
        concurrency: int = 10
    ):
        self.target = target
        self.scorers = scorers
        self.semaphore = asyncio.Semaphore(concurrency)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def _safe_run_target(self, example: Example) -> TargetResult:
        return await self.target.run(example, trace=True)

    async def _evaluate_single(self, example: Example) -> EvaluationResult:
        async with self.semaphore:
            try:
                target_result = await self._safe_run_target(example)
                
                scores: List[Score] = []
                all_passed = True
                
                # Run scorers concurrently
                score_tasks = [scorer.score(example, target_result) for scorer in self.scorers]
                score_results = await asyncio.gather(*score_tasks, return_exceptions=True)
                
                for scorer, result in zip(self.scorers, score_results):
                    if isinstance(result, Exception):
                        logger.error(f"Scorer {scorer.name} failed on example {example.id}: {result}")
                        scores.append(Score(name=scorer.name, value=0.0, passed=False, reasoning=str(result)))
                        all_passed = False
                    else:
                        # Simplified for scalar returns; dict returns can be expanded
                        val = float(result) 
                        passed = val >= 0.8 # Configurable threshold in real app
                        scores.append(Score(name=scorer.name, value=val, passed=passed))
                        if not passed:
                            all_passed = False
                            
                return EvaluationResult(
                    example=example,
                    target_result=target_result,
                    scores=scores,
                    success=all_passed
                )
            except Exception as e:
                logger.error(f"Target execution failed for {example.id}: {e}")
                return EvaluationResult(
                    example=example,
                    target_result=TargetResult(example_id=example.id, output="", error=str(e)),
                    success=False
                )

    async def run_suite(self, examples: Sequence[Example]) -> List[EvaluationResult]:
        tasks = [self._evaluate_single(ex) for ex in examples]
        return await asyncio.gather(*tasks)