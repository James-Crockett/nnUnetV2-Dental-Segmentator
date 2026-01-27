#  nnUnet2D Dental Segmentator

This project converts CBCT DICOM files into multi-class segmentation outputs. I used to work with this tool in 3D slicer. Integrated a similar tool like this my last internship. Just created this for my future projects to work with medical data.


## Model Classes

  Label   Structure
  ------- ------------------
  1       Upper skull
  2       Mandible
  3       Upper teeth
  4       Lower teeth
  5       Mandibular canal

------------------------------------------------------------------------

## Installation

Activate your virtual environment and install dependencies or use uv:

``` bash
pip install nnunetv2 SimpleITK nibabel numpy scipy scikit-image tqdm pypandoc
```

------------------------------------------------------------------------

## Set nnU-Net Environment Variables

### Windows (PowerShell)

``` powershell
$env:nnUNet_raw = "$PWD\nnunet_data\nnUNet_raw"
$env:nnUNet_preprocessed = "$PWD\nnunet_data\nnUNet_preprocessed"
$env:nnUNet_results = "$PWD\nnunet_data\nnUNet_results"

mkdir $env:nnUNet_raw, $env:nnUNet_preprocessed, $env:nnUNet_results -Force
Copy-Item -Recurse -Force ".\Dataset112_DentalSegmentator_v100" "$env:nnUNet_results\Dataset112_DentalSegmentator_v100"
```

### Linux / macOS

``` bash
export nnUNet_raw="$PWD/nnunet_data/nnUNet_raw"
export nnUNet_preprocessed="$PWD/nnunet_data/nnUNet_preprocessed"
export nnUNet_results="$PWD/nnunet_data/nnUNet_results"

mkdir -p "$nnUNet_raw" "$nnUNet_preprocessed" "$nnUNet_results"
cp -r Dataset112_DentalSegmentator_v100 "$nnUNet_results/"
```

------------------------------------------------------------------------

## To Run Segmentation

``` bash
python -m dseg.cli --input dataset/ --out run1 --dataset Dataset112_DentalSegmentator_v100 --device cuda
```

Or CPU:

``` bash
python -m dseg.cli --input dataset/ --out run1 --dataset Dataset112_DentalSegmentator_v100 --device cpu
```

------------------------------------------------------------------------

## References

-   https://zenodo.org/records/10829675
-   nnU‑Net: Isensee et al., *Nature Methods*, 2021\
-   DentalSegmentator: Gaudot et al., Slicer Extension
