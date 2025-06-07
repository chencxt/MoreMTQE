import matplotlib.pyplot as plt
from matplotlib import rcParams

def plot_similarity_scores(nums, scores, average_score, output_path="similarity_scores_chart.png"):
    """
    绘制相似度评分的柱状图
    
    Args:
        nums: 编号列表
        scores: 相似度评分列表
        average_score: 平均分
        output_path: 输出图片路径
    """
    # 设置支持中文的字体
    rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
    rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    
    plt.figure(figsize=(10, 6))
    bar_color = "#1f77b4"  # 默认柱状图颜色
    line_color = "#ff7f0e"  # 默认线条颜色
    background_color = "#f9f9f9"  # 默认背景颜色
    
    # 根据得分是否低于平均值设置颜色
    bar_colors = [bar_color if score >= average_score else "red" for score in scores]
    plt.bar(nums, scores, color=bar_colors, label="相似度评分")
    plt.axhline(y=average_score, color=line_color, linestyle="--", label=f"平均值: {average_score:.4f}")
    
    # 在每个柱状图顶部显示具体值
    for i, score in enumerate(scores):
        plt.text(nums[i], score, f"{score:.2f}", ha="center", va="bottom", fontsize=5)
    
    # 设置图表样式
    plt.title("原文与译文相似度评分", fontsize=14)
    plt.xlabel("编号 (num)", fontsize=12)
    plt.ylabel("相似度评分", fontsize=12)
    plt.xticks(nums, fontsize=7)
    plt.yticks(fontsize=7)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.gca().set_facecolor(background_color)
    plt.legend()
    
    # 显示图表
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"图表已保存为图片：{output_path}")