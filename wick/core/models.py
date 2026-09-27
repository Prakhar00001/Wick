from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class TraceStep(BaseModel):
    step_name: str
    latency_ms: float
    input_data: Any
    output_data: Any
    tokens_used: int = 0
    cost: float = 0.0

class Trace(BaseModel):
    steps: List[TraceStep] = Field(default_factory=list)
    total_latency_ms: float = 0.0
    total_tokens: int = 0
    total_cost: float = 0.0

class Example(BaseModel):
    id: str
    input: Dict[str, Any]
    expected_output: Optional[Any] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class TargetResult(BaseModel):
    example_id: str
    output: Any
    trace: Trace = Field(default_factory=Trace)
    error: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None

class Score(BaseModel):
    name: str
    value: float
    passed: bool
    reasoning: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class EvaluationResult(BaseModel):
    example: Example
    target_result: TargetResult
    scores: List[Score] = Field(default_factory=list)
    success: bool = False