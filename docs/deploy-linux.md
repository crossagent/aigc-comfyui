# Linux + NVIDIA 部署

此文档给新虚拟机上的操作者提供可复现的安装路径；模型和素材按需从原始来源或资产存储恢复。以下命令假定已安装 Git、Python 3.12 或 3.13、Python venv，并且 NVIDIA 驱动可由 `nvidia-smi` 检测。

## 获取工程和 ComfyUI

```bash
git clone https://github.com/crossagent/aigc-comfyui.git
cd aigc-comfyui
git clone https://github.com/Comfy-Org/ComfyUI.git platforms/ComfyUI
git -C platforms/ComfyUI checkout --detach 98cc0bf84b7cb1383654c5b402e7612d875d6d22
git -C platforms/ComfyUI rev-parse HEAD
python3 -c 'import sys; assert sys.version_info[:2] in {(3, 12), (3, 13)}, f"Use Python 3.12 or 3.13, got {sys.version}"'
python3 -m venv platforms/ComfyUI/.venv
platforms/ComfyUI/.venv/bin/python -m pip install --upgrade pip
platforms/ComfyUI/.venv/bin/python -m pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu130
platforms/ComfyUI/.venv/bin/python -m pip install -r platforms/ComfyUI/requirements.txt brotlicffi "huggingface_hub[cli]"
platforms/ComfyUI/.venv/bin/python -c 'import torch; assert torch.cuda.is_available(), "CUDA unavailable"; print(torch.__version__, torch.cuda.get_device_name(0))'
```

上游 [ComfyUI 手动安装说明](https://github.com/Comfy-Org/ComfyUI/blob/v0.41.0/README.md#manual-install-windows-linux) 推荐 NVIDIA 使用稳定版 CUDA 13.0 PyTorch。若系统默认 `python3` 不是 3.12 或 3.13（例如 3.14），需显式调用 `python3.12 -m venv platforms/ComfyUI/.venv` 或 `uv venv --python 3.12 platforms/ComfyUI/.venv`。安装 `brotlicffi` 可规避部分 Linux 主机预装 C 版 `brotli` 导致的 `httpx2` 解压参数异常。国内机器下载模型前建议设置国内镜像：`export HF_ENDPOINT=https://hf-mirror.com`；pip 亦可使用国内源（如 `https://mirrors.aliyun.com/pypi/simple/`）。GPU 驱动、显存及 Python 版本必须与所选 PyTorch 发行版匹配；不通过更换模型或盲目调整参数掩盖安装错误。

## 接入本仓库目录

```bash
mkdir -p assets/models/comfyui/{diffusion_models,text_encoders,vae,loras,embeddings,model_patches,unet,clip}
python3 assets/catalog.py verify
task_name=example-task
mkdir -p "tasks/$task_name/comfyui/input" "tasks/$task_name/comfyui/output"
cd platforms/ComfyUI
.venv/bin/python main.py --listen 127.0.0.1 --port 8188 \
  --extra-model-paths-config ../comfyui-model-paths.yaml \
  --input-directory "../../tasks/$task_name/comfyui/input" \
  --output-directory "../../tasks/$task_name/comfyui/output"
# 可选启动冒烟测试验证环境与目录加载：在上述命令后附加 --quick-test-for-ci 并在通过后自动退出
```

将 `example-task` 换成当前任务在 `tasks/` 下的路径；每个任务使用自己的 ComfyUI 输入与输出目录。长期复用的原件留在 `assets/`，需要时使用 `python3 assets/catalog.py stage <资产ID> --task <任务路径>` 投放到任务输入目录。模型路径配置已设 `is_default: true`，以其 YAML 文件所在的 `platforms/` 目录解析相对路径，使 ComfyUI 默认读写 `assets/models/comfyui/`。远程机器可以通过 SSH 端口转发访问 Web 界面：`ssh -L 8188:127.0.0.1:8188 <远程登录信息>`，然后在本机打开 `http://127.0.0.1:8188`。不要将未认证的 ComfyUI 服务直接公开到互联网。

## 工作流与模型

先读 [已验证工作流目录](../workflows/comfyui/README.md) 和每个工作流的模型清单。`assets/catalog.json` 初始为空，表示尚无随仓库登记的可复用原始素材；缺失的模型或素材必须显式恢复并校验。

MiniMax-H3 使用 ComfyUI **Template Library → Video → MiniMax H3 → Text to Video**（`video_minimax_h3_t2v`）官方模板。官方 [H3 指南](https://docs.comfy.org/tutorials/video/minimax/minimax-h3)说明该模板需要 ComfyUI 0.30.0 以上。模板内子图连接了 `LoraLoaderModelOnly`，即便关闭 `Enable Lightning LoRA`，ComfyUI 提交校验仍要求 8 步 LoRA 文件在盘；模板默认引用的 5 个文件合计约 42.0 GB（十进制，39.1 GiB），若将文本编码器换为 `qwen3vl_32b_minimax_h3_int8_convrot.safetensors`（27.1 GB）则合计约 53.5 GB（十进制）。建议数据盘留出至少 70 GB 给权重、下载缓存和结果。可直接使用虚拟环境自带的 `hf` CLI 拉取至 `assets/models/comfyui/`：

```bash
platforms/ComfyUI/.venv/bin/hf download Comfy-Org/MiniMax-H3 \
  diffusion_models/minimax_h3_fl2va_pruned_int8_convrot.safetensors \
  text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors \
  vae/minimax_h3_video_vae_int8_convrot.safetensors \
  vae/minimax_h3_audio_vae_fp32.safetensors \
  loras/minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors \
  --local-dir assets/models/comfyui
```

| 相对路径（`assets/models/comfyui/` 下） | 字节数 | SHA-256 |
| --- | ---: | --- |
| `diffusion_models/minimax_h3_fl2va_pruned_int8_convrot.safetensors` | 20970379616 | `e889202c41dafb67b10d67b97f0d8541508036a6090af23425a5c2615d03c47a` |
| `text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` | 15687142551 | `35a88d51044231fe332301d7a62aa81e3f2cba62febeb446e2c1e3e0ef76f2c6` |
| `vae/minimax_h3_video_vae_int8_convrot.safetensors` | 2811065184 | `52a2c8c73583c86e4f41cdcce3a6ad0ea562987bc0bf3d60a0cef5f5c8e60c0e` |
| `vae/minimax_h3_audio_vae_fp32.safetensors` | 605254808 | `8e505d95dd1561d47abd43d4238fd40d9bb1ae9e147ed0a4cba778d76ae4db48` |
| `loras/minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors` | 1956193000 | `2339acdf19bfe123f46b971ea35d367a84adb85de43627e1eceafa5a5b2b111e` |

官方模板顶层 `ResolutionSelector` 默认处于快速预览尺寸（`0.2` MP，`608×352`）；跑全尺寸 16:9 原生画幅（`1344×768`，短边 768px）时需将 `Megapixels` 设为 `0.98`（勿用 `1.0`，其输出 `1376×768` 超出模型 `1344×768` 像素上限）。模型文件不加入 Git。该工作流待新机器完成真实生成验收后，再标为本仓库的已验证工作流。
