import typer

app = typer.Typer()


@app.command()
def process(input_path: str):
    """Process an interview video/audio file into an .srt subtitle file."""
    typer.echo(f"Would process: {input_path}")


if __name__ == "__main__":
    app()
