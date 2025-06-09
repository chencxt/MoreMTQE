import os
import sys
# 把当前脚本所在目录加入 sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import json
import gradio as gr
import plotly.graph_objects as go
import numpy as np
import subprocess
from main import process_similarity_and_scores
from transformers import BertTokenizer, BertModel, AutoModel, AutoTokenizer, XLMRobertaTokenizer, XLMRobertaModel
import json
from bert_score import BERTScorer




# 读取 outputINFO.json 数据
def load_data():
    with open("outputINFO.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data["translations"]

# 获取低于判断区间的数据点并排序
def get_below_interval_data(weight_tst, weight_comet, weight_bertscore):
    data = load_data()
    nums = [item["num"] for item in data]
    scores_tst = [item["score-TST"] for item in data]
    scores_comet = [item["score-COMET"] for item in data]
    scores_bertscore = [item["score-BERTScore-F1"] for item in data]

    # 计算加权平均数
    weighted_scores = [
        weight_tst * tst + weight_comet * comet + weight_bertscore * bertscore
        for tst, comet, bertscore in zip(scores_tst, scores_comet, scores_bertscore)
    ]

    # 计算平均值和标准差
    mean_score = np.mean(weighted_scores)
    std_dev = np.std(weighted_scores)
    lower_bound = mean_score - std_dev

    # 获取低于判断区间的数据点
    below_interval = [(num, score) for num, score in zip(nums, weighted_scores) if score < lower_bound]
    
    # 按加权得分从低到高排序
    below_interval.sort(key=lambda x: x[1])
    
    # 转换为HTML表格格式，添加样式
    if below_interval:
        table_html = """
        <style>
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 10px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
        }
        th {
            background-color: #f2f2f2;
            color: #333;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        </style>
        <table>
            <tr>
                <th>标红行数</th>
                <th>加权最终得分</th>
            </tr>
        """
        for num, score in below_interval:
            table_html += f"<tr><td>{num}</td><td>{score:.4f}</td></tr>"
        table_html += "</table>"
    else:
        table_html = "<p style='text-align: center; color: #666; padding: 20px;'>没有发现低于判断区间的数据点</p>"
    
    return table_html

# 制作交互式图表
def create_chart(weight_tst, weight_comet, weight_bertscore, bar_spacing):
    data = load_data()
    nums = [item["num"] for item in data]
    scores_tst = [item["score-TST"] for item in data]
    scores_comet = [item["score-COMET"] for item in data]
    scores_bertscore = [item["score-BERTScore-F1"] for item in data]

    # 计算加权平均数
    weighted_scores = [
        weight_tst * tst + weight_comet * comet + weight_bertscore * bertscore
        for tst, comet, bertscore in zip(scores_tst, scores_comet, scores_bertscore)
    ]

    # 计算平均值和标准差
    mean_score = np.mean(weighted_scores)
    std_dev = np.std(weighted_scores)
    lower_bound = mean_score - std_dev
    upper_bound = mean_score + std_dev

    # 创建柱状图
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=nums,
        y=scores_tst,
        name="TST Score",
        marker=dict(color="blue"),
        width=bar_spacing
    ))

    fig.add_trace(go.Bar(
        x=nums,
        y=scores_bertscore,
        name="BERTScore-F1",
        marker=dict(color="purple"),
        width=bar_spacing
    ))

    fig.add_trace(go.Bar(
        x=nums,
        y=scores_comet,
        name="COMET Score",
        marker=dict(color="green"),
        width=bar_spacing
    ))

    # 添加加权平均值折线
    fig.add_trace(go.Scatter(
        x=nums,
        y=weighted_scores,
        mode="lines+markers",
        name="Weighted Average",
        line=dict(color="orange", dash="dash"),
        marker=dict(size=8)
    ))

    # 根据区间标记数据点颜色
    for x, y in zip(nums, weighted_scores):
        if y < lower_bound:
            fig.add_trace(go.Scatter(
                x=[x],
                y=[y],
                mode="markers",
                marker=dict(color="red", size=10),
                name="Below Interval"
            ))
        elif y > upper_bound:
            fig.add_trace(go.Scatter(
                x=[x],
                y=[y],
                mode="markers",
                marker=dict(color="yellow", size=10),
                name="Above Interval"
            ))
        else:
            fig.add_trace(go.Scatter(
                x=[x],
                y=[y],
                mode="markers",
                marker=dict(color="green", size=10),
                name="Within Interval"
            ))

    # 添加平均值±标准差区间
    fig.add_shape(type="line", x0=min(nums), x1=max(nums), y0=mean_score, y1=mean_score,
                  line=dict(color="purple", dash="dash"), name="Mean")
    fig.add_shape(type="line", x0=min(nums), x1=max(nums), y0=lower_bound, y1=lower_bound,
                  line=dict(color="gray", dash="dash"), name="Mean - Std Dev")
    fig.add_shape(type="line", x0=min(nums), x1=max(nums), y0=upper_bound, y1=upper_bound,
                  line=dict(color="gray", dash="dash"), name="Mean + Std Dev")

    fig.update_layout(
        title="Interactive Translation Scores Chart",
        xaxis_title="Translation Number",
        yaxis_title="Score",
        barmode="group",
        legend_title="Legend",
        template="plotly_white"
    )

    return fig

# Gradio 界面
def display_chart(weight_tst, weight_comet, weight_bertscore, bar_spacing):
    fig = create_chart(weight_tst, weight_comet, weight_bertscore, bar_spacing)
    table = get_below_interval_data(weight_tst, weight_comet, weight_bertscore)
    return fig, table

# 创建 Gradio 界面
with gr.Blocks() as demo:
    with gr.Tab("翻译得分统计(读取outputINFO.json文件)"):
        with gr.Column():
            weight_tst_slider = gr.Slider(0, 1, step=0.05, value=0.2, label="Weight for TST: 语义相似度参数权重，主要用于单字、字词级别的翻译得分计算，无理解能力")
            weight_bertscore_slider = gr.Slider(0, 1, step=0.05, value=0.5, label="Weight for BERTScore-F1: BERTScore的F1参数权重，主要用于字词、段落级翻译得分计算，有理解能力")
            weight_comet_slider = gr.Slider(0, 1, step=0.05, value=0.5, label="Weight for COMET: COMET参数权重，主要用于句子、段落级翻译得分计算，有理解能力")
            bar_spacing_slider = gr.Slider(0.1, 1, step=0.1, value=0.4, label="Bar Spacing: 柱状图粗细调节，但您的所有数据均存储于outputINFO.json文件中，这里只是显示和统计")
        with gr.Column():
            hint_text = gr.Textbox(label="更多机器翻译质量评估-MoreMTQE-v1.1-TIPs", value="1、以上三个参数需要根据译文调节，比如，如果你的译文中长难句较多，那么Weight for COMET应该调高一点，其它两个应该适当调低，反之亦然。语义相似度不是MTQE问题的参考量所以Weight for TST无论何时都不能给高。\n2、最终得分仅供参考，不是说标红的数据点对应的那句就一定翻译的不好，只是翻译有误的概率偏高。也有可能只是“标点符号没对齐”或“这句话中的专有名词太多了”等意外情况")
            generate_button = gr.Button("Generate Chart")
        with gr.Row():
            chart_output = gr.Plot(label="Interactive Chart")
        with gr.Row():
            table_output = gr.HTML(label="低于判断区间的数据点")
        generate_button.click(
            display_chart,
            inputs=[weight_tst_slider, weight_comet_slider, weight_bertscore_slider, bar_spacing_slider],
            outputs=[chart_output, table_output]
        )
    with gr.Tab("翻译得分计算(生成outputINFO.json文件)"):
        with gr.Row():
            with gr.Column():
                hint_text = gr.Textbox(label="提示信息", value="请确保输入文件格式正确，原文命名为Origin.txt，译文命名为Translation.txt，放在与webui.py同目录下\n按顺序运行后将生成outputINFO.json 文件。")
                run_button_1 = gr.Button("1、运行 format_txt_to_json.py格式化txt为json")
                model_name_input = gr.Textbox(label="Model Name or Path: 语义相似度模型路径", value="./paraphrase-multilingual-mpnet-base-v2", interactive=True)
                json_file_input = gr.Textbox(label="JSON File Path: 输入json文件的路径。", value="formatted_translations.json", interactive=True)
                output_file_input = gr.Textbox(label="Output File Path: 输出json文件的路径", value="outputINFO.json", interactive=True)
                bert_model_input = gr.Textbox(label="BERT Model Path: BERTScore模型的路径。", value="./xlm-roberta-large", interactive=True)
                model_directory_input = gr.Textbox(label="Model Directory: COMET模型的路径。", value="./wmt22-cometkiwi-da", interactive=True)
                run_button_2 = gr.Button("2、运行main.py开始计算并输出outputINFO.json文件")
            with gr.Column():
                terminal_output = gr.Textbox(label="终端输出信息", lines=20)
        run_button_1.click(
            fn=lambda: subprocess.run(["python", "format_txt_to_json.py"], capture_output=True, text=True).stdout,
            inputs=[],
            outputs=terminal_output
        )
        run_button_2.click(
            fn=lambda model_name_or_path, json_file_path, output_file_path, bert_model_path, model_directory: process_similarity_and_scores(
                model_name_or_path, json_file_path, output_file_path, bert_model_path, model_directory
            ),
            inputs=[model_name_input, json_file_input, output_file_input, bert_model_input, model_directory_input],
            outputs=terminal_output
        )
    with gr.Tab("outputINFO.json文件查阅"):
        # 添加用于显示内容的文本框
        content_textbox = gr.Textbox(
            label="JSON内容显示区域",
            value="",
            lines=10,
            max_lines=20
        )
        
        with gr.Row():
            # 添加清空按钮
            clear_btn = gr.Button("清空文本框")
            # 添加读取JSON按钮
            read_json_btn = gr.Button("读取outputINFO.json")
            
        # 清空文本框的函数
        def clear_textbox():
            return ""
            
        # 读取JSON文件的函数
        def read_json_content():
            try:
                with open("outputINFO.json", "r", encoding="utf-8") as file:
                    data = json.load(file)
                    return json.dumps(data, ensure_ascii=False, indent=2)
            except Exception as e:
                return f"读取文件时发生错误: {str(e)}"
        
        # 绑定按钮点击事件
        clear_btn.click(
            fn=clear_textbox,
            outputs=content_textbox
        )
        read_json_btn.click(
            fn=read_json_content,
            outputs=content_textbox
        )
    with gr.Tab("Information"):
        hint_text = gr.Textbox(label="提示信息", value="MoreMTQE 是一个用于评估机器翻译质量的工具，需提供一一对应的原文（Origin.txt）和译文（Translation.txt）\n使用 TST（无理解能力，字符/词级）、BERTScore-F1（有理解能力，词/段落级）、COMET（有理解能力，句/段落级）三个指标进行评分\nTST 不适合高权重，因为语义相似度不是 MTQE 的核心\n若译文包含长难句，应提高 COMET 权重，适当降低另外两个\n若译文较简单，则可提升 BERTScore 权重\n最终得分仅供参考，标红句子可能翻译有误，也可能是标点错位或专有名词干扰\n在终端界面Ctrl+C可以关闭gradio服务", lines=7)
        gr.Image("img/schematic.png", label="MoreMTQE-v1.1流程图")
        gr.Image("img/Venn.png", label="翻译标注点结果与实际翻译可能性维恩图")


demo.launch()


