import json
import os
import logging
from typing import Optional
from groq import AsyncGroq
from wick.core.interfaces import Scorer
from wick.core.models import Example, TargetResult

logger = logging.getLogger("wick.scorer")

class LLMJudgeScorer(Scorer):
    # Using Llama 3 70B as default since it is highly capable for evaluation tasks
    def __init__(self, model: str = "llama3-70b-8192", criteria: str = "Is the output helpful?"):
        self._name = f"llm_judge_{model}"
        self.model = model
        self.criteria = criteria
        
        # Initialize Groq client
        self.client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))

    @property
    def name(self) -> str:
        return self._name

    async def score(self, example: Example, result: TargetResult) -> float:
        prompt = f"""
        Evaluate the following output based on this criteria: "{self.criteria}"
        
        Input: {example.input}
        Output: {result.output}
        
        Respond ONLY with a valid JSON object containing two keys:
        "score": A float between 0.0 and 1.0 (where 1.0 means perfect alignment with criteria)
        "reasoning": A brief explanation of the score.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.0 # Deterministic evaluation
            )
            
            content = response.choices[0].message.content or "{}"
            parsed = json.loads(content)
            return float(parsed.get("score", 0.0))
            
        except Exception as e:
            logger.error(f"Groq Evaluation Failed for {example.id}: {str(e)}")
            return 0.0