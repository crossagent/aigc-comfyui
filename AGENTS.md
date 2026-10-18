# 工作区引导

先阅读与当前工作有关的说明文件：

| 文件 | 主要内容 |
| --- | --- |
| [README.md](README.md) | 工作区顶层目录及当前使用的工具 |
| [docs/git-scope.md](docs/git-scope.md) | 哪些目录和文件进入 Git，哪些数据只保留在本机 |
| [docs/environment.md](docs/environment.md) | 已选择的 ComfyUI 源码版本与环境约定 |
| [docs/deploy-linux.md](docs/deploy-linux.md) | Linux + NVIDIA 新机器部署步骤 |
| [assets/README.md](assets/README.md) | 模型、原始素材和骨架的存放位置；资产目录用法 |
| [tasks/README.md](tasks/README.md) | 任务目录结构；实验记录不纳入主仓库 |
| [workflows/README.md](workflows/README.md) | 工作流目录职责和 ComfyUI 入口 |
| [workflows/comfyui/README.md](workflows/comfyui/README.md) | 验证工作流及其依赖、验收证据的位置 |
| [platforms/README.md](platforms/README.md) | ComfyUI 上游源码安装位置和模型路径配置 |

处理本工作区时遵守这些要求：

1. 不为兼容旧方案添加 fallback。
2. 清晰暴露错误，使报错便于 LLM 理解，不随意兜底。
3. 采用与规模相称的标准实践，不自造轮子。
4. 模块名称明确表达职责，修改不随意扩大职责；职责不合适时先提出重构。
5. 尽量使用静态检查，减少动态推断。
6. 定位问题先建立稳定证据链，不靠反复调参碰运气。
