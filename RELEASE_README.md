# MoreMTQE 发行版使用说明

## 1. 环境要求

- Python 3.12 或更高版本
- 建议使用虚拟环境
- 至少8GB内存（实际运行会占用4GB内存，推荐16GB）
- 约12GB磁盘空间（主要用于存储预训练模型）

## 2. 安装步骤

1. 解压下载的发行版压缩包
2. 创建并激活Python虚拟环境（推荐）：
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```
3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 3. 目录结构

```
MoreMTQE/
├── main.py              # 命令行主程序
├── WebUI.py            # Web界面程序
├── calculator_*.py     # 计算模块
├── plot_utils.py       # 绘图工具
├── requirements.txt    # 依赖项
├── example/           # 示例文件
│   ├── Origin.txt     # 示例原文
│   └── Translation.txt # 示例译文
└── models/            # 预训练模型目录
    ├── paraphrase-multilingual-mpnet-base-v2/
    ├── wmt22-cometkiwi-da/
    └── xlm-roberta-large/
```

## 4. 使用方法

### 4.1 使用Web界面（推荐）

1. 运行Web界面：
```bash
python WebUI.py
```
2. 在浏览器中打开显示的地址（默认为 http://localhost:7860）
3. 上传原文和译文文件，设置评估参数
4. 点击"开始评估"按钮

### 4.2 使用命令行

```bash
python main.py --origin Origin.txt --translation Translation.txt --tst-weight 0.1 --bert-weight 0.3 --comet-weight 0.6
```


---