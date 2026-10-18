# ComfyUI 工作流

| 目录 | 用途 |
| --- | --- |
| `validated/` | 通过实际运行的工作流、模型依赖和验收证据；进入 Git |
| `ui/`、`api/` | 本机试验用工作流，不进入 Git |

每个已验证工作流单独成目录。模型权重、输入图、生成结果和单次实验记录不放在本目录。新 ComfyUI 版本上的工作流要重新跑通后才更新该目录的验证说明。

### 已验证工作流列表

- `validated/flux-schnell-gguf/`: Flux Schnell GGUF 文生图（1024×1024）
- `validated/minimax-h3-t2v/`: MiniMax-H3 文生视频（1344×768，24fps 原生 16:9 画幅，全套 5 模块权重）
