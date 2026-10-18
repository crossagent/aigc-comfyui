# 资产目录

| 目录 | 内容 |
| --- | --- |
| `originals/` | 跨任务复用的原始参考原件 |
| `models/comfyui/` | ComfyUI 模型权重的实际存储位置 |
| `rigs/` | 可复用的骨架与绑定资产 |
| `catalog.json` | 可复用原始素材的 ID、相对路径、来源、大小和 SHA-256；进入 Git |
| `catalog.py` | 注册、校验原件并投放到指定任务 ComfyUI 输入目录的命令行工具 |

资产二进制文件不进入 Git。新机器需要从原始来源或资产存储恢复文件，再运行 `python assets/catalog.py verify` 校验。已有原件可用 `python assets/catalog.py register <id> <文件> --source <来源>` 登记；运行工作流前用 `python assets/catalog.py stage <id> --task <任务路径>` 将已校验原件复制到 `tasks/<任务路径>/comfyui/input/`，工作流引用生成的 `<id>.<扩展名>`。任务本身的原始输入放在 `tasks/<任务>/00_素材/`；ComfyUI 生成结果放在同一任务的 `comfyui/output/`。模型依赖记录在对应的[已验证工作流](../workflows/comfyui/README.md)中。
