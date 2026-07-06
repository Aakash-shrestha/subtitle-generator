from subtitle_generator.types import SpeakerTurn, SubtitleCues, TranscriptSegment


def _overlap(a_start: float, a_end: float, b_start: float, b_end: float) -> float:
    return max(0.0, min(a_end, b_end) - max(a_start, b_start))


def assign_speakers(
    transcript: list[TranscriptSegment], turns: list[SpeakerTurn]
) -> list[SubtitleCues]:
    cues: list[SubtitleCues] = []
    for segment in transcript:
        best_turn = max(
            turns,
            key=lambda turn: _overlap(segment.start, segment.end, turn.start, turn.end),
            default=None,
        )  # finds the highest overlap turn for each segment, returns best turn basically

        speaker = best_turn.speaker if best_turn else "unknown"
        cues.append(
            SubtitleCues(
                start=segment.start, end=segment.end, speaker=speaker, text=segment.text
            )
        )
    return cues
