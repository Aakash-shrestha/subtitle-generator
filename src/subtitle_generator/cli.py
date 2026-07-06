import gc
import os
from pathlib import Path

import typer
from dotenv import find_dotenv, load_dotenv

from subtitle_generator.audio import export_audio
from subtitle_generator.cache import save_json
from subtitle_generator.diarize import diarize
from subtitle_generator.merge import assign_speakers, write_srt
from subtitle_generator.transcribe import transcribe

app = typer.Typer()


@app.command()
def process(
    input_path: Path = typer.Argument(
        ..., exists=True, help="Interview video/audio file"
    ),
):
    """Process an interview video/audio file into an .srt subtitle file."""
    load_dotenv(find_dotenv(usecwd=True))
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise RuntimeError(
            "HF_TOKEN not found in environment variables. Please set it in your .env file."
        )

    slug = input_path.stem
    output_dir = Path("data") / slug
    output_dir.mkdir(parents=True, exist_ok=True)

    wav_path = output_dir / "audio.wav"
    export_audio(input_path, wav_path)
    typer.echo(f"Audio exported to {wav_path}")

    turns = diarize(wav_path, hf_token)
    save_json(output_dir / "diarization.json", turns)
    typer.echo(f"Diarization found {len(turns)} turns")

    gc.collect()

    segments = transcribe(wav_path)
    save_json(output_dir / "transcription.json", segments)
    typer.echo(f"Transcription found {len(segments)} segments")

    cues = assign_speakers(segments, turns)
    srt_path = output_dir / f"{slug}.srt"
    write_srt(cues, srt_path)
    typer.echo(f"Wrote subtitles -> {srt_path}")


if __name__ == "__main__":
    app()
