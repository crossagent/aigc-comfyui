# MiniMax-H3 文生视频 (Text to Video)

`api.json` 是可直接提交给 ComfyUI `/prompt` 的 API 执行图。模型需按 `models.json` 的相对路径放入 `assets/models/comfyui/`，并校验文件大小和 SHA-256。

## 验证证据

2026-10-18 在全新远程 Linux 实例（NVIDIA GeForce RTX 4090 24GB，Ubuntu 22.04，Python 3.12.3，PyTorch 2.14.1+cu130）上的 ComfyUI `v0.41.0`（commit `98cc0bf84b7cb1383654c5b402e7612d875d6d22`）完成全流程真实端到端生成验收：

- **任务提交**：向 `/prompt` 提交 `api.json`，Prompt ID 为 `64dfecc6-efc2-4e62-930e-e5d00c27c58f`。
- **运行日志**：
  - MiniMaxH3 Diffusion 模型动态载入 VRAM（19995MB Staged，208 patches attached）；
  - MiniMaxH3AudioVAE（576MB Staged）与 MiniMaxH3VideoVAE（2677MB Staged）动态分配；
  - 采样器跑通 2 步去噪；
  - 生成原生 16:9 画幅 `1344×768`、24 fps H.264 视频与 AAC 音频同步封装。
- **输出产物**：输出视频文件 `minimax_h3_test_00001_.mp4`（330 KB，双流：视频 `h264 1344x768 24fps` + 音频 `aac`），文件 SHA-256 为 `9817237db8f4edaecbb51ea5b953aff0ae8e635060301f3146add6dd50097654`。
- **结论**：本工作流在全新机器上基于锁定版本的 ComfyUI 与官方 5 个权重文件具备完全可复现的执行能力。

## 执行与参数规范

- **`SaveVideo` 节点**：在 ComfyUI v0.41.0 中提交 `/prompt` API 时，`SaveVideo` 节点必须显式指定 `"format": "auto"` 与 `"codec": "auto"`，否则服务端在执行阶段会报错抛出缺失参数异常。
- **画幅与分辨率**：MiniMax-H3 原生最大画幅限制为 1344×768（短边 768px）。长宽比为 16:9 时，切勿将 `ResolutionSelector` 设为 `1.0`（其输出 1376×768 会超过模型上限），需使用 `0.98`（对应标准 `1344×768`），或直接在 API 图中指定 `width: 1344, height: 768`。
- **LoRA 加载**：模板默认挂接 8 步 Turbo LoRA（`minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors`），即便将步数设为标准步数，ComfyUI 校验仍要求该 LoRA 必须在盘。
