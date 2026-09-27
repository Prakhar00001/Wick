from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from typing import List
from wick.core.models import EvaluationResult

console = Console()

class ConsoleReporter:
    @staticmethod
    def print_summary(results: List[EvaluationResult]):
        total = len(results)
        passed = sum(1 for r in results if r.success)
        failed = total - passed
        
        table = Table(title="Evaluation Scorecard", show_header=True, header_style="bold magenta")
        table.add_column("Example ID", style="cyan")
        table.add_column("Status", justify="center")
        table.add_column("Scores")
        
        for res in results:
            status = "[green]PASS[/green]" if res.success else "[red]FAIL[/red]"
            score_str = ", ".join([f"{s.name}: {s.value:.2f}" for s in res.scores])
            table.add_row(res.example.id, status, score_str)
            
        console.print(table)
        
        summary = f"Total: {total} | [green]Passed: {passed}[/green] | [red]Failed: {failed}[/red]"
        console.print(Panel(summary, title="Run Complete", border_style="blue"))