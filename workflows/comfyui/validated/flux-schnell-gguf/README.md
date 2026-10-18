# Flux Schnell GGUF 文生图

`api.json` 是可直接提交给 ComfyUI `/prompt` 的 API 图。模型需按 `models.json` 的相对路径放入 `assets/models/comfyui/`，并校验文件大小和 SHA-256。使用自定义节点 [ComfyUI-GGUF](https://github.com/city96/ComfyUI-GGUF)，本次验证时的节点 commit 为 `373048b8403a7820620065210a691263d4da0a61`。

验证证据：2026-10-18 在本机 ComfyUI commit `6c62ca0b6bbee7ef293ca475f7904065af5bfb42` 上向 `/prompt` 提交本目录的中性风景 `api.json`，任务 ID 为 `b5c67e45-97ec-4b23-a17f-e5c68fd633af`，`/history` 报告 `execution_success`，输出 1024×1024 山湖风景 `flux_schnell_gguf_00003_.png`。图片内嵌的 prompt 图与本目录 `api.json` 一致，图片 SHA-256 为 `4a5edfa992905f454015c7e8024207981f43982dd5528a00b331ab12547ad582`。生成图片不进入 Git。

此证据只覆盖上述旧本机版本。迁移到仓库锁定的 ComfyUI `v0.41.0` 时，需要重新执行并更新验证证据，不能仅凭旧版本结果宣称新版本已验收。
