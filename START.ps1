Clear-Host
# Clear-Host：清空 PowerShell 窗口中的之前输出，等同于命令行中的 cls。

$env:HF_ENDPOINT = "https://hf-mirror.com"
# $env:HF_ENDPOINT = "https://hf-mirror.com"：设置 PowerShell 环境变量，指定 Hugging Face 镜像加速地址。
# 该环境变量在当前 PowerShell 会话及其子进程中有效。

.\python-3.12.8-embed-amd64\python.exe WebUI.py
# .\python-3.12.8-embed-amd64\python.exe WebUI.py：调用指定路径的 Python 可执行文件运行 WebUI.py 脚本。
# 假设 Python 可执行文件及 WebUI.py 脚本位于当前工作目录下。

Write-Host "程序终止完毕"
# Write-Host ""：使界面更加整洁。

Read-Host "Press Enter to exit; 请按任意键退出"
# Read-Host "Press Enter to exit"：暂停脚本并显示提示信息“Press Enter to exit”，
# 等待用户按下回车键后退出 PowerShell 窗口。
