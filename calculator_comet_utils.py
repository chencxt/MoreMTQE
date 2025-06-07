import json
from comet import download_model, load_from_checkpoint

def calculate_comet_scores(output_file_path, model_directory):
    """
    计算COMET评分并更新JSON文件。

    参数:
    - output_file_path: JSON文件路径
    - model_directory: 模型下载保存路径
    """
    # 下载并加载COMET模型
    try:
        # 先尝试下载模型（如果本地不存在）
        comet_model_path = download_model("Unbabel/wmt22-cometkiwi-da", saving_directory=model_directory)
        # 加载模型
        comet_model = load_from_checkpoint(comet_model_path)
    except Exception as model_error:
        print(f"COMET模型加载失败：{model_error}")
        exit(1)

    # 加载JSON文件
    with open(output_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 遍历translations并计算COMET评分
    for translation in data["translations"]:
        src = translation["original"]
        mt = translation["translation"]
        comet_score = comet_model.predict([{"src": src, "mt": mt}])[0][0]  # 提取单一值
        translation["score-COMET"] = comet_score  # 添加COMET评分

    # 保存更新后的JSON文件
    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("已更新文件：添加COMET评分")