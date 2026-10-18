# 任务目录

每个任务目录保存该目标的素材、中间参考和结果。可按需要设置子任务：

```text
任务名称/
├── 00_素材/            # 本任务的输入
├── comfyui/
│   ├── input/           # 本任务投放给 ComfyUI 的输入
│   └── output/          # 本任务的 ComfyUI 生成结果
├── references/         # 中间参考
├── experiments/        # 本机实验与运行结果
├── comparison/         # 本机对比材料
└── selected/           # 选定成品
```

主仓库保留本说明和 `_template/` 的空目录结构。启动 ComfyUI 时，用 `--input-directory` 和 `--output-directory` 指向当前任务的两个目录；切换任务时明确更换这两个路径。所有具体任务目录及其素材、参数、提示词、运行快照、实验评估和结果都留在本机；模型变化时无需维护一套容易过期的任务实验记录。可复用的 ComfyUI 工作流见 [workflows/](../workflows/README.md)。
