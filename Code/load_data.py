import glob


def get_paths_data(datapath):
    fixed_landmarks_csv_list = sorted(
        glob.glob(f"{datapath}/BraTSReg_*_0000_landmarks.csv")
    )
    moving_landmarks_csv_list = sorted(
        glob.glob(f"{datapath}/BraTSReg_*_0262_landmarks.csv")
    )

    # Rutas de archivos de imágenes T1GD fijas y móviles
    fixed_t1ce_list = sorted(glob.glob(f"{datapath}/*/UPENN-GBM-*_11*_T1GD.nii.gz"))
    moving_t1ce_list = sorted(glob.glob(f"{datapath}/*/UPENN-GBM-*_21*_T1GD.nii.gz"))

    # Rutas de archivos de imágenes T2 fijas y móviles
    fixed_t2_list = sorted(glob.glob(f"{datapath}/*/UPENN-GBM-*_11*_T2.nii.gz"))
    moving_t2_list = sorted(glob.glob(f"{datapath}/*/UPENN-GBM-*_21*_T2.nii.gz"))

    # Repetir fixed_landmarks_csv_list para que tenga el tamaño de fixed_t1ce_list
    fixed_landmarks_csv_list = fixed_landmarks_csv_list * len(fixed_t1ce_list)
    moving_landmarks_csv_list = moving_landmarks_csv_list * len(fixed_t1ce_list)

    return (
        fixed_landmarks_csv_list,
        moving_landmarks_csv_list,
        fixed_t1ce_list,
        moving_t1ce_list,
        fixed_t2_list,
        moving_t2_list,
    )
