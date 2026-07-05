from pathlib import Path

import ffmpeg


def export_audio(input_path: Path, output_path: Path) -> Path:
    (
        ffmpeg.input(input_path)
        .output(output_path, ar=16000, ac=1, format="wav")
        .overwrite_output()
        .run(quiet=True)
    )
    return output_path
