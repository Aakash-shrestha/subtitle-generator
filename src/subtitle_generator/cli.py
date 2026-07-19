import gc
import os
from pathlib import Path

import typer
from dotenv import find_dotenv, load_dotenv

from subtitle_generator.audio import export_audio
from subtitle_generator.cache import load_json, save_json
from subtitle_generator.diarize import diarize
from subtitle_generator.merge import assign_speakers, write_srt
from subtitle_generator.transcribe import transcribe
from subtitle_generator.types import SpeakerTurn, TranscriptSegment

app = typer.Typer()


@app.command()
def process(
    input_path: Path = typer.Argument(
        ..., exists=True, help="Interview video/audio file"
    ),
    force: bool = typer.Option(
        False, "--force", help="Recompute all stages, ignoring cached results"
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
    if force or not wav_path.exists():
        export_audio(input_path, wav_path)
        typer.echo(f"Audio exported to {wav_path}")
    else:
        typer.echo(f"Using cached audio: {wav_path}")

    turns_path = output_dir / "diarization.json"
    if not force and turns_path.exists():
        turns = load_json(turns_path, SpeakerTurn)
        typer.echo(f"Loaded cached diarization ({len(turns)} turns)")
    else:
        turns = diarize(wav_path, hf_token)
        save_json(turns_path, turns)
        typer.echo(f"Diarization found {len(turns)} turns")

    gc.collect()

    segments_path = output_dir / "transcription.json"
    if not force and segments_path.exists():
        segments = load_json(segments_path, TranscriptSegment)
        typer.echo(f"Loaded cached transcription ({len(segments)} segments)")
    else:
        segments = transcribe(wav_path)
        save_json(segments_path, segments)
        typer.echo(f"Transcription found {len(segments)} segments")

    cues = assign_speakers(segments, turns)
    srt_path = output_dir / f"{slug}.srt"
    write_srt(cues, srt_path)
    typer.echo(f"Wrote subtitles -> {srt_path}")


if __name__ == "__main__":
    app()
