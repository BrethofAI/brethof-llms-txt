# ChatGLM3

> 一个由智谱AI与清华大学KEG实验室联合发布的开源对话预训练模型系列，支持多轮对话、工具调用、代码解释器和Agent任务等场景。

基于Python，通过pip安装依赖后可从Hugging Face或ModelScope下载模型权重，用transformers加载。提供综合Demo、命令行对话、Gradio/Streamlit网页版、LangChain集成以及OpenAI/ZhipuAI格式的API部署（api_server.py）。开源系列包括对话模型ChatGLM3-6B、基础模型ChatGLM3-6B-Base及长文本模型32K/128K版本，支持FP16、4-bit量化、CPU、Mac MPS和多卡部署；另有微调套件，权重对学术研究开放，登记后可免费商用。

## Docs

- [ChatGLM3](https://raw.githubusercontent.com/THUDM/ChatGLM3/main/README.md): ChatGLM3-6B 模型介绍、GLM-4 开源模型与 API 渠道、开源序列及社区资源链接。
- [GLM-4 开源模型和API](https://github.com/THUDM/ChatGLM3/blob/main/README.md#glm-4-开源模型和api): 体验 GLM-4 的渠道：开源 GLM-4-9B 模型、智谱清言、API 平台及 GLM-4 API 开源教程。
- [ChatGLM3 介绍](https://github.com/THUDM/ChatGLM3/blob/main/README.md#chatglm3-介绍): ChatGLM3-6B 的特性、开源模型序列、开源协议及免责声明。
- [模型列表](https://github.com/THUDM/ChatGLM3/blob/main/README.md#模型列表): 各模型在 Huggingface、ModelScope、WiseModel 上的发布与同步更新说明。
- [友情链接](https://github.com/THUDM/ChatGLM3/blob/main/README.md#友情链接): 支持 ChatGLM3-6B 的推理加速、高效微调与应用框架等优秀开源仓库列表。
- [评测结果](https://github.com/THUDM/ChatGLM3/blob/main/README.md#评测结果): ChatGLM3-6B 在 8 个中英文数据集上的性能测试及 ChatGLM3-6B-32K 长文本评估结果。
- [使用方式](https://github.com/THUDM/ChatGLM3/blob/main/README.md#使用方式): 环境安装、综合 Demo、代码调用与本地加载、模型微调、网页版与命令行 Demo、LangChain 及 OpenAI API 部署方法。
- [低成本部署](https://github.com/THUDM/ChatGLM3/blob/main/README.md#低成本部署): 模型量化、CPU、Mac MPS、多卡部署及 OpenVINO、TensorRT-LLM 加速推理的使用方法与显存需求。
- [Deployment](https://raw.githubusercontent.com/THUDM/ChatGLM3/main/DEPLOYMENT.md): 模型量化、CPU、Mac MPS 与多卡部署方法，含 accelerate 多 GPU 切分和 device_map 自定义。
- [Prompt](https://raw.githubusercontent.com/THUDM/ChatGLM3/main/PROMPT.md): ChatGLM3 对话格式规定，包括对话头 special token、多轮对话、工具调用与代码执行样例。
