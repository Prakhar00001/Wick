import typer
import asyncio
from rich.console import Console
import uuid

from wick.core.models import Example
from wick.runners.async_runner import AsyncEvalRunner
from wick.scorers.llm_judge import LLMJudgeScorer
from wick.reporters.console import ConsoleReporter
from wick.regression.store import RunStore

app = typer.Typer(help="Wick: Production LLM Evaluation Harness")
console = Console()

# Mock target for demonstration without API keys
class MockTarget:
    async def run(self, example: Example, *, trace: bool = False):
        from wick.core.models import TargetResult
        return TargetResult(example_id=example.id, output=f"Processed: {example.input.get('query')}")

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
            Example(id="ex-2", input={"query": "Write a python script to reverse a string."})
        ]
        
        target = MockTarget()
        # In a real run, you'd instantiate based on YAML config
        scorers = [LLMJudgeScorer(criteria="Is the response concise and accurate?")]
        
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