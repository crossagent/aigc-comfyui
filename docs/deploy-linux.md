# Linux + NVIDIA 部署

此文档给新虚拟机上的操作者提供可复现的安装路径；模型和素材按需从原始来源或资产存储恢复。以下命令假定已安装 Git、Python 3.12 或 3.13、Python venv，并且 NVIDIA 驱动可由 `nvidia-smi` 检测。本仓库为私有仓库，新机器克隆前需要配置 GitHub 登录或只读 deploy key；凭据不可写入本仓库。

## 获取工程和 ComfyUI

```bash
git clone https://github.com/crossagent/aigc-comfyui.git
cd aigc-comfyui
git clone https://github.com/Comfy-Org/ComfyUI.git platforms/ComfyUI
git -C platforms/ComfyUI checkout --detach 98cc0bf84b7cb1383654c5b402e7612d875d6d22
git -C platforms/ComfyUI rev-parse HEAD
python3 -m venv platforms/ComfyUI/.venv
platforms/ComfyUI/.venv/bin/python -m pip install --upgrade pip
platforms/ComfyUI/.venv/bin/python -m pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu130
platforms/ComfyUI/.venv/bin/python -m pip install -r platforms/ComfyUI/requirements.txt
platforms/ComfyUI/.venv/bin/python -c 'import torch; assert torch.cuda.is_available(), "CUDA unavailable"; print(torch.__version__, torch.cuda.get_device_name(0))'
```

上游 [ComfyUI 手动安装说明](https://github.com/Comfy-Org/ComfyUI/blob/v0.41.0/README.md#manual-install-windows-linux) 推荐 NVIDIA 使用稳定版 CUDA 13.0 PyTorch。GPU 驱动、显存及 Python 版本必须与所选 PyTorch 发行版匹配；不通过更换模型或盲目调整参数掩盖安装错误。

## 接入本仓库目录

```bash
mkdir -p assets/comfyui-input assets/comfyui-output
mkdir -p assets/models/comfyui/{diffusion_models,text_encoders,vae,loras,unet,clip}
python3 assets/catalog.py verify
cd platforms/ComfyUI
.venv/bin/python main.py --listen 127.0.0.1 --port 8188 \
  --extra-model-paths-config ../comfyui-model-paths.yaml \
  --input-directory ../../assets/comfyui-input \
  --output-directory ../../assets/comfyui-output
```

模型路径配置以其 YAML 文件所在的 `platforms/` 目录解析相对路径。远程机器可以通过 SSH 端口转发访问 Web 界面：`ssh -L 8188:127.0.0.1:8188 <远程登录信息>`，然后在本机打开 `http://127.0.0.1:8188`。不要将未认证的 ComfyUI 服务直接公开到互联网。

## 工作流与模型

先读 [已验证工作流目录](../workflows/comfyui/README.md) 和每个工作流的模型清单。`assets/catalog.json` 初始为空，表示尚无随仓库登记的可复用原始素材；缺失的模型或素材必须显式恢复并校验。

MiniMax-H3 使用 ComfyUI **Template Library → Video → MiniMax H3 → Text to Video** 官方模板。官方 [H3 指南](https://docs.comfy.org/tutorials/video/minimax/minimax-h3)说明该模板需要 ComfyUI 0.30.0 以上，并提供模型下载入口。T2V 的主模型、文本编码器、音频 VAE、int8 视频 VAE合计约 51.5 GB（十进制）；若使用 8 步 LoRA，再增加约 2.0 GB。建议数据盘留出至少 70 GB 给权重、下载过程和结果。模型文件不加入 Git。该工作流目前尚未做新机器生成验收，不能标为本仓库的已验证工作流。
