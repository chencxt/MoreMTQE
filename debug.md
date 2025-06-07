第一次记录：无法加载模型。
    git clone https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2

    PS F:\CodeWorkspace\Python\STSspirit> & C:/Users/OMEN/AppData/Local/Programs/Python/Python312/python.exe f:/CodeWorkspace/Python/STSspirit/main.py
    从指定路径加载模型： F:/CodeWorkspace/Python/STSspirit/models--sentence-transformers--paraphrase-multilingual-mpnet-base-v2
    No sentence-transformers model found with name F:/CodeWorkspace/Python/STSspirit/models--sentence-transformers--paraphrase-multilingual-mpnet-base-v2. Creating a new one with mean pooling.
    Traceback (most recent call last):
    File "f:\CodeWorkspace\Python\STSspirit\main.py", line 28, in <module>
        model = SentenceTransformer(model_name_or_path)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "C:\Users\OMEN\AppData\Local\Programs\Python\Python312\Lib\site-packages\sentence_transformers\SentenceTransformer.py", line 321, in __init__ 
        modules = self._load_auto_model(
                ^^^^^^^^^^^^^^^^^^^^^^
    File "C:\Users\OMEN\AppData\Local\Programs\Python\Python312\Lib\site-packages\sentence_transformers\SentenceTransformer.py", line 1606, in _load_auto_model
        transformer_model = Transformer(
                            ^^^^^^^^^^^^
    File "C:\Users\OMEN\AppData\Local\Programs\Python\Python312\Lib\site-packages\sentence_transformers\models\Transformer.py", line 81, in __init__   
        self._load_model(model_name_or_path, config, cache_dir, backend, is_peft_model, **model_args)
    File "C:\Users\OMEN\AppData\Local\Programs\Python\Python312\Lib\site-packages\sentence_transformers\models\Transformer.py", line 181, in _load_model
        self.auto_model = AutoModel.from_pretrained(
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "C:\Users\OMEN\AppData\Local\Programs\Python\Python312\Lib\site-packages\transformers\models\auto\auto_factory.py", line 564, in from_pretrained
        return model_class.from_pretrained(
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "C:\Users\OMEN\AppData\Local\Programs\Python\Python312\Lib\site-packages\transformers\modeling_utils.py", line 3730, in from_pretrained       
        raise EnvironmentError(
    OSError: Error no file named pytorch_model.bin, model.safetensors, tf_model.h5, model.ckpt.index or flax_model.msgpack found in directory F:/CodeWorkspace/Python/STSspirit/models--sentence-transformers--paraphrase-multilingual-mpnet-base-v2.


    原因：下载时命令行窗口卡死，导致部分文件没有下载完全。
    解决：重新下载，并检查完整性之后重新运行（记得把路径都改成“/”）

第二次记录：参考用的长句子：
1、『１０人の妹と過ごす１ヵ月のサバイバル生活で何も起こらぬハズはなく』コンビニくじ十番勝負

《与10位妹妹度过为期一个月的生存生活，不可能不发生点什么吧》便利商店抽奖十番胜负

「《和十個妹妹的刺激生存戰》便利商店抽獎大對決！」

机翻：在与十个妹妹一起度过一个月的生存生活中，不可能什么事情都不发生——便利店抽奖十次对决。


2、今後のナタリーちゃんと旅人さんの関係にちょっと関わって来る予定です!!

第三次记录：'''
需要迁移的变量：
模型保存路径
算法的权重
'''

第四次记录：明天的任务：
    1、将绘图的功能封装为一个函数，扔到另一个py文件中（已完成）
    2、完成评分机制，引入https://github.com/Unbabel/COMET
        comet-score -s {source-inputs}.txt -t {translation-outputs}.txt -r {references}.txt --model Unbabel/XCOMET-XL
        comet-score -s 日文原文.txt -t 中文译文.txt -r comet.txt --model Unbabel/XCOMET-XL
        comet-score -s {source-input}.txt -t {translation-output}.txt --model Unbabel/wmt23-cometkiwi-da-xxl
        comet-score -s ja.txt -t zh.txt --model Unbabel/wmt23-cometkiwi-da-xxl



    3、制作一个gardio雏形出来。
    4、将json的得分键值对修改，引入之后分别记录语义相似度评分、comet评分
    5、添加专有名词替换方案，修正数据偏差


第5次记录：
bug修复：使用git clone克隆hugeface仓库报错：
```

第一步，登陆hugeface并授权同意相关仓库的用户协议

第二步，git clone https://<hf_username>:<hf_token>@huggingface.co/meta-llama/Llama-2-7b-chat-hf


```

第六次记录：
    https://packaging.pythonlang.cn/en/latest/guides/installing-using-pip-and-virtual-environments/
    使用虚拟环境之前，需要激活虚拟环境：.venv\Scripts\activate
    停用虚拟环境：deactivate

第七次记录：
    存在问题：终端的打印信息无法显示在gradio的文本窗口中
    pip freeze > requirements.txt 这个命令可以用于生成所需的代码环境需求包文档。
    或者也可以使用pip install pipreqs && pipreqs ./ --encoding=utf-8 --force

第八次记录：占用内存：4-5G，CPU推理。重点关注目录：C:\Users\OMEN\AppData\Roaming\Code\User\globalStorage\rooveterinaryinc.roo-cline\tasks

第九次记录：接下来的任务：解决requirements.txt和readme的完善（添加模型部分的说明），并发布到github。

第十次记录：已完成同设备异路径迁移测试，明天开始测试异设备系统完备性。另外添加一个图片：维恩图，用来说明标注颜色和翻译译文质量之间的区别。

嵌入式python需要指定python解释器路径然后再执行脚本。

$env:HF_ENDPOINT = "https://hf-mirror.com"
.\python-3.12.8-embed-amd64\python.exe WebUI.py

第十一次记录：正在使用镜像站 https://hf-mirror.com 下载模型...
Lightning automatically upgraded your loaded checkpoint from v1.8.2 to v2.5.1.post0. To apply the upgrade to your files permanently, run `python -m pytorch_lightning.utilities.upgrade_checkpoint F:\CodeWorkspace\Python\MoreMTQE\wmt22-cometkiwi-da\models--Unbabel--wmt22-cometkiwi-da\snapshots\1ad785194e391eebc6c53e2d0776cada8f83179a\checkpoints\model.ckpt`
主镜像站下载失败，尝试备用地址...
Lightning automatically upgraded your loaded checkpoint from v1.8.2 to v2.5.1.post0. To apply the upgrade to your files permanently, run `python -m pytorch_lightning.utilities.upgrade_checkpoint F:\CodeWorkspace\Python\MoreMTQE\wmt22-cometkiwi-da\models--Unbabel--wmt22-cometkiwi-da\snapshots\1ad785194e391eebc6c53e2d0776cada8f83179a\checkpoints\model.ckpt`
COMET模型加载失败：(MaxRetryError("HTTPSConnectionPool(host='huggingface.co', port=443): Max retries exceeded with url: /api/models/microsoft/infoxlm-large/tree/main/additional_chat_templates?recursive=False&expand=False (Caused by ConnectTimeoutError(<urllib3.connection.HTTPSConnection object at 0x00000175D9B8E660>, 'Connection to huggingface.co timed out. (connect timeout=None)'))"), '(Request ID: a18cd9ae-8838-46d2-a0ac-9963753d653e)')
请检查网络连接或手动下载模型。

这种情况可以使用镜像站环境变量，或者直接在download_model和load_from_checkpoint这两函数里面把local_files_only选项打开，直接跳过网页验证使用本地模型。

第十二次记录：不使用GPU加速的情况下，可以直接删除xlm-roberta-large中的pytorch_model.bin文件。目前并未影响使用。



---

## 📝 Bug 记录文档：ModuleNotFoundError - 无法导入同目录下的文件模块

### 📌 问题概述

- **报错信息：**

```
ModuleNotFoundError: No module named 'main'
```

- **执行命令：**

```bash
F:\CodeWorkspace\Python\MoreMTQE\python-3.12.8-embed-amd64>python F:\CodeWorkspace\Python\MoreMTQE\WebUI.py
```

- **项目结构：**

```
MoreMTQE/
├── python-3.12.8-embed-amd64/
├── main.py
└── WebUI.py
```

### 🎯 原因分析

当使用 **Python Embedded（嵌入式版本）** 运行脚本时，Python 默认不会自动将脚本所在目录加入模块搜索路径 `sys.path`，导致即使 `main.py` 与 `WebUI.py` 同目录，也无法使用：

```python
from main import process_similarity_and_scores
```

### ✅ 解决方案

#### ✅ 方法一（已采用 ✅）：手动添加脚本所在路径到 `sys.path`

**修改位置：`WebUI.py` 开头处，导入语句之前**

```python
import sys
import os

# ✅ 将当前脚本所在目录加入模块搜索路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import process_similarity_and_scores
```

此方法确保 Python 能正确解析并加载 `main.py` 模块，无需更改工作目录或使用 `-m` 参数。

---

### 🧠 经验总结

- 嵌入式 Python 不自动配置模块路径，使用时需手动管理 `sys.path`。
- 可以将公共路径写入一个通用的导入配置文件，例如 `bootstrap.py`，集中管理路径注入逻辑。
- 更稳妥的做法是：统一用包结构 + `python -m` 执行方式，这样 Python 会以模块模式运行，路径解析更标准。

---

