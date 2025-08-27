# --------------------------------------------------------#
#   该文件用于生成每张图片的SOD指标，便于Origin使用
# --------------------------------------------------------#
import os
import cv2
from tqdm import tqdm
import csv
from py_sod_metrics import MAE, Emeasure, Fmeasure, Smeasure, WeightedFmeasure

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# 定义 CSV 文件路径
csv_path = './origin/ERPNet'
csv_file_name = "ERPNet_metrics.csv"
csv_file_path = os.path.join(csv_path, csv_file_name)

# 创建并初始化 CSV 文件
with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([
        "Image", "Smeasure", "MAE", "adpEm", "meanEm", "maxEm",
        "adpFm", "meanFm", "maxFm"
    ])


def SOD_Eval(pred_root, mask_root):
    mask_name_list = sorted(os.listdir(mask_root))
    FM = Fmeasure()
    SM = Smeasure()
    EM = Emeasure()
    M = MAE()

    with open(csv_file_path, 'a', newline='', encoding='utf-8-sig') as csv_file:
        csv_writer = csv.writer(csv_file)

        for mask_name in tqdm(mask_name_list, total=len(mask_name_list)):
            mask_path = os.path.join(mask_root, mask_name)
            pred_path = os.path.join(pred_root, mask_name)
            mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
            pred = cv2.imread(pred_path, cv2.IMREAD_GRAYSCALE)

            FM.step(pred=pred, gt=mask)
            SM.step(pred=pred, gt=mask)
            EM.step(pred=pred, gt=mask)
            M.step(pred=pred, gt=mask)

            fm = FM.get_results()["fm"]
            sm = SM.get_results()["sm"]
            em = EM.get_results()["em"]
            mae = M.get_results()["mae"]

            results = {
                "Smeasure": "{:.4f}".format(sm),
                "MAE": "{:.4f}".format(mae),
                "adpEm": "{:.4f}".format(em["adp"]),
                "meanEm": "{:.4f}".format(em["curve"].mean()),
                "maxEm": "{:.4f}".format(em["curve"].max()),
                "adpFm": "{:.4f}".format(fm["adp"]),
                "meanFm": "{:.4f}".format(fm["curve"].mean()),
                "maxFm": "{:.4f}".format(fm["curve"].max()),
            }

            # 将每张图片的结果写入 CSV
            csv_writer.writerow([
                mask_name, results["Smeasure"], results["MAE"],
                results["adpEm"], results["meanEm"], results["maxEm"],
                results["adpFm"], results["meanFm"], results["maxFm"]
            ])

            print(f"Processed {mask_name}: {results}")

    # 打印整体结果
    print("All images processed and results saved to CSV.")
    return


if __name__ == '__main__':
    pred_root = './origin/EORSSD/'  # 预测结果文件夹路径
    mask_root = './origin/GT/'  # 标签文件夹路径
    SOD_Eval(pred_root, mask_root)
