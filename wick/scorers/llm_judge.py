import json
from typing import Optional
from openai import AsyncOpenAI
from wick.core.interfaces import Scorer
from wick.core.models import Example, TargetResult

class LLMJudgeScorer(Scorer):
    def __init__(self, model: str = "gpt-4o", criteria: str = "Is the output helpful?"):
        self._name = f"llm_judge_{model}"
        self.model = model
        self.criteria = criteria
        self.client = AsyncOpenAI()

    @property
    def name(self) -> str:
        return self._name

    async def score(self, example: Example, result: TargetResult) -> float:
        prompt = f"""
        Evaluate the following output based on this criteria: "{self.criteria}"
        
        Input: {example.input}
        Output: {result.output}
        
        Respond ONLY with a valid JSON object containing two keys:
        "score": A float between 0.0 and 1.0
        "reasoning": A brief explanation of the score.
        """
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.0
        )
        
        try:
            content = response.choices[0].message.content or "{}"
            parsed = json.loads(content)
            # In a real system, we'd inject 'reasoning' into the Score object metadata
            return float(parsed.get("score", 0.0))
        except Exception:
            return 0.0