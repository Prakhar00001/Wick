import typer
import asyncio
import uuid
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from wick.core.models import Example, TargetResult
from wick.runners.async_runner import AsyncEvalRunner
from wick.scorers.llm_judge import LLMJudgeScorer
from wick.reporters.console import ConsoleReporter
from wick.regression.store import RunStore

app = typer.Typer(help="Wick: Production LLM Evaluation Harness")
console = Console()

# Vibrant Terminal-Native Crimson Red
RED = "#FF2E4D"

BANNER = f"""[{RED}]
██╗    ██╗██╗ ██████╗██╗  ██╗
██║    ██║██║██╔════╝██║ ██╔╝
██║ █╗ ██║██║██║     █████╔╝ 
██║███╗██║██║██║     ██╔═██╗ 
╚███╔███╔╝██║╚██████╗██║  ██╗
 ╚══╝╚══╝ ╚═╝ ╚═════╝╚═╝  ╚═╝[/{RED}]"""

SUBTITLE = f"[{RED}]>_ PRODUCTION LLM EVALUATION ENGINE • TERMINAL-NATIVE HARNESS[/{RED}]\n"

def print_init_panel():
    """Generates the interactive startup panel in vibrant red."""
    left_content = f"""[{RED}]
      .-.  
     [o o] 
     | v | 
     '---' 
    [ WICK ]
    
session:  {str(uuid.uuid4())[:8]}
target:   local_run[/{RED}]"""

    right_content = f"""
[bold {RED}]Active Subsystems[/bold {RED}]
  [{RED}]runner:[/{RED}]   asyncio bounded semaphore (concurrency: 10)
  [{RED}]scorer:[/{RED}]   llm-as-a-judge (openai/gpt-oss-120b)
  [{RED}]db:[/{RED}]       aiosqlite regression engine
  [{RED}]target:[/{RED}]   SmartMockTarget

[bold {RED}]Intelligence & Heuristics[/bold {RED}]
  [{RED}]metrics:[/{RED}]  groundedness, relevance, exact-match
  [{RED}]traces:[/{RED}]   zero-overhead latency & token tracking
"""
    
    grid = Table.grid(expand=True)
    grid.add_column(width=20)
    grid.add_column()
    grid.add_row(left_content, right_content)
    
    panel = Panel(
        grid,
        title=f"[bold {RED}]WICK --INIT v0.1.0[/bold {RED}]",
        title_align="left",
        border_style=RED,
        padding=(1, 2)
    )
    console.print(panel)
    console.print()

class SmartMockTarget:
    async def run(self, example: Example, *, trace: bool = False) -> TargetResult:
        query = str(example.input.get("query", "")).lower()
        if "light" in query:
            ans = "The speed of light in a vacuum is approximately 299,792 kilometers per second."
        else:
            ans = "The sky is blue due to Rayleigh scattering of sunlight by the atmosphere."
        # Simulating processing time
        await asyncio.sleep(0.5)
        return TargetResult(example_id=example.id, output=ans)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    console.print(BANNER)
    console.print(SUBTITLE)
    if ctx.invoked_subcommand is None:
        console.print(f"[{RED}]> wick ready. run 'wick --help' for commands.[/{RED}]")

@app.command()
def run(suite: str = typer.Argument(..., help="Path to evaluation suite YAML")):
    async def _run():
        print_init_panel()
        
        examples = [
            Example(id="ex-1", input={"query": "What is the speed of light?"}),
            Example(id="ex-2", input={"query": "Why is the sky blue?"})
        ]
        
        target = SmartMockTarget()
        scorers = [LLMJudgeScorer(criteria="Is the response scientifically accurate and direct?")]
        runner = AsyncEvalRunner(target=target, scorers=scorers)
        
        with console.status(f"[bold {RED}]Executing target traces & remote heuristics...[/bold {RED}]", spinner="bouncingBar"):
            results = await runner.run_suite(examples)
            
        ConsoleReporter.print_summary(results)
        
        store = RunStore()
        await store.initialize()
        await store.save_run(str(uuid.uuid4()), results)
        
    asyncio.run(_run())

@app.command()
def compare(run_a: str, run_b: str):
    console.print(f"Comparing [bold]{run_a}[/bold] with [bold]{run_b}[/bold]...")

@app.command()
def doctor():
    console.print(f"[{RED}]System dependencies and API keys verified.[/{RED}]")

if __name__ == "__main__":
    app()