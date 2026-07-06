from pathlib import Path

from faster_whisper import WhisperModel

from subtitle_generator.types import TranscriptSegment


def transcribe(audio_path: Path) -> list[TranscriptSegment]:
    model = WhisperModel("large-v3", device="cpu", compute_type="int8")

    segments, info = model.transcribe(
        str(audio_path), multilingual=True, beam_size=1, word_timestamps=True
    )
    print(f"Detected language: {info.language} (p={info.language_probability:.2f})")

    result = []
    for segment in segments:
        words = segment.words
        start = words[0].start if words else segment.start
        end = words[-1].end if words else segment.end
        result.append(TranscriptSegment(start=start, end=end, text=segment.text))
    return result
