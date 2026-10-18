# Git 管理范围

主仓库保存目录结构、稳定说明、ComfyUI 版本与路径配置、可复用资产的元数据，以及有实际运行证据的工作流。提交前检查 `git status --short` 和 `git diff --cached --stat`。

| 路径 | 纳入 Git | 留在机器或外部资产存储 |
| --- | --- | --- |
| 根目录 | `README.md`、`AGENTS.md`、Git 配置 | 密钥、`.env`、编辑器状态 |
| `assets/` | README、目录占位、`catalog.json`、`catalog.py` | 原始素材、模型权重、骨架、ComfyUI 输入与输出 |
| `tasks/` | 通用说明与 `_template/` 空目录结构 | 所有具体任务目录及其输入、参数、提示词、实验、评估与结果 |
| `workflows/` | 目录说明、`validated/` 下的工作流与依赖、验收证据 | 未验证的界面图、API 图、历史工作流 |
| `platforms/` | README、ComfyUI 版本锁与模型路径配置 | 上游源码、虚拟环境、本机脚本、缓存与日志 |
| `docs/` | 环境、部署与 Git 范围说明 | 本机历史审计 |

`.gitignore` 使用路径白名单。新增需要纳入的文件时，先明确职责，再调整规则；不要用 `git add -f` 绕过排除。具体任务目录始终不进入本仓库。模型变化不要求维护逐次任务实验记录。
