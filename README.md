# aigc comfyui 工程环境

工作区按任务、资产、工作流和工具安装划分目录。目录组织不依赖特定生成平台；目前统一使用 ComfyUI。

| 目录 | 内容 |
| --- | --- |
| [assets/](assets/README.md) | 可复用的原始参考、模型和骨架 |
| [tasks/](tasks/README.md) | 各任务的输入、中间参考、实验和成品 |
| [workflows/](workflows/README.md) | 当前使用的 ComfyUI 工作流 |
| [platforms/](platforms/README.md) | 工具安装和工作区维护脚本 |
| [docs/](docs/git-scope.md) | Git 范围与部署说明 |

模型和素材保存在 `assets/`，任务专属的输入与生成结果保存在 `tasks/`。经验证的 ComfyUI 工作流位于 `workflows/comfyui/validated/`，ComfyUI 源码安装目录为 `platforms/ComfyUI/`。具体目录约定见各目录的 README。
