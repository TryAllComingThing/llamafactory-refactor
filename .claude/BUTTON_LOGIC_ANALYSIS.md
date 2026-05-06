# 按钮业务逻辑对比分析：Gradio UI vs Frontend + API

**分析日期**: 2026-05-05

---

## 一、Gradio UI 全部按钮清单

### 1.1 所有 17 个按钮/触发器

| # | 位置 | 元素 | 类型 | 核心事件 |
|---|------|------|------|---------|
| 1 | Top Bar | `lang` (语言) | Dropdown | `change` → 刷新所有 i18n 标签 |
| 2 | Top Bar | `model_name` (模型名) | Dropdown | `change` → 触发 `list_output_dirs` + `check_multimodal` |
| 3 | Top Bar | `finetuning_type` (微调方法) | Dropdown | `change` → 触发 `list_output_dirs` |
| 4 | Top Bar | `refresh_btn` (刷新状态) | Button | `click` → 刷新 GPU 状态 |
| 5 | Train Tab | `data_preview_btn` (预览数据集) | Button | `click` → `get_preview` 模态框 |
| 6 | Train Tab | `cmd_preview_btn` (预览命令) | Button | `click` → `runner.preview_train` |
| 7 | Train Tab | `arg_save_btn` (保存训练参数) | Button | `click` → `runner.save_args` |
| 8 | Train Tab | `arg_load_btn` (载入训练参数) | Button | `click` → `runner.load_args` |
| 9 | Train Tab | `start_btn` (开始训练) | Button | `click` → `runner.run_train` |
| 10 | Train Tab | `stop_btn` (中止训练) | Button | `click` → `runner.set_abort` |
| 11 | Train Tab | `resume_btn` (恢复监控) | Checkbox | `change` → `runner.monitor` |
| 12 | Train Tab | `output_dir` (输出目录变更) | Dropdown | `change/input` → 重新列举 + `check_output_dir` |
| 13 | Train Tab | `config_path` (配置路径变更) | Dropdown | `change` → `list_config_paths` |
| 14 | Eval Tab | `cmd_preview_btn` (预览命令) | Button | `click` → `runner.preview_eval` |
| 15 | Eval Tab | `start_btn` (开始评估) | Button | `click` → `runner.run_eval` |
| 16 | Eval Tab | `stop_btn` (中止评估) | Button | `click` → `runner.set_abort` |
| 17 | Eval Tab | `resume_btn` (恢复监控) | Checkbox | `change` → `runner.monitor` |
| 18 | Export Tab | `export_btn` (开始导出) | Button | `click` → `save_model` (直接调用 Python) |
| 19 | Infer Tab | `load_btn` (加载模型) | Button | `click` → `chatter.load_model` |
| 20 | Infer Tab | `unload_btn` (卸载模型) | Button | `click` → `chatter.unload_model` |
| 21 | Infer Tab | `submit_btn` (发送消息) | Button | `click` → `chatter.append` → `chatter.stream` |
| 22 | Infer Tab | `clear_btn` (清空对话) | Button | `click` → 清空 chatbot + messages |
| 23 | Infer Tab | `max_new_tokens` (生成长度) | Slider | ⚙️ 参数输入 |
| 24 | Infer Tab | `top_p` | Slider | ⚙️ 参数输入 |
| 25 | Infer Tab | `temperature` | Slider | ⚙️ 参数输入 |
| 26 | Infer Tab | `skip_special_tokens` | Checkbox | ⚙️ 参数输入 |
| 27 | Infer Tab | `escape_html` | Checkbox | ⚙️ 参数输入 |
| 28 | Infer Tab | `enable_thinking` | Checkbox | ⚙️ 参数输入 |

---

## 二、逐按钮业务逻辑对比

### 2.1 Top Bar - 模型名称变更

| 维度 | Gradio | Frontend + API | 状态 |
|------|--------|---------------|------|
| 触发 | `model_name.change(...)` | `onModelChange` | ✅ |
| 获取路径 | `get_model_path(model_name)` | API `GET /models/{model_name}` | ✅ |
| 获取模板 | `get_template(model_name)` | 含在 models 接口中 | ✅ |
| 获取 checkpoint 列表 | `list_checkpoints(...)` | API `GET /checkpoints` | ✅ |
| 获取量化可用性 | 本地逻辑 | API `GET /on-model-change` 返回 `quantization_available` | ✅ |
| 获取输出目录 | `list_output_dirs(...)` | API `GET /output-dirs` | ✅ |
| 检测多模态 | `is_multimodal(model_name)` | ❌ 未实现 | ❌ **缺失** |
| 重新列举数据集 | `list_datasets(...)` | API `GET /datasets` | ✅ |
| **缺失** | | ❌ 未在模型切换时触发数据集刷新 | ⚠️ |

### 2.2 Train Tab - cmd_preview_btn (预览命令)

| 维度 | Gradio (`runner.preview_train`) | Frontend (`previewTrain`) | 状态 |
|------|------|------|------|
| 触发 | Button click | Button click → `handlePreview()` | ✅ |
| 收集入参 | 所有 `input_elems` (60+ 字段) | `buildTrainParams()` (合并 store + session) | ✅ |
| 校验 | `_initialize(data, do_train=True, from_preview=True)` | 无前端校验 | ⚠️ 依赖后端 |
| 业务逻辑 | `_parse_train_args(data)` → `gen_cmd(args)` | API `POST /train/preview` | ✅ |
| 输出 | `[{output_box: gen_cmd(args)}]` → Generator yield | `result.command` → `message.info()` | ⚠️ 弹窗显示 |
| **差异** | Gradio 输出到 output_box (持久显示) | Frontend 用 message 弹窗 (临时显示) | ⚠️ |

### 2.3 Train Tab - arg_save_btn (保存训练参数)

| 维度 | Gradio (`runner.save_args`) | Frontend (`handleSave`) | 状态 |
|------|------|------|------|
| 触发 | Button click | Button click | ✅ |
| 收集入参 | 所有 `input_elems` | `store.toParams()` + `sessionToParams()` | ✅ |
| 校验 | `_initialize(..., from_preview=True)` | 前端仅校验 configPath 非空 | ⚠️ |
| 保存路径 | `DEFAULT_CONFIG_DIR / config_path` | API `POST /configs/{config_path}` | ✅ |
| 保存内容 | `_build_config_dict(data)` → YAML | 直接序列化 params | ✅ |
| 反馈 | 返回保存路径 + output_box 更新 | `message.success()` 弹出 | ✅ |
| **差异** | 有完整的初始化校验 | 前端校验不完整 | ⚠️ |

### 2.4 Train Tab - arg_load_btn (载入训练参数)

| 维度 | Gradio (`runner.load_args`) | Frontend (`handleLoad`) | 状态 |
|------|------|------|------|
| 触发 | Button click (传入 lang, config_path) | Button click (读取 configPath) | ✅ |
| API | 本地文件读取 `load_args(path)` | API `GET /configs/{config_path}` | ✅ |
| 还原范围 | **所有 input_elems** (包括 Top 栏位的 model/template) | `store.updateFields(data)` (仅 train form 字段) | ❌ **不完整** |
| 反馈 | 更新所有组件值 + output_box | `message.success()` | ⚠️ |
| **差异** | 载入 config 会还原 **所有** 字段（含 Top Bar 设置） | 仅还原 trainForm store 内的字段 | ❌ **严重** |

### 2.5 Train Tab - start_btn (开始训练)

| 维度 | Gradio (`runner.run_train`) | Frontend (`handleStart`) | 状态 |
|------|------|------|------|
| 触发 | Button click | Button click | ✅ |
| 收集入参 | 所有 `input_elems` | `buildTrainParams()` | ✅ |
| 校验 | `_initialize(data, do_train=True, from_preview=False)` | 无前端校验 | ⚠️ |
| API | 直接调用 Python 子进程 `Popen(["llamafactory-cli", "train", ...])` | `POST /train/start` → `run_id` | ✅ |
| 实时监控 | `runner.monitor()` Generator | WebSocket `/ws/train/{run_id}` | ✅ |
| 输出 | 实时更新 `output_box` + `progress_bar` + `loss_viewer` + `swanlab_link` | TrainMonitor 组件实时更新 | ✅ |
| 状态管理 | `running_data` 持久化，支持断点续监控 | `runId` ref | ✅ |

### 2.6 Train Tab - stop_btn (中止训练)

| 维度 | Gradio (`runner.set_abort`) | Frontend (`handleAbort`) | 状态 |
|------|------|------|------|
| 触发 | Button click | Button click | ✅ |
| 业务逻辑 | `self.aborted = True` → `abort_process(self.trainer.pid)` | API `POST /train/abort` | ✅ |
| 反馈 | 无直接反馈 (monitor loop 检测到并通知) | `message.info("abort_sent")` | ✅ |
| **注意** | resume_btn 的 load 逻辑需要 abort 后的 runner 状态 | Frontend 不可见 | ⚠️ |

### 2.7 Train Tab - resume_btn (断点续训监控)

| 维度 | Gradio (`runner.monitor`) | Frontend | 状态 |
|------|------|------|------|
| 触发 | Checkbox `change` | ❌ 无对应控件 | ❌ **缺失** |
| 业务逻辑 | 不启动训练，仅恢复对已有 output_dir 的监控 | ❌ 未实现 | ❌ **缺失** |
| 用途 | 页面崩溃后恢复查看训练进度 | ❌ | ❌ |

### 2.8 Train Tab - output_dir 自动检测

| 维度 | Gradio (`runner.check_output_dir`) | Frontend | 状态 |
|------|------|------|------|
| 触发 | `output_dir.input(...)` 每次输入变更 | ❌ 无自动检测 | ❌ **缺失** |
| 业务逻辑 | 检测 output_dir 是否存在 → 警告并恢复状态 | ❌ | ❌ **缺失** |
| 用途 | 选择已有输出目录时自动加载之前的训练配置 | ❌ | ❌ |

### 2.9 Eval Tab - cmd_preview_btn (预览命令)

| 维度 | Gradio (`runner.preview_eval`) | Frontend (`handlePreview`) | 状态 |
|------|------|------|------|
| 触发 | Button click | Button click | ✅ |
| 收集入参 | 所有 `input_elems` | `buildEvalParams()` | ✅ |
| API | `_preview(data, do_train=False)` → `gen_cmd(args)` | `previewTrain({...params, do_train: false})` | ⚠️ 复用 train preview |
| 输出 | 输出到 output_box | `message.info()` 弹窗 | ⚠️ 临时显示 |

### 2.10 Eval Tab - start_btn (开始评估)

| 维度 | Gradio (`runner.run_eval`) | Frontend (`handleStart`) | 状态 |
|------|------|------|------|
| API | 完整校验 + 子进程 | `POST /eval/start` | ✅ |
| 实时监控 | `runner.monitor()` Generator | WebSocket | ✅ |
| 进度 | `progress_bar` + `output_box` | `n-progress` + `outputText` | ✅ |

### 2.11 Eval Tab - stop_btn (中止评估)

| 维度 | Gradio | Frontend | 状态 |
|------|--------|----------|------|
| 业务逻辑 | 同 Train Tab stop | 同 Train Tab abort | ✅ |

### 2.12 Eval Tab - resume_btn (断点续监控)

| 维度 | Gradio | Frontend | 状态 |
|------|--------|----------|------|
| 状态 | ✅ 支持 | ❌ 缺失 | ❌ **缺失** |

### 2.13 Export Tab - export_btn (开始导出)

| 维度 | Gradio (`save_model`) | Frontend (`handleExport`) | 状态 |
|------|------|------|------|
| 触发 | Button click | Button click | ✅ |
| 收集入参 | `model_name`, `model_path`, `finetuning_type`, `checkpoint_path`, `template`, `export_size`, `export_quantization_bit`, `export_quantization_dataset`, `export_device`, `export_legacy_format`, `export_dir`, `export_hub_model_id`, `extra_args` | ❌ 仅传 `form` 字段 | ❌ **严重不完整** |
| 校验 | 完整校验（模型名、路径、导出目录、GPTQ 条件、Checkpoint 条件、JSON schema） | `message.info("export_started")` | ❌ **仅占位** |
| 业务逻辑 | `export_model(args)` → Generator yield 进度 | ❌ 无实际导出逻辑 | ❌ **严重** |
| 输出 | 实时 yield 导出进度信息 | ❌ 无实时反馈 | ❌ |
| **整体评级** | 完整的多步校验 + 导出 + 清理 | **占位实现，无实际功能** | ❌ |

### 2.14 Infer Tab - load_btn (加载模型)

| 维度 | Gradio (`chatter.load_model`) | Frontend (`handleToggleModel`) | 状态 |
|------|------|------|------|
| 入参 | `model_name`, `model_path`, `finetuning_type`, `template`, `rope_scaling`, `flash_attn`, `use_unsloth`, `enable_liger_kernel`, `infer_backend`, `infer_dtype`, `extra_args`, `checkpoint_path`, `quantization_bit/quantization_method/double_quantization`, `cache_dir`, `trust_remote_code` | `model_name`, `model_path`, `finetuning_type`, `template`, `quantized_bit`, `checkpoint_path` | ❌ **缺失多个关键字段** |
| 校验 | 已加载检查、模型名检查、路径检查、Demo 模式检查、JSON schema 检查 | 无前端校验 | ⚠️ |
| 实时反馈 | Generator yield:"正在加载..."→"加载完成" | 一次性 message.success | ⚠️ |
| **缺失** | | `infer_backend`, `infer_dtype`, `extra_args` 未传递 | ❌ |

### 2.15 Infer Tab - unload_btn (卸载模型)

| 维度 | Gradio | Frontend | 状态 |
|------|--------|----------|------|
| 业务逻辑 | 释放 engine + `torch_gc()` | `POST /model/unload` | ✅ |
| 副作用 | 清空 chatbot + messages | `chatBoxRef?.handleClear()` | ✅ |

### 2.16 Infer Tab - submit_btn (发送消息)

| 维度 | Gradio (`chatter.append` → `chatter.stream`) | Frontend (`handleSend`) | 状态 |
|------|------|------|------|
| Step 1 | `append`: 添加到 chatbot → 清空 query | `chat.addMessage(...)` | ✅ |
| Step 2 | `stream`: 调用 `self.stream_chat(messages, system, tools, images, videos, audios, max_new_tokens, top_p, temperature, skip_special_tokens)` | Mock: `setInterval` 逐字输出硬编码文本 | ❌ **mock** |
| 入参 | system, tools, image, video, audio, max_new_tokens, top_p, temperature, skip_special_tokens, escape_html, enable_thinking | 无 (mock) | ❌ |
| 多模态 | `images=[image]`, `videos=[video]`, `audios=[audio]` | 仅有 image (mock SVG) | ⚠️ |
| Tool Calling | `engine.template.extract_tool(response)` | ❌ 未实现 | ❌ |
| 思考模式 | `engine.template.enable_thinking` + 格式化输出 | ❌ 未实现 | ❌ |
| HTML 转义 | `_escape_html` + `_format_response` | ❌ 未实现 | ❌ |
| **整体评级** | 完整的流式对话 + 多模态 + 工具调用 | **完全 mock，无实际功能** | ❌ |

### 2.17 Infer Tab - clear_btn (清空对话)

| 维度 | Gradio | Frontend | 状态 |
|------|--------|----------|------|
| 业务逻辑 | `([], [])` → chatbot + messages | `chat.clearMessages()` + clearInterval | ✅ |

### 2.18 数据集预览 (data_preview_btn)

| 维度 | Gradio (`get_preview`) | Frontend (`DatasetPreview`) | 状态 |
|------|------|------|------|
| 触发 | Button click → 模态框 | Button click → Modal | ✅ |
| 分页 | 2 条/页 (PAGE_SIZE=2) | 支持 page/page_size 参数 | ✅ 增强 |
| 数据加载 | 直接读文件 (JSON/JSONL) | API `GET /datasets/preview` | ✅ |

---

## 三、总体评估

### 3.1 按钮覆盖度

| Tab | Gradio 按钮数 | Frontend 实现数 | 覆盖率 | 评级 |
|-----|-------------|---------------|-------|------|
| **Top Bar** | 4 触发器 | 3 | 75% | ⚠️ |
| **Train** | 7 按钮 + 2 触发器 | 5 按钮 | 56% | ⚠️ |
| **Eval** | 3 按钮 + 1 触发器 | 2 按钮 | 50% | ⚠️ |
| **Export** | 1 按钮 | 1 按钮 (占位) | 0%* | ❌ |
| **Infer** | 4 按钮 | 3 按钮 (1 mock) | 25%* | ❌ |
| **ChatBox** | 6 参数控件 | 0 | 0% | ❌ |

*标注 0% 表示按钮存在但没有实际业务逻辑。

### 3.2 功能完整性等级

| 类别 | 评级 | 说明 |
|------|------|------|
| **Train 预览命令** | 🟡 B | 逻辑正确，但预览用弹窗而非持久显示 |
| **Train 保存参数** | 🟡 B | 逻辑正确，缺少完整校验 |
| **Train 载入参数** | 🔴 D | 仅还原 store 字段，**不包含 Top Bar 模型参数** |
| **Train 开始训练** | 🟢 A | 逻辑正确，WebSocket 实时监控 |
| **Train 中止训练** | 🟢 A | 逻辑正确 |
| **Train 断点续监控** | 🔴 F | **完全缺失** |
| **Train 自动检测** | 🔴 F | **完全缺失** |
| **Eval 开始评估** | 🟢 A | 逻辑正确 |
| **Eval 中止评估** | 🟢 A | 逻辑正确 |
| **Export 导出** | 🔴 F | **仅占位，无实际导出逻辑** |
| **Infer 加载模型** | 🟡 C | 缺少 infer_backend/dtype/extra_args 传递 |
| **Infer 卸载模型** | 🟢 A | 逻辑正确 |
| **Infer 发送消息** | 🔴 F | **完全 mock，无实际推理逻辑** |
| **Infer 推理参数** | 🔴 F | **全部缺失** |

### 3.3 优先级建议

| 优先级 | 功能 | 影响 |
|--------|------|------|
| **P0** | Export 按钮实现实际导出逻辑 | 核心功能不可用 |
| **P0** | Infer 发送消息接入真实 API | 核心功能不可用 |
| **P0** | Infer 推理参数 (max_new_tokens 等) | 核心功能不可用 |
| **P1** | Infer 加载模型传递完整参数 | 模型加载可能失败 |
| **P1** | Train 载入参数还原 Top Bar 设置 | 恢复配置不完整 |
| **P2** | Train 断点续监控 (resume) | 异常恢复场景 |
| **P2** | output_dir 自动检测 | 防止覆盖已有训练 |
| **P3** | 多模态检测 | 条件性 UI 显示 |
