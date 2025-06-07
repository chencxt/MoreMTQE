import os
import json
from sentence_transformers import SentenceTransformer, util

def calculate_and_save_similarity(model_path, input_json_path, output_json_path):
    """
    计算文本相似度并保存结果到JSON文件
    
    Args:
        model_path (str): SentenceTransformer模型路径
        input_json_path (str): 输入JSON文件路径
        output_json_path (str): 输出JSON文件路径
        
    Returns:
        tuple: (scores列表, nums列表, 平均分数)
    """
    # 检查模型路径
    if not os.path.exists(model_path) or not os.listdir(model_path):
        raise ValueError(f"模型路径无效或为空：{model_path}")
    
    # 加载模型
    model = SentenceTransformer(model_path)
    
    # 读取输入JSON文件
    if not os.path.exists(input_json_path):
        raise FileNotFoundError(f"文件不存在：{input_json_path}")
        
    with open(input_json_path, "r", encoding="utf-8") as file:
        data = json.load(file).get("translations", [])
    
    # 检查数据格式
    if not isinstance(data, list):
        raise ValueError("JSON文件格式错误，期望是一个列表")
    
    # 初始化存储相似度评分的列表
    score_TST = []
    nums = []
    
    # 逐个计算相似度
    for item in data:
        num = item.get("num")
        original = item.get("original")
        translation = item.get("translation")
        
        if not all([num, original, translation]):
            print(f"数据项缺少必要字段：{item}")
            continue
        
        # 编码并计算相似度
        embeddings = model.encode([original, translation], convert_to_tensor=True)
        score_TST_item = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()
        score_TST.append(score_TST_item)
        nums.append(num)
    
    # 计算平均相似度
    average_score = sum(score_TST) / len(score_TST) if score_TST else 0
    
    # 创建输出数据
    output_data = {"translations": []}
    for item, score_TST_item in zip(data, score_TST):
        item_with_score_TST = item.copy()
        item_with_score_TST["score-TST"] = score_TST_item
        output_data["translations"].append(item_with_score_TST)
    
    # 写入输出文件
    with open(output_json_path, "w", encoding="utf-8") as output_file:
        json.dump(output_data, output_file, ensure_ascii=False, indent=4)
    
    return score_TST, nums, average_score