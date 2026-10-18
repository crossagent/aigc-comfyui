# 工具安装目录

工作区的目录设计不依赖具体平台，目前统一使用 ComfyUI。`ComfyUI/` 是单独的上游源码检出，不进入主仓库；目标版本固定在 `comfyui.lock.json`。

`comfyui-model-paths.yaml` 把本仓库的 `assets/models/comfyui/` 添加为 ComfyUI 模型搜索路径。安装与运行方法见 [Linux 部署说明](../docs/deploy-linux.md)。本机历史安装、旧脚本、虚拟环境、缓存及日志不进入主仓库。

输入和输出目录通过 ComfyUI 启动参数指向 `assets/comfyui-input/` 和 `assets/comfyui-output/`。模型与资产二进制文件保持在 Git 之外。
