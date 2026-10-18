# ComfyUI 环境约定

新机器统一使用官方 ComfyUI 源码版，版本由 [comfyui.lock.json](../platforms/comfyui.lock.json) 固定为 `v0.41.0`（commit `98cc0bf84b7cb1383654c5b402e7612d875d6d22`）。不安装 Desktop。该版本包含 MiniMax-H3 原生节点；ComfyUI 官方 H3 文档要求基础工作流至少 `0.30.0`。

上游源码独立检出在 `platforms/ComfyUI/`，不进入本仓库。模型路径由 [comfyui-model-paths.yaml](../platforms/comfyui-model-paths.yaml) 指向 `assets/models/comfyui/`；输入、输出由启动参数指向 `assets/comfyui-input/` 和 `assets/comfyui-output/`。模型、素材、生成结果均留在 Git 之外。

新 Linux + NVIDIA 虚拟机的安装命令见 [部署说明](deploy-linux.md)。本机旧 ComfyUI 检出仍可用于历史任务，但不作为可迁移环境的版本依据；本仓库不携带其补丁、硬编码 Windows 路径的脚本或试验工作流。

MiniMax-H3 的开源权重尚未在本工作区完成实际生成验收，因此现在仅引用 [ComfyUI 官方 H3 工作流指南](https://docs.comfy.org/tutorials/video/minimax/minimax-h3)。完成新机器实测后，再将对应工作流和验证证据加入 `workflows/comfyui/validated/`。
