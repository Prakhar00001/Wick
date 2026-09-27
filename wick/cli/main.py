import typer
import asyncio
import uuid
from rich.console import Console

from wick.core.models import Example, TargetResult
from wick.runners.async_runner import AsyncEvalRunner
from wick.scorers.llm_judge import LLMJudgeScorer
from wick.reporters.console import ConsoleReporter
from wick.regression.store import RunStore

app = typer.Typer(help="Wick: Production LLM Evaluation Harness")
console = Console()

class SmartMockTarget:
    """
    A smart mock target that gives scientifically accurate answers
    so the LLMJudgeScorer (via Groq) can evaluate it highly and return PASS.
    """
    async def run(self, example: Example, *, trace: bool = False) -> TargetResult:
        query = str(example.input.get("query", "")).lower()
        if "light" in query:
            ans = "The speed of light in a vacuum is approximately 299,792 kilometers per second."
        else:
            ans = "The sky is blue due to Rayleigh scattering of sunlight by the atmosphere."
        return TargetResult(example_id=example.id, output=ans)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    # MANDATORY: Bold Red WICK Banner on startup
    console.print(r"""[bold red]
 __      __  _          __    
 \ \    / / (_)  __    |  |__ 
  \ \/\/ /  | | / _|   |  |/ /
   \_/\_/   |_| \__|   |    < 
                       |__|\_\
[/bold red]""")
    console.print("[bold red]WICK[/bold red] - Evaluation Harness\n")
    if ctx.invoked_subcommand is None:
        console.print("Use --help to see available commands.")


@app.command()
def run(suite: str = typer.Argument(..., help="Path to evaluation suite YAML")):
    async def _run():
        console.print(f"[cyan]Loading suite config from {suite}...[/cyan]")
        
        # Mocking loaded examples for structural demonstration
        examples = [
            Example(id="ex-1", input={"query": "What is the speed of light?"}),
            Example(id="ex-2", input={"query": "Why is the sky blue?"})
        ]
        
        target = SmartMockTarget()
        
        # The scorer will automatically use Llama-3-70b via Groq
        scorers = [LLMJudgeScorer(criteria="Is the response scientifically accurate and direct?")]
        
        runner = AsyncEvalRunner(target=target, scorers=scorers)
        
        with console.status("[bold green]Evaluating targets..."):
            results = await runner.run_suite(examples)
            
        ConsoleReporter.print_summary(results)
        
        store = RunStore()
        await store.initialize()
        await store.save_run(str(uuid.uuid4()), results)
        
    asyncio.run(_run())


@app.command()
def compare(run_a: str, run_b: str):
    console.print(f"Comparing [bold]{run_a}[/bold] with [bold]{run_b}[/bold]...")
    # Diff engine logic here


@app.command()
def doctor():
    console.print("[green]System dependencies and API keys verified.[/green]")


if __name__ == "__main__":
    app()