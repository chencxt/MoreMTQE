import gradio as gr
import io
import sys
import contextlib

def run_code():
    # 创建一个 StringIO 对象来捕获 print 输出
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        # 模拟终端输出
        print("程序正在运行...")
        for i in range(3):
            print(f"第 {i+1} 步完成")
        print("任务完成！")
    output = buffer.getvalue()
    return output

with gr.Blocks() as demo:
    output_box = gr.Textbox(label="终端输出", lines=10)
    run_button = gr.Button("运行程序")

    run_button.click(fn=run_code, outputs=output_box)

demo.launch()
