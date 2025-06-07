@echo on

cls
:: cls：清屏命令，用于清空命令行窗口中之前的输出内容

set HF_ENDPOINT=https://hf-mirror.com
:: set HF_ENDPOINT=https://hf-mirror.com：通过 CMD 设置环境变量 HF_ENDPOINT
:: 此环境变量在当前批处理脚本及其子进程中有效

.\python-3.12.8-embed-amd64\python.exe WebUI.py
:: 调用指定目录下的 Python 可执行文件运行 WebUI.py 脚本
:: .\python-3.12.8-embed-amd64\python.exe：这是 Python 嵌入式版本的路径
:: WebUI.py：要运行的 Python 脚本，假设它位于当前工作目录下

echo.
:: echo.：输出一个空行，使界面美观

pause
:: pause：命令行阻塞，提示“Press any key to continue . . .”，等待用户按下任意键再退出
:: 这是阻断功能的一部分，用于确保用户能看到上方输出结果
