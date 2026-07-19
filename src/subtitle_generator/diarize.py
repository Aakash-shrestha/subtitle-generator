from collections.abc import Iterator
from pathlib import Path
from typing import cast

import torch
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.speaker_diarization import DiarizeOutput
from pyannote.audio.pipelines.utils.hook import ProgressHook
from pyannote.core import Segment

from subtitle_generator.types import SpeakerTurn


def diarize(audio_path: Path, hf_token: str) -> list[SpeakerTurn]:
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1", token=hf_token
    )
    if pipeline is None:
        raise RuntimeError("Failed to load pyannote diarization pipeline")

    device = torch.device("mps" if torch.mps.is_available() else "cpu")
    pipeline = pipeline.to(device)

    with ProgressHook() as hook:
        output = cast(DiarizeOutput, pipeline(str(audio_path), hook=hook))
    annotation = output.exclusive_speaker_diarization
    tracks = cast(
        Iterator[tuple[Segment, str, str]],
        annotation.itertracks(yield_label=True),
    )
    return [
        SpeakerTurn(start=segment.start, end=segment.end, speaker=speaker)
        for segment, _, speaker in tracks
        if segment.end > segment.start
    ]
