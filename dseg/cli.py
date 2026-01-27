# cli stuff

from pathlib import Path
import argparse
import shutil

from .io import materialize_input_as_nifti
from .nnunet import run_nnunet_predict, find_prediction_file
from .postprocess import split_multilabel


def main():
    ap = argparse.ArgumentParser(prog="dseg")
    ap.add_argument("--input", required=True, help="DICOM folder or volume file (.nii.gz/.nrrd/.mha/...)")
    ap.add_argument("--out", required=True, help="Output folder")
    ap.add_argument("--dataset", default="Dataset112_DentalSegmentator_v100", help="Dataset id or name (e.g., 112)")
    ap.add_argument("--device", default="cuda", choices=["cuda", "cpu"], help="Inference device")

    # advanced stuff (loweky wont need this)
    ap.add_argument("--folds", default="0", help="Fold(s), e.g. 0 or 0 1 2 3 4 (passed as a single string)")
    ap.add_argument("--disable-tta", action="store_true", default=True, help="Disable test-time augmentation (default: on)")

    args = ap.parse_args()

    inp = Path(args.input)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    nn_in = out / "nnunet_input"
    nn_out = out / "nnunet_output"
    nn_in.mkdir(exist_ok=True)
    nn_out.mkdir(exist_ok=True)

    # nnU-Net uses *_0000 for channel 0
    nifti_path = nn_in / "case_0000.nii.gz"
    materialize_input_as_nifti(inp, nifti_path)

    run_nnunet_predict(
        input_dir=nn_in,
        output_dir=nn_out,
        dataset=args.dataset,
        device=args.device,
        folds=args.folds,
        disable_tta=args.disable_tta,
    )

    pred = find_prediction_file(nn_out)
    seg_final = out / "segmentation.nii.gz"
    shutil.copy2(pred, seg_final)

    split_multilabel(seg_final, out / "masks")

    print("\nDone.")
    print("Input (converted):", nifti_path)
    print("Segmentation:", seg_final)
    print("Masks:", out / "masks")


if __name__ == "__main__":
    main()