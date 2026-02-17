#!/usr/bin/env python3
"""
Developer Productivity Dashboard
Built by Jackson Studio

A terminal-based dashboard showing Git activity, GitHub stats, 
daily goals, and productivity metrics.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box

try:
    from git import Repo
    HAS_GIT = True
except ImportError:
    HAS_GIT = False

try:
    from github import Github
    HAS_GITHUB = True
except ImportError:
    HAS_GITHUB = False


class ProductivityDashboard:
    """Main dashboard controller"""
    
    def __init__(self, config_path: str = "config.json"):
        self.console = Console()
        self.config = self.load_config(config_path)
        self.layout = self.create_layout()
        self.goals = self.load_goals()
        
        if HAS_GITHUB and self.config.get("github", {}).get("token"):
            self.gh = Github(self.config["github"]["token"])
        else:
            self.gh = None
    
    def load_config(self, path: str) -> Dict:
        """Load configuration from JSON file"""
        if not os.path.exists(path):
            self.console.print(f"[red]Config file not found: {path}[/red]")
            self.console.print("[yellow]Creating example config...[/yellow]")
            self.create_example_config(path)
            sys.exit(1)
        
        with open(path) as f:
            return json.load(f)
    
    def create_example_config(self, path: str):
        """Create example config.json"""
        example = {
            "github": {
                "token": "",
                "username": "your-username",
                "repos": []
            },
            "local_repos": [],
            "goals": {
                "commits_per_day": 5,
                "coding_hours_per_day": 4
            },
            "refresh_interval": 60
        }
        with open(path, 'w') as f:
            json.dump(example, f, indent=2)
        self.console.print(f"[green]Created {path} — edit it with your settings[/green]")
    
    def load_goals(self) -> List[Dict]:
        """Load today's goals from file"""
        goals_file = "goals.json"
        if not os.path.exists(goals_file):
            return []
        
        with open(goals_file) as f:
            data = json.load(f)
        
        today = datetime.now().strftime("%Y-%m-%d")
        return data.get(today, [])
    
    def create_layout(self) -> Layout:
        """Create the dashboard layout"""
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )
        
        layout["body"].split_row(
            Layout(name="left"),
            Layout(name="right")
        )
        
        layout["left"].split_column(
            Layout(name="stats"),
            Layout(name="goals")
        )
        
        layout["right"].split_column(
            Layout(name="github"),
            Layout(name="streak")
        )
        
        return layout
    
    def render_header(self) -> Panel:
        """Render header panel"""
        now = datetime.now()
        title = Text("Developer Productivity Dashboard", style="bold cyan")
        subtitle = Text(now.strftime("%A, %B %d, %Y"), style="dim")
        content = Align.center(Text.assemble(title, "\n", subtitle))
        return Panel(content, box=box.DOUBLE)
    
    def render_stats(self) -> Panel:
        """Render today's stats"""
        if not HAS_GIT:
            return Panel("[yellow]GitPython not installed[/yellow]", title="📊 Today's Stats")
        
        commits_today = self.count_commits_today()
        coding_time = self.calculate_coding_time()
        active_repos = len(self.config.get("local_repos", []))
        
        table = Table.grid(padding=(0, 2))
        table.add_column(style="cyan")
        table.add_column(style="green")
        
        table.add_row("Commits:", str(commits_today))
        table.add_row("Coding Time:", coding_time)
        table.add_row("Active Repos:", str(active_repos))
        
        return Panel(table, title="📊 Today's Stats", box=box.ROUNDED)
    
    def count_commits_today(self) -> int:
        """Count commits made today across all repos"""
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        total = 0
        
        for repo_path in self.config.get("local_repos", []):
            if not os.path.exists(repo_path):
                continue
            
            try:
                repo = Repo(repo_path)
                for commit in repo.iter_commits(since=today_start.isoformat()):
                    if commit.author.email == self.config.get("github", {}).get("email", ""):
                        total += 1
            except Exception:
                pass
        
        return total
    
    def calculate_coding_time(self) -> str:
        """Calculate coding time based on commit timestamps"""
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        commit_times = []
        
        for repo_path in self.config.get("local_repos", []):
            if not os.path.exists(repo_path):
                continue
            
            try:
                repo = Repo(repo_path)
                for commit in repo.iter_commits(since=today_start.isoformat()):
                    commit_times.append(commit.committed_datetime)
            except Exception:
                pass
        
        if not commit_times:
            return "0h 0m"
        
        # Sort and calculate gaps
        commit_times.sort()
        total_minutes = 0
        
        for i in range(1, len(commit_times)):
            gap = (commit_times[i] - commit_times[i-1]).total_seconds() / 60
            if gap < 30:  # Assume active if commits < 30min apart
                total_minutes += gap
        
        hours = int(total_minutes // 60)
        minutes = int(total_minutes % 60)
        return f"{hours}h {minutes}m"
    
    def render_goals(self) -> Panel:
        """Render daily goals"""
        if not self.goals:
            content = Text("No goals set for today.\nPress 'G' to add goals.", style="dim")
        else:
            table = Table.grid(padding=(0, 1))
            table.add_column(width=2)
            table.add_column()
            
            for goal in self.goals:
                status = "✅" if goal.get("completed") else "⏳"
                table.add_row(status, goal["text"])
            
            content = table
        
        return Panel(content, title="🎯 Daily Goals", box=box.ROUNDED)
    
    def render_github(self) -> Panel:
        """Render GitHub stats"""
        if not self.gh:
            content = Text("GitHub integration disabled.\nAdd token to config.json", style="dim")
            return Panel(content, title="📈 GitHub Stats", box=box.ROUNDED)
        
        try:
            user = self.gh.get_user(self.config["github"]["username"])
            
            table = Table.grid(padding=(0, 2))
            table.add_column(style="cyan")
            table.add_column(style="green")
            
            table.add_row("Public Repos:", str(user.public_repos))
            table.add_row("Total Stars:", str(sum(r.stargazers_count for r in user.get_repos())))
            table.add_row("Followers:", str(user.followers))
            
            return Panel(table, title="📈 GitHub Stats", box=box.ROUNDED)
        
        except Exception as e:
            return Panel(f"[red]GitHub API error: {str(e)}[/red]", title="📈 GitHub Stats")
    
    def render_streak(self) -> Panel:
        """Render commit streak"""
        streak = self.calculate_streak()
        
        text = Text.assemble(
            ("🔥 ", "red bold"),
            (f"{streak} days", "yellow bold")
        )
        
        content = Align.center(text)
        return Panel(content, title="Commit Streak", box=box.ROUNDED)
    
    def calculate_streak(self) -> int:
        """Calculate current commit streak"""
        if not HAS_GIT:
            return 0
        
        # Simplified streak calculation
        # In production, this would check each day going backwards
        return 14  # Placeholder
    
    def render_footer(self) -> Panel:
        """Render footer with shortcuts"""
        shortcuts = Text.assemble(
            ("R", "bold cyan"), " Refresh  ",
            ("G", "bold cyan"), " Goals  ",
            ("Q", "bold cyan"), " Quit"
        )
        return Panel(Align.center(shortcuts), box=box.DOUBLE)
    
    def render(self):
        """Render the entire dashboard"""
        self.layout["header"].update(self.render_header())
        self.layout["stats"].update(self.render_stats())
        self.layout["goals"].update(self.render_goals())
        self.layout["github"].update(self.render_github())
        self.layout["streak"].update(self.render_streak())
        self.layout["footer"].update(self.render_footer())
        
        return self.layout


def main():
    """Main entry point"""
    dashboard = ProductivityDashboard()
    
    try:
        with Live(dashboard.render(), console=dashboard.console, refresh_per_second=1):
            dashboard.console.print("[green]Dashboard started. Press Ctrl+C to exit.[/green]")
            import time
            while True:
                time.sleep(dashboard.config.get("refresh_interval", 60))
                dashboard.render()
    except KeyboardInterrupt:
        dashboard.console.print("\n[yellow]Dashboard stopped.[/yellow]")


if __name__ == "__main__":
    main()
