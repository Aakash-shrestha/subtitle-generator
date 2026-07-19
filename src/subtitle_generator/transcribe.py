import time
from pathlib import Path

import mlx_whisper
from rich.console import Console

from subtitle_generator.types import TranscriptSegment

console = Console()

MODEL = "mlx-community/whisper-large-v3-turbo"


def _clock(seconds: float) -> str:
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes:02d}:{secs:02d}"


def transcribe(audio_path: Path) -> list[TranscriptSegment]:
    console.print(f"Transcribing on Apple GPU (MLX, {MODEL.split('/')[-1]})...")
    started = time.monotonic()

    result = mlx_whisper.transcribe(
        str(audio_path),
        path_or_hf_repo=MODEL,
        word_timestamps=True,
        verbose=False,
    )

    segments = []
    for seg in result["segments"]:
        words = seg.get("words") or []
        start = words[0]["start"] if words else seg["start"]
        end = words[-1]["end"] if words else seg["end"]
        segments.append(
            TranscriptSegment(start=float(start), end=float(end), text=seg["text"])
        )

    elapsed = time.monotonic() - started
    audio_len = float(segments[-1].end) if segments else 0.0
    console.print(
        f"Detected language: [bold]{result['language']}[/] | "
        f"transcribed {_clock(audio_len)} of audio in {_clock(elapsed)} "
        f"({audio_len / elapsed:.1f}x realtime)"
    )
    return segments
