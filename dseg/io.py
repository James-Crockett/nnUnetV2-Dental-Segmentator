from pathlib import Path
import shutil
import SimpleITK as sitk


def read_dicom_series(dicom_dir: Path) -> sitk.Image:
    reader = sitk.ImageSeriesReader()
    series_ids = reader.GetGDCMSeriesIDs(str(dicom_dir))
    if not series_ids:
        raise ValueError(f"No DICOM series found in: {dicom_dir}")

    # if multiple series exist, we take the first.
    series_files = reader.GetGDCMSeriesFileNames(str(dicom_dir), series_ids[0])
    reader.SetFileNames(series_files)
    return reader.Execute()


def load_volume(path: Path) -> sitk.Image:
    return sitk.ReadImage(str(path))


def save_as_nifti(img: sitk.Image, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sitk.WriteImage(img, str(out_path), useCompression=True)


def materialize_input_as_nifti(inp: Path, nifti_out: Path) -> None:
    """
    only accepts:
      - DICOM directory
      - volume file (.nii/.nii.gz/.nrrd/.mha/...)
    writes a NIfTI (.nii.gz) to `nifti_out`.
    """
    nifti_out.parent.mkdir(parents=True, exist_ok=True)

    if inp.is_dir():
        img = read_dicom_series(inp)
        save_as_nifti(img, nifti_out)
        return

    # if already nifti, copy.
    if inp.suffixes[-2:] == [".nii", ".gz"] or inp.suffix == ".nii":
        shutil.copy2(inp, nifti_out)
        return

    # convert other formats via SimpleITK
    img = load_volume(inp)
    save_as_nifti(img, nifti_out)