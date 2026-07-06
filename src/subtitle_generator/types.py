from dataclasses import dataclass


@dataclass
class SpeakerTurn:
    start: float
    end: float
    speaker: str


@dataclass
class TranscriptSegment:
    start: float
    end: float
    text: str


@dataclass
class SubtitleCue:
    start: float
    end: float
    speaker: str
    text: str
