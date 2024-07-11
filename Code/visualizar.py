import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import argparse
import glob

slice_num = 70


def imprimir_inferencia(
    serie, result="Result", recurrence=False, original=False, deformada=False
):
    global slice_num
    recurrence_t1ce_list = sorted(
        glob.glob("../Dataset/test/*/UPENN-GBM-*_21*_T1GD.nii.gz")
    )
    if recurrence:
        recurrence_t1ce_list = sorted(
            glob.glob("../Dataset/test/*/UPENN-GBM-*_21*_T1GD.nii.gz")
        )
        path_recurrence = recurrence_t1ce_list[serie - 1]
        path_base_deformated = f"../{result}/{serie}_X_Y.nii.gz"
        print("img", path_recurrence)
    else:
        base_t1ce_list = sorted(
            glob.glob("../Dataset/test/*/UPENN-GBM-*_11*_T1GD.nii.gz")
        )
        path_base = base_t1ce_list[serie - 1]

        if deformada:
            # T1GD deformada
            path_follow_deformated = f"../{result}/{serie}_Y_X.nii.gz"  # T1GD deformada
        else:
            # T1GD original
            path_follow_deformated = recurrence_t1ce_list[serie - 1]  # T1GD original

        # Segmentation file
        # segmentation_files = sorted(glob.glob("../Dataset/test/seg_out_*.npy"))
        # path_segmentation = segmentation_files[serie-1]
        segmentation_files = sorted(glob.glob("../segmentations/*.nii.gz"))
        path_segmentation = f"../segmentations/{serie-1}segmentation.nii.gz"
        print("img", path_base)

    if recurrence:
        img_add = path_base_deformated
        img_rec = path_recurrence
        label_add = f"../{result}/{serie}segmentation.nii.gz"
    else:
        img_add = path_base
        img_rec = path_follow_deformated
        if original:
            label_add = path_segmentation
            print("segmentación original")
        else:
            label_add = (
                f"../{result}/{serie}segmentation_back.nii.gz"  # path_segmentation
            )
            print("segmentación deformado")

    img = nib.load(img_add).get_fdata()
    img_rec = nib.load(img_rec).get_fdata()
    print("img_rec", img_rec.shape)

    if recurrence:
        seg_out = nib.load(label_add).get_fdata()
        seg_out = seg_out.squeeze()
    else:
        if original:
            # seg_out = np.load(label_add)
            seg_out = nib.load(label_add).get_fdata()
        else:
            seg_out = nib.load(label_add).get_fdata()  # np.load(label_add)
        seg_out = seg_out.squeeze()

    # print("seg_out", seg_out.shape)
    fig, ax = plt.subplots(2, 2, figsize=(12, 9))
    # Ajustar los espacios entre los subplots
    plt.subplots_adjust(
        left=0.05, right=0.95, top=0.95, bottom=0.05, wspace=0.05, hspace=0.05
    )

    # Hacer que los ejes ocupen todo el espacio disponible en la figura
    fig.tight_layout()
    fig.canvas.mpl_connect(
        "scroll_event", lambda event: scroll_slices(event, img.shape[2])
    )
    fig.canvas.mpl_connect(
        "key_press_event", lambda event: key_press(event, img.shape[2])
    )

    def update_slice(slice_num):
        ax[0, 0].clear()
        ax[0, 0].imshow(
            np.rot90(img[:, :, slice_num], k=-1),
            cmap="gray",
        )  # k=-1
        ax[0, 0].set_title("Image base")

        # GT segmentation
        # ax[0, 0].clear()
        # ax[0, 0].imshow(np.rot90(label[:, :, slice_num], k=-1))
        # ax[0, 0].set_title("label")

        ax[0, 1].clear()
        ax[0, 1].imshow(np.rot90(img[:, :, slice_num], k=-1), cmap="gray")
        ax[0, 1].imshow(np.rot90(seg_out[:, :, slice_num], k=-1), cmap="jet", alpha=0.3)
        ax[0, 1].set_title("nroi - froi - inter.")

        # ax[1, 0].clear()
        # ax[1, 0].imshow(np.rot90(seg[0][:, :, slice_num], k=-1))
        # ax[1, 0].set_title("Map nroi")

        ax[1, 1].clear()
        ax[1, 1].imshow(np.rot90(img_rec[:, :, slice_num], k=-1), cmap="gray")
        ax[1, 1].imshow(np.rot90(seg_out[:, :, slice_num], k=-1), cmap="jet", alpha=0.3)
        ax[1, 1].set_title("Recurrence Map nroi")

        ax[1, 0].clear()
        ax[1, 0].imshow(np.rot90(img_rec[:, :, slice_num], k=-1), cmap="gray")
        ax[1, 0].set_title(f"Recurrence slice {slice_num}")

        plt.draw()

    def scroll_slices(event, max_slices):
        global slice_num
        if event.button == "up":
            slice_num = (slice_num + 1) % max_slices
            update_slice(slice_num)
        elif event.button == "down":
            slice_num = (slice_num - 1) % max_slices
            update_slice(slice_num)

    def key_press(event, max_slices):
        global slice_num
        if event.key == "up":
            slice_num = (slice_num + 1) % max_slices
            update_slice(slice_num)
        elif event.key == "down":
            slice_num = (slice_num - 1) % max_slices
            update_slice(slice_num)

    update_slice(slice_num)
    plt.show()


def main():
    global slice_num
    parser = argparse.ArgumentParser(description="Visualizador de MRI")
    parser.add_argument("--serie", type=int, default=1, help="Número de serie")
    parser.add_argument(
        "--result", type=str, default="Result", help="Carpeta de resultados"
    )
    parser.add_argument(
        "--b",
        default=True,
        action="store_false",
        help="Colocar si queremos usar la deformacion Y_X",
    )
    parser.add_argument(
        "--o",
        default=False,
        action="store_true",
        help="Colocar si queremos ver la segmentacion original",
    )
    parser.add_argument(
        "--d",
        default=False,
        action="store_true",
        help="Colocar si queremos ver la imagen follow sin deformación",
    )
    args = parser.parse_args()

    # seg_out = np.load(f"inferences/seg_out_{str(args.serie).zfill(5)}.npy")
    # seg_out = nib.load(
    #     f"inferences/seg_out_{str(args.serie).zfill(5)}_t.nii.gz"
    # ).get_fdata()
    # seg_out = np.load(f"../{args.result}/{args.serie}.npy")
    # seg_out = nib.load(img_add).get_fdata()
    # slice = 70  # Slice inicial

    imprimir_inferencia(
        args.serie, args.result, recurrence=args.b, original=args.o, deformada=args.d
    )


if __name__ == "__main__":
    main()
