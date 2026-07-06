from pathlib import Path

from subtitle_generator.types import SpeakerTurn, SubtitleCue, TranscriptSegment


def _overlap(a_start: float, a_end: float, b_start: float, b_end: float) -> float:
    return max(0.0, min(a_end, b_end) - max(a_start, b_start))


def _format_timestamp(seconds: float) -> str:
    total_ms = round(seconds * 1000)
    hours, remainder_ms = divmod(total_ms, 3_600_000)
    minutes, remainder_ms = divmod(remainder_ms, 60_000)
    secs, ms = divmod(remainder_ms, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def assign_speakers(
    transcript: list[TranscriptSegment], turns: list[SpeakerTurn]
) -> list[SubtitleCue]:
    cues: list[SubtitleCue] = []
    for segment in transcript:
        best_turn = max(
            turns,
            key=lambda turn: _overlap(segment.start, segment.end, turn.start, turn.end),
            default=None,
        )  # finds the highest overlap turn for each segment, returns best turn basically

        speaker = best_turn.speaker if best_turn else "unknown"
        cues.append(
            SubtitleCue(
                start=segment.start, end=segment.end, speaker=speaker, text=segment.text
            )
        )
    return cues


def write_srt(cues: list[SubtitleCue], output_path: Path) -> None:
    lines = []
    for i, cue in enumerate(cues, start=1):
        lines.append(str(i))
        lines.append(
            f"""{_format_timestamp(cue.start)} --> {_format_timestamp(cue.end)}"""
        )
        lines.append(cue.text.strip())
        lines.append("")  # Empty line after each cue
    output_path.write_text("\n".join(lines), encoding="utf-8")
