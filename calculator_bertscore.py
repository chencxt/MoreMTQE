import torch
from transformers import XLMRobertaTokenizer, XLMRobertaModel
from bert_score import BERTScorer
import json
from tqdm import tqdm

def calculate_bertscore(source_text, translated_text, model_path):
    """
    计算 BERTScore 的 F1 得分。

    参数:
    - source_text: 原文列表
    - translated_text: 译文列表
    - model_path: 本地模型路径

    返回:
    - F1 平均得分
    """
    # 加载本地模型
    tokenizer = XLMRobertaTokenizer.from_pretrained(model_path)
    model = XLMRobertaModel.from_pretrained(model_path)

    # 初始化 BERTScorer（禁用基准分数 rescale_with_baseline=False）
    scorer = BERTScorer(
        model_type="xlm-roberta-large",
        lang="zh",  # 目标语言=中文
        rescale_with_baseline=False,  # 禁用基准分数
        device='cuda' if torch.cuda.is_available() else 'cpu'
    )

    # 计算 BERTScore
    _, _, F1 = scorer.score(source_text, translated_text)

    # 返回 F1 平均得分
    return F1.mean().item()

def process_and_write_bertscore(json_input_path, json_output_path, model_path):
    """
    从输入 JSON 文件读取原文和译文，计算 BERTScore 的 F1 得分，并写入输出 JSON 文件。

    参数:
    - json_input_path: 输入 JSON 文件路径
    - json_output_path: 输出 JSON 文件路径
    - model_path: 本地模型路径
    """
    # 读取输入 JSON 文件
    with open(json_input_path, "r", encoding="utf-8") as f:
        translations_data = json.load(f)

    # 读取输出 JSON 文件
    with open(json_output_path, "r", encoding="utf-8") as f:
        output_data = json.load(f)

    # 遍历每个条目，计算 BERTScore 的 F1 得分
    for entry in tqdm(translations_data["translations"], desc="计算 BERTScore 进度"):
        source_text = [entry["original"]]
        translated_text = [entry["translation"]]

        # 调用 calculate_bertscore 函数
        f1_score = calculate_bertscore(source_text, translated_text, model_path)

        # 在 output_data 中找到对应条目并插入 score-BERTScore-F1 键值对
        for output_entry in output_data["translations"]:
            if output_entry["original"] == entry["original"] and output_entry["translation"] == entry["translation"]:
                # 确保写在 score-COMET 键值对的下一行
                if "score-COMET" in output_entry:
                    comet_score = output_entry.pop("score-COMET")
                    output_entry["score-COMET"] = comet_score
                output_entry["score-BERTScore-F1"] = f1_score

    # 将更新后的数据写回输出 JSON 文件
    with open(json_output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f"已更新文件：{json_output_path}")
