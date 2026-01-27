#this file just reanames the mesh files
from pathlib import Path
import numpy as np
import nibabel as nib
from .constants import LABELS


def split_multilabel(seg_path: Path, masks_dir: Path) -> None:
    masks_dir.mkdir(parents=True, exist_ok=True)

    seg_nii = nib.load(str(seg_path))
    seg = seg_nii.get_fdata().astype(np.int16)

    for label_id, name in LABELS.items():
        mask = (seg == label_id).astype(np.uint8)
        out = nib.Nifti1Image(mask, seg_nii.affine, seg_nii.header)
        out_path = masks_dir / f"label_{label_id:02d}_{name}.nii.gz"
        nib.save(out, str(out_path))