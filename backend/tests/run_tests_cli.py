import os
import subprocess
from pathlib import Path

import typer
from dotenv import load_dotenv

app = typer.Typer()


@app.command()
def test(env: str = typer.Option("dev", help="Test environment (dev, test, ci)")):
    typer.echo(f"Environment: {env}")

    root_dir = Path(__file__).parent.resolve().parent
    env_file = root_dir / f"{env}.env"

    if env_file.exists():
        typer.echo(f"Loading environment from {env_file}")
        os.environ["ENV_PATH"] = str(env_file)
        load_dotenv(env_file)
    else:
        typer.echo(f"Warning: {env_file} not found. Using current env vars.")

    command = ["pytest", "--cov", "--env", env]
    raise SystemExit(subprocess.call(command))


if __name__ == "__main__":
    app()
