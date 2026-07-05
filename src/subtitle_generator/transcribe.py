from pathlib import Path

from faster_whisper import WhisperModel

from subtitle_generator.types import TranscriptSegment


def transcribe(audio_path: Path) -> list[TranscriptSegment]:
    model = WhisperModel("large-v3", device="cpu", compute_type="int8")

    segments, info = model.transcribe(str(audio_path), multilingual=True, beam_size=1)
    print(f"Detected language: {info.language} (p={info.language_probability:.2f})")

    return [
        TranscriptSegment(start=segment.start, end=segment.end, text=segment.text)
        for segment in segments
    ]
