import os
from enum import Enum

import typer
import uvicorn
from dotenv import load_dotenv

app = typer.Typer(help="FastAPI Template CLI")


class DatabaseType(str, Enum):
    postgresql = "postgresql"


@app.command()
def init_application(
        name: str = typer.Argument(..., help="Project name"),
        persistence: bool = typer.Option(False, "--persist", "-p", help="Enable database persistence"),
        host: str = typer.Option("0.0.0.0", help="Host to bind"),
        port: int = typer.Option(8000, help="Port to bind"),
        reload: bool = typer.Option(False, help="Enable auto-reload"),
        workers: int = typer.Option(1, help="Number of worker processes"),
        env: str = typer.Option('dev', help="Environment")
):
    typer.echo(f"Initializing FastAPI project: {name}")
    os.environ["APP_NAME"] = str(name)
    typer.echo(f"Environment: {env}")

    env_path = os.path.abspath(f"{env}.env")
    if not os.path.exists(env_path):
        typer.secho(f"Environment file {env_path} not found.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    os.environ["ENV_PATH"] = env_path

    load_dotenv(env_path)

    os.environ["ENABLE_PERSISTENCE"] = "true" if persistence else "false"
    typer.echo(f"Persistence: {os.environ.get('ENABLE_PERSISTENCE')}")

    if reload and workers > 1:
        typer.secho("Warning: 'reload' is incompatible with multiple workers. Using a single worker.",
                    fg=typer.colors.YELLOW)

    run_application(host=host, port=port, reload=reload, workers=workers)
    typer.echo("Project initialized successfully!")


def run_application(
        host: str,
        port: int,
        reload: bool,
        workers: int,
):
    typer.echo(f"Starting FastAPI server on {host}:{port}")
    from backend.main import create_app

    app = create_app()

    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=reload,
        workers=workers if not reload else 1
    )


if __name__ == "__main__":
    app()
