import os
from calculator_similarity import calculate_and_save_similarity
from plot_utils import plot_similarity_scores
from transformers import BertTokenizer, BertModel, AutoModel, AutoTokenizer, XLMRobertaTokenizer, XLMRobertaModel
import json
from bert_score import BERTScorer
from calculator_comet_utils import calculate_comet_scores
from calculator_bertscore import process_and_write_bertscore
import sys

def process_similarity_and_scores(
    model_name_or_path,
    json_file_path,
    output_file_path,
    bert_model_path,
    model_directory
):
    """
    处理相似度计算、COMET评分和BERTScore处理的主函数。
    设置模型与json文件保存路径(此处很重要，不能随意修改！每个用户都需要修改这些变量):

    参数:
    - model_name_or_path: 语义相似度模型路径
    - json_file_path: 输入json文件的路径
    - output_file_path: 输出json文件的路径
    - bert_model_path: BERTScore模型的路径
    - model_directory: COMET模型的路径
    """
    # 创建一个列表来存储所有输出信息
    output_messages = []
    
    try:
        # 计算相似度并保存结果
        scores, nums, average_score = calculate_and_save_similarity(
            model_name_or_path,
            json_file_path,
            output_file_path
        )
        
        message = f"已生成文件：{output_file_path}"
        print(message)
        output_messages.append(message)
        
        # 调用封装的COMET评分函数
        calculate_comet_scores(output_file_path, model_directory)
        message = "COMET评分计算完成"
        print(message)
        output_messages.append(message)
        
        # 调用封装的 BERTScore 处理函数
        process_and_write_bertscore(json_file_path, output_file_path, bert_model_path)
        message = "BERTScore处理完成"
        print(message)
        output_messages.append(message)

        return "\n".join(output_messages)

    except Exception as e:
        error_message = f"发生错误：{str(e)}"
        print(error_message)
        return error_message
