#!/usr/bin/env python3
"""
sup - The Ultimate Superset CLI 🚀

Main entry point for the sup command-line interface.
"""

import os
import typer
from rich.theme import Theme
from typing_extensions import Annotated

from sup.commands import (
    chart,
    dashboard,
    database,
    dataset,
    dbt,
    group,
    instance,
    ownership,
    query,
    rls,
    role,
    sql,
    sync,
    theme,
    user,
    workspace,
)
from sup.commands import config as config_cmd
from sup.output.console import get_console
from sup.output.styles import RICH_STYLES

# Custom Rich theme to eliminate purple/magenta colors
PRESET_THEME = Theme(
    {
        # Override default purple/magenta with emerald green
        "panel.border": "#10B981",  # Emerald green borders
        "panel.title": "bold #10B981",  # Emerald green panel titles
        "rule.line": "#10B981",  # Emerald green lines
        "table.header": "bold #10B981",  # Emerald green table headers
        "table.border": "#10B981",  # Emerald green table borders
        "table.title": "bold #10B981",  # Emerald green table titles
        "progress.bar": "#10B981",  # Emerald green progress bars
        "progress.complete": "#10B981",  # Emerald green completion
    },
)

# Initialize Rich console with custom theme
console = get_console(theme=PRESET_THEME)

# ASCII Art Banner
BANNER = """\
██ ███████╗██╗   ██╗██████╗ ██╗
██ ██╔════╝██║   ██║██╔══██╗██║
   ███████╗██║   ██║██████╔╝██║
   ╚════██║██║   ██║██╔═══╝ ╚═╝
   ███████║╚██████╔╝██║     ██╗
   ╚══════╝ ╚═════╝ ╚═╝     ╚═╝"""

# App title for consistent usage
APP_TITLE = "🚀 'sup! - the official Preset CLI with a git-like interface 📊"

# Use cases for consistent display
USE_CASES = [
    "Run any SQL through Superset's data access layer - "
    + "get results as rich table, CSV, YAML or JSON",
    "Backup and restore charts, dashboards, and datasets with full dependency tracking",
    "Synchronize assets across Superset instances with Jinja2 templating for customization",
    "Enrich metadata to/from dbt Core/Cloud - more integrations to come",
    "Automate workflows and integrate with CI/CD pipelines",
    "Perfect for scripting and AI-assisted data exploration",
]

# Help text template - will be formatted with actual colors
HELP_TEMPLATE = """{app_title}
   [bold {primary}]Brought to you and fully compatible with Preset[/bold {primary}]
   [dim]For power users and AI agents[/dim]

[bold {primary}]Key capabilities:[/bold {primary}]
{capabilities}

[bold {primary}]Getting Started:[/bold {primary}]
• [bold]Step 1:[/bold] [cyan]sup config[/cyan] - Set up authentication and credentials
• [bold]Step 2:[/bold] [cyan]sup workspace list[/cyan] - Find your workspace
• [bold]Step 3:[/bold] [cyan]sup workspace use <ID>[/cyan] - Set default workspace
• [bold]Step 4:[/bold] [cyan]sup sql "SELECT 1"[/cyan] - Start querying data"""


def format_help():
    """Create help text with beautiful emerald green Preset branding."""
    from sup.output.styles import COLORS

    capabilities = "\n".join(f"• [bright_white]{use_case}[/bright_white]" for use_case in USE_CASES)

    # Format APP_TITLE with colors for consistent usage
    formatted_title = APP_TITLE.replace(
        "sup",
        f"[bold {COLORS.primary}]sup[/bold {COLORS.primary}]",
    )

    return HELP_TEMPLATE.format(
        app_title=formatted_title,
        primary=COLORS.primary,
        capabilities=capabilities,
    )


# Initialize the main Typer app with -h support
app = typer.Typer(
    name="sup",
    help=format_help(),
    rich_markup_mode="rich",
    no_args_is_help=False,  # We'll handle this ourselves
    context_settings={"help_option_names": ["-h", "--help"]},
)


def show_banner():
    """Display the sup banner with beautiful Preset emerald green branding."""
    from sup.output.styles import COLORS

    console.print(BANNER, style=f"bold {COLORS.primary}")  # Beautiful emerald green
    console.print(APP_TITLE, style=RICH_STYLES["info"])
    console.print(
        "   Brought to you and fully compatible with Preset",
        style=f"bold {COLORS.primary}",
    )
    console.print("   For power users and AI agents\n", style=RICH_STYLES["dim"])

    # High-level use cases
    console.print("[bold]Key capabilities:[/]", style=RICH_STYLES["header"])
    for use_case in USE_CASES:
        console.print(f"• {use_case}", style=RICH_STYLES["accent"])
    console.print()


# Add command modules with logical sectioning

app.add_typer(config_cmd.app, name="config", rich_help_panel="Configuration & Setup")
app.add_typer(sql.app, name="sql", rich_help_panel="Direct Data Access")
app.add_typer(
    workspace.app, name="workspace", help="Manage workspaces", rich_help_panel="Manage Assets"
)
app.add_typer(
    instance.app,
    name="instance",
    help="Manage self-hosted Superset instances",
    rich_help_panel="Manage Assets",
)
app.add_typer(
    database.app, name="database", help="Manage databases", rich_help_panel="Manage Assets"
)
app.add_typer(dataset.app, name="dataset", help="Manage datasets", rich_help_panel="Manage Assets")
app.add_typer(chart.app, name="chart", help="Manage charts", rich_help_panel="Manage Assets")
app.add_typer(
    dashboard.app, name="dashboard", help="Manage dashboards", rich_help_panel="Manage Assets"
)
app.add_typer(query.app, name="query", help="Manage saved queries", rich_help_panel="Manage Assets")
app.add_typer(user.app, name="user", help="Manage users", rich_help_panel="Manage Assets")
app.add_typer(group.app, name="group", help="Manage SCIM groups", rich_help_panel="Manage Assets")
app.add_typer(
    rls.app,
    name="rls",
    help="Manage row-level security",
    rich_help_panel="Security & Governance",
)
app.add_typer(
    role.app,
    name="role",
    help="Manage roles and permissions",
    rich_help_panel="Security & Governance",
)
app.add_typer(
    ownership.app,
    name="ownership",
    help="Manage asset ownership",
    rich_help_panel="Security & Governance",
)
app.add_typer(sync.app, name="sync", rich_help_panel="Synchronize Assets Across Workspaces")
app.add_typer(dbt.app, name="dbt", rich_help_panel="Integrations & Metadata")
app.add_typer(theme.app, name="theme", help="Manage themes", rich_help_panel="Manage Assets")


def version_callback(value: bool):
    if value:
        from sup import __version__

        console.print(f"sup version {__version__}", style=RICH_STYLES["success"])
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Annotated[
        bool,
        typer.Option("--version", "-v", help="Show version", callback=version_callback),
    ] = False,
    no_verify_ssl: Annotated[
        bool,
        typer.Option(
            "--no-verify-ssl",
            help=(
                "Disable TLS certificate verification for the Superset server. "
                "Use only for trusted internal hosts. Prefer --ca-bundle for "
                "internal CAs."
            ),
        ),
    ] = False,
    ca_bundle: Annotated[
        str,
        typer.Option(
            "--ca-bundle",
            help=(
                "Path to a CA bundle (PEM) used to verify the Superset server's "
                "TLS certificate. Use this for self-hosted Superset behind a "
                "private CA. Overrides per-instance config."
            ),
        ),
    ] = "",
):
    """
    🚀 The Ultimate Superset/Preset CLI 📊

    For power users and AI agents. Access data, manage assets, automate workflows.
    """
    # Propagate SSL overrides to the auth factory via env vars so any
    # downstream `create_superset_auth(config)` call respects them.
    if no_verify_ssl:
        os.environ["SUP_NO_VERIFY_SSL"] = "1"
    if ca_bundle:
        os.environ["SUP_CA_BUNDLE"] = ca_bundle

    if ctx.invoked_subcommand is None:
        show_banner()
        console.print(
            "Use [bold]sup --help[/] for available commands",
            style=RICH_STYLES["dim"],
        )


def cli():
    """Entry point for console script."""
    app()


if __name__ == "__main__":
    cli()
