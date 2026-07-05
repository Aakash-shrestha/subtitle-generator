from dataclasses import dataclass


@dataclass
class SepakerTurn:
    start: float
    end: float
    speaker: str


@dataclass
class TranscriptSegment:
    start: float
    end: float
    text: str
