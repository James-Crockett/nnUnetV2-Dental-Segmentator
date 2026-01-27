from pathlib import Path
import subprocess
from .constants import (
    DEFAULT_TRAINER,
    DEFAULT_PLANS,
    DEFAULT_CONFIG,
    DEFAULT_FOLDS,
    DEFAULT_CHECKPOINT,
)


def run_nnunet_predict(
    input_dir: Path,
    output_dir: Path,
    dataset: str,
    trainer: str = DEFAULT_TRAINER,
    plans: str = DEFAULT_PLANS,
    config: str = DEFAULT_CONFIG,
    folds: str = DEFAULT_FOLDS,
    device: str = "cuda",  # if no gpu use "cpu" 
    checkpoint: str = DEFAULT_CHECKPOINT,
    disable_tta: bool = True,
    npp: int = 1,
    nps: int = 1,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "nnUNetv2_predict",
        "-i", str(input_dir),
        "-o", str(output_dir),
        "-d", str(dataset),
        "-tr", trainer,
        "-p", plans,
        "-c", config,
        "-f", folds,
        "-npp", str(npp),
        "-nps", str(nps),
        "-device", device,
        "-chk", checkpoint,
    ]
    if disable_tta:
        cmd.append("--disable_tta")

    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)


def find_prediction_file(output_dir: Path) -> Path:
    preds = sorted(output_dir.glob("*.nii.gz"))
    if not preds:
        raise RuntimeError(f"No prediction file found in {output_dir}")
    return preds[0]