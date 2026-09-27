from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from typing import List
from wick.core.models import EvaluationResult

console = Console()
# Vibrant Terminal-Native Crimson Red
RED = "#FF2E4D"

class ConsoleReporter:
    @staticmethod
    def print_summary(results: List[EvaluationResult]):
        total = len(results)
        passed = sum(1 for r in results if r.success)
        failed = total - passed
        
        table = Table(
            title=f"\n[{RED}]Evaluation Scorecard[/{RED}]", 
            show_header=True, 
            header_style=f"bold {RED}",
            border_style=RED,
            title_justify="center"
        )
        table.add_column("Example ID", style=RED)
        table.add_column("Status", justify="center")
        table.add_column("Scores", style=RED)
        
        for res in results:
            status = "[bold green]PASS[/bold green]" if res.success else "[bold red]FAIL[/bold red]"
            score_str = ", ".join([f"{s.name}: {s.value:.2f}" for s in res.scores])
            table.add_row(res.example.id, status, score_str)
            
        console.print(table)
        console.print()
        
        summary = f"Total: {total} | [bold green]Passed: {passed}[/bold green] | [bold red]Failed: {failed}[/bold red]"
        console.print(Panel(summary, title=f"[{RED}]Run Complete[/{RED}]", border_style=RED, title_align="left"))