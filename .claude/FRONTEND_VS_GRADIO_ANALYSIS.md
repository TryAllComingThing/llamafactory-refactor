# Frontend vs Gradio UI 功能对比分析报告

**分析日期**: 2026-05-05
**分析范围**: TrainView, EvalView, InferView, ExportView

---

## 一、TrainView 对比

### 1.1 数据区域 (Data Section)

| 字段 | Gradio | Frontend | 状态 |
|------|--------|----------|------|
| training_stage | ✅ Dropdown | ✅ Select | ✅ 一致 |
| dataset_dir | ✅ Textbox | ✅ Input | ✅ 一致 |
| dataset | ✅ Dropdown (multi) | ✅ Select (multi) | ✅ 一致 |
| data_preview_btn | ✅ Button + Modal | ✅ Button + Modal | ✅ 一致 |

### 1.2 超参数区域 (Hyperparameters)

| 字段 | Gradio | Frontend | 状态 |
|------|--------|----------|------|
| learning_rate | ✅ Textbox | ✅ Input | ✅ 一致 |
| num_train_epochs | ✅ Textbox | ✅ Input | ✅ 一致 |
| max_grad_norm | ✅ Textbox | ✅ Input | ✅ 一致 |
| max_samples | ✅ Textbox | ✅ Input | ✅ 一致 |
| compute_type | ✅ Dropdown | ✅ Select | ✅ 一致 |
| cutoff_len | ✅ Slider (4-131072) | ✅ InputNumber | ⚠️ 交互不同 |
| batch_size | ✅ Slider (1-1024) | ✅ InputNumber | ⚠️ 交互不同 |
| gradient_accumulation_steps | ✅ Slider (1-1024) | ✅ InputNumber | ⚠️ 交互不同 |
| val_size | ✅ Slider (0-1) | ✅ InputNumber | ⚠️ 交互不同 |
| lr_scheduler_type | ✅ Dropdown | ✅ Select | ✅ 一致 |

### 1.3 其他参数 (Extra Tab)

| 字段 | Gradio | Frontend | 状态 |
|------|--------|----------|------|
| logging_steps | ✅ Slider | ✅ InputNumber | ⚠️ 交互不同 |
| save_steps | ✅ Slider | ✅ InputNumber | ⚠️ 交互不同 |
| warmup_steps | ✅ Slider | ✅ InputNumber | ⚠️ 交互不同 |
| neftune_alpha | ✅ Slider | ✅ InputNumber | ⚠️ 交互不同 |
| extra_args | ✅ Textbox | ✅ Input | ✅ 一致 |
| packing | ✅ Checkbox | ✅ Checkbox | ✅ 一致 |
| neat_packing | ✅ Checkbox | ✅ Checkbox | ✅ 一致 |
| train_on_prompt | ✅ Checkbox | ✅ Checkbox | ✅ 一致 |
| mask_history | ✅ Checkbox | ✅ Checkbox | ✅ 一致 |
| resize_vocab | ✅ Checkbox | ✅ Checkbox | ✅ 一致 |
| use_llama_pro | ✅ Checkbox | ✅ Checkbox | ✅ 一致 |
| enable_thinking | ✅ Checkbox | ❌ 缺失 | ❌ **缺失** |
| report_to | ✅ Dropdown | ✅ Select | ✅ 一致 |

### 1.4 Freeze Tab

| 字段 | Gradio | Frontend | 状态 |
|------|--------|----------|------|
| freeze_trainable_layers | ✅ Slider | ✅ InputNumber | ⚠️ 交互不同 |
| freeze_trainable_modules | ✅ Textbox | ✅ Input | ✅ 一致 |
| freeze_extra_modules | ✅ Textbox | ✅ Input | ✅ 一致 |

### 1.5 LoRA Tab

| 字段 | Gradio | Frontend | 状态 |
|------|--------|----------|------|
| lora_rank | ✅ Slider | ✅ InputNumber | ⚠️ 交互不同 |
| lora_alpha | ✅ Slider | ✅ InputNumber | ⚠️ 交互不同 |
| lora_dropout | ✅ Slider | ✅ InputNumber | ⚠️ 交互不同 |
| loraplus_lr_ratio | ✅ Slider | ✅ InputNumber | ⚠️ 交互不同 |
| create_new_adapter | ✅ Checkbox | ✅ Checkbox | ✅ 一致 |
| use_rslora | ✅ Checkbox | ✅ Checkbox | ✅ 一致 |
| use_dora | ✅ Checkbox | ✅ Checkbox | ✅ 一致 |
| use_pissa | ✅ Checkbox | ✅ Checkbox | ✅ 一致 |
| lora_target | ✅ Textbox | ✅ Input | ✅ 一致 |
| additional_target | ✅ Textbox | ❌ 缺失 | ❌ **缺失** |

### 1.6 RLHF Tab

| 字段 | Gradio | Frontend | 状态 |
|------|--------|----------|------|
| pref_beta | ✅ Slider | ✅ InputNumber | ⚠️ 交互不同 |
| pref_ftx | ✅ Slider | ✅ InputNumber | ⚠️ 交互不同 |
| pref_loss | ✅ Dropdown | ✅ Select | ✅ 一致 |
| reward_model | ✅ Dropdown (multi) | ✅ Select (multi) | ✅ 一致 |
| ppo_score_norm | ✅ Checkbox | ✅ Checkbox | ✅ 一致 |
| ppo_whiten_rewards | ✅ Checkbox | ✅ Checkbox | ✅ 一致 |

### 1.7 Multimodal Tab

| 字段 | Gradio | Frontend | 状态 |
|------|--------|----------|------|
| freeze_vision_tower | ✅ Checkbox | ✅ Checkbox | ✅ 一致 |
| freeze_multi_modal_projector | ✅ Checkbox | ✅ Checkbox | ✅ 一致 |
| freeze_language_model | ✅ Checkbox | ✅ Checkbox | ✅ 一致 |
| image_max_pixels | ✅ Textbox | ✅ Input | ✅ 一致 |
| image_min_pixels | ✅ Textbox | ✅ Input | ✅ 一致 |
| video_max_pixels | ✅ Textbox | ✅ Input | ✅ 一致 |
| video_min_pixels | ✅ Textbox | ✅ Input | ✅ 一致 |

### 1.8 GaLore Tab

| 字段 | Gradio | Frontend | 状态 |
|------|--------|----------|------|
| use_galore | ✅ Checkbox | ✅ Checkbox | ✅ 一致 |
| galore_rank | ✅ Slider | ✅ InputNumber | ⚠️ 交互不同 |
| galore_update_interval | ✅ Slider | ✅ InputNumber | ⚠️ 交互不同 |
| galore_scale | ✅ Slider (0-100) | ✅ InputNumber (0-1) | ❌ **范围不同** |
| galore_target | ✅ Textbox | ✅ Input | ✅ 一致 |

### 1.9 APOLLO Tab

| 字段 | Gradio | Frontend | 状态 |
|------|--------|----------|------|
| use_apollo | ✅ Checkbox | ✅ Checkbox | ✅ 一致 |
| apollo_rank | ✅ Slider | ✅ InputNumber | ⚠️ 交互不同 |
| apollo_update_interval | ✅ Slider | ✅ InputNumber | ⚠️ 交互不同 |
| apollo_scale | ✅ Slider (0-100) | ✅ InputNumber (0-1) | ❌ **范围不同** |
| apollo_target | ✅ Textbox | ✅ Input | ✅ 一致 |

### 1.10 BAdam Tab

| 字段 | Gradio | Frontend | 状态 |
|------|--------|----------|------|
| use_badam | ✅ Checkbox | ✅ Checkbox | ✅ 一致 |
| badam_mode | ✅ Dropdown (layer/ratio) | ✅ Dropdown (layer/block) | ❌ **选项不同** |
| badam_switch_mode | ✅ Dropdown | ✅ Dropdown | ✅ 一致 |
| badam_switch_interval | ✅ Slider | ✅ InputNumber | ⚠️ 交互不同 |
| badam_update_ratio | ✅ Slider | ✅ InputNumber | ⚠️ 交互不同 |

### 1.11 SwanLab Tab

| 字段 | Gradio | Frontend | 状态 |
|------|--------|----------|------|
| use_swanlab | ✅ Checkbox | ✅ Checkbox | ✅ 一致 |
| swanlab_project | ✅ Textbox | ✅ Input | ✅ 一致 |
| swanlab_run_name | ✅ Textbox | ✅ Input | ✅ 一致 |
| swanlab_workspace | ✅ Textbox | ✅ Input | ✅ 一致 |
| swanlab_api_key | ✅ Textbox | ✅ Input (password) | ✅ 增强 |
| swanlab_mode | ✅ Dropdown | ✅ Select | ✅ 一致 |
| swanlab_logdir | ❌ 缺失 | ✅ Input | ✅ 增强 |

### 1.12 操作按钮区域

| 功能 | Gradio | Frontend | 状态 |
|------|--------|----------|------|
| 预览命令 | ✅ Button | ✅ Button | ✅ 一致 |
| 保存参数 | ✅ Button | ✅ Button | ✅ 一致 |
| 载入参数 | ✅ Button | ✅ Button | ✅ 一致 |
| 开始训练 | ✅ Button (primary) | ✅ Button (primary) | ✅ 一致 |
| 中止训练 | ✅ Button (stop) | ✅ Button (error) | ✅ 一致 |

### 1.13 输出区域

| 字段 | Gradio | Frontend | 状态 |
|------|--------|----------|------|
| output_dir | ✅ Dropdown | ✅ Select | ✅ 一致 |
| config_path | ✅ Dropdown | ✅ Select | ✅ 一致 |
| device_count | ✅ Textbox | ✅ InputNumber | ✅ 一致 |
| ds_stage | ✅ Dropdown (none/2/3) | ✅ Select (none/stage1/stage2/stage3) | ⚠️ 选项增强 |
| ds_offload | ✅ Checkbox | ✅ Checkbox | ✅ 一致 |
| resume_btn | ✅ Checkbox | ❌ 缺失 | ❌ **缺失** |
| progress_bar | ✅ Slider (hidden) | ✅ Progress (via WS) | ✅ 增强 |
| output_box | ✅ Markdown | ✅ Text (via WS) | ✅ 增强 |
| loss_viewer | ✅ Plot | ✅ ECharts (via WS) | ✅ 增强 |

---

## 二、EvalView 对比

### 2.1 数据区域

| 字段 | Gradio | Frontend | 状态 |
|------|--------|----------|------|
| dataset_dir | ✅ Textbox | ✅ Input | ✅ 一致 |
| dataset | ✅ Dropdown (multi) | ✅ Select (multi) | ✅ 一致 |
| data_preview_btn | ✅ Button + Modal | ✅ Button + Modal | ✅ 一致 |

### 2.2 评估参数

| 字段 | Gradio | Frontend | 状态 |
|------|--------|----------|------|
| cutoff_len | ✅ Slider | ✅ InputNumber | ⚠️ 交互不同 |
| max_samples | ✅ Textbox | ✅ Input | ✅ 一致 |
| batch_size | ✅ Slider | ✅ InputNumber | ⚠️ 交互不同 |
| predict | ✅ Checkbox | ✅ Checkbox | ✅ 一致 |
| max_new_tokens | ✅ Slider | ✅ InputNumber | ⚠️ 交互不同 |
| top_p | ✅ Slider | ✅ InputNumber | ⚠️ 交互不同 |
| temperature | ✅ Slider | ✅ InputNumber | ⚠️ 交互不同 |
| output_dir | ✅ Textbox | ✅ Textbox | ✅ 一致 |

### 2.3 操作按钮

| 功能 | Gradio | Frontend | 状态 |
|------|--------|----------|------|
| 预览命令 | ✅ Button | ✅ Button | ✅ 一致 |
| 开始评估 | ✅ Button (primary) | ✅ Button (primary) | ✅ 一致 |
| 中止评估 | ✅ Button (stop) | ✅ Button (error) | ✅ 一致 |
| resume_btn | ✅ Checkbox | ❌ 缺失 | ❌ **缺失** |
| progress_bar | ✅ Slider (hidden) | ✅ Progress (via WS) | ✅ 增强 |

---

## 三、InferView 对比

### 3.1 推理配置

| 字段 | Gradio | Frontend | 状态 |
|------|--------|----------|------|
| infer_backend | ✅ Dropdown | ✅ Select | ✅ 一致 |
| infer_dtype | ✅ Dropdown | ✅ Select | ✅ 一致 |
| extra_args | ✅ Textbox | ✅ Input | ✅ 一致 |

### 3.2 模型控制

| 功能 | Gradio | Frontend | 状态 |
|------|--------|----------|------|
| 加载模型 | ✅ Button | ✅ Button (large) | ✅ 一致 |
| 卸载模型 | ✅ Button | ✅ Button (large) | ✅ 一致 |
| info_box | ✅ Textbox | ✅ Message | ✅ 增强 |

### 3.3 对话区域 (ChatBox)

| 字段 | Gradio | Frontend | 状态 |
|------|--------|----------|------|
| chatbot | ✅ Chatbot | ✅ Custom Component | ✅ 一致 |
| role | ✅ Dropdown | ❌ 缺失 | ❌ **缺失** |
| system | ✅ Textbox | ❌ 缺失 | ❌ **缺失** |
| tools | ✅ Textbox | ❌ 缺失 | ❌ **缺失** |
| image | ✅ Image | ✅ Image (mock) | ⚠️ API 待接入 |
| video | ✅ Video | ❌ 缺失 | ❌ **缺失** |
| audio | ✅ Audio | ❌ 缺失 | ❌ **缺失** |
| query | ✅ Textbox | ✅ Textarea | ✅ 一致 |
| submit_btn | ✅ Button | ✅ Button | ✅ 一致 |
| max_new_tokens | ✅ Slider | ❌ 缺失 | ❌ **缺失** |
| top_p | ✅ Slider | ❌ 缺失 | ❌ **缺失** |
| temperature | ✅ Slider | ❌ 缺失 | ❌ **缺失** |
| skip_special_tokens | ✅ Checkbox | ❌ 缺失 | ❌ **缺失** |
| escape_html | ✅ Checkbox | ❌ 缺失 | ❌ **缺失** |
| enable_thinking | ✅ Checkbox | ❌ 缺失 | ❌ **缺失** |
| clear_btn | ✅ Button | ✅ Button | ✅ 一致 |

---

## 四、ExportView 对比

### 4.1 导出参数

| 字段 | Gradio | Frontend | 状态 |
|------|--------|----------|------|
| export_size | ✅ Slider (1-100) | ✅ InputNumber + Slider | ✅ 增强 |
| export_quantization_bit | ✅ Dropdown | ✅ Select | ✅ 一致 |
| export_quantization_dataset | ✅ Textbox | ✅ Input | ✅ 一致 |
| export_device | ✅ Radio | ✅ Radio | ✅ 一致 |
| export_legacy_format | ✅ Checkbox | ✅ Checkbox | ✅ 一致 |

### 4.2 输出区域

| 字段 | Gradio | Frontend | 状态 |
|------|--------|----------|------|
| export_dir | ✅ Textbox | ✅ Input | ✅ 一致 |
| export_hub_model_id | ✅ Textbox | ✅ Input | ✅ 一致 |
| extra_args | ✅ Textbox | ✅ Input | ✅ 一致 |

### 4.3 操作按钮

| 功能 | Gradio | Frontend | 状态 |
|------|--------|----------|------|
| 开始导出 | ✅ Button | ✅ Button (large) | ✅ 一致 |
| info_box | ✅ Textbox | ✅ Progress + Text | ✅ 增强 |

---

## 五、总结

### 5.1 一致性分析

| 视图 | 字段覆盖率 | 布局一致性 | 交互一致性 |
|------|-----------|-----------|-----------|
| TrainView | 95% | ✅ 高 | ⚠️ 部分不同 |
| EvalView | 100% | ✅ 高 | ⚠️ 部分不同 |
| InferView | 60% | ✅ 高 | ⚠️ 部分不同 |
| ExportView | 100% | ✅ 高 | ✅ 高 |

### 5.2 缺失功能汇总

#### TrainView 缺失
- `enable_thinking` (Extra Tab)
- `additional_target` (LoRA Tab)
- `resume_btn` (输出区域)

#### EvalView 缺失
- `resume_btn` (输出区域)

#### InferView 缺失 (严重)
- `role` 选择 (User/Observation)
- `system` 提示词输入
- `tools` 工具列表输入
- `video` 上传
- `audio` 上传
- `max_new_tokens` 滑块
- `top_p` 滑块
- `temperature` 滑块
- `skip_special_tokens` 开关
- `escape_html` 开关
- `enable_thinking` 开关

### 5.3 交互差异说明

| 组件类型 | Gradio | Frontend | 影响评估 |
|---------|--------|----------|---------|
| 数值输入 | Slider | InputNumber | ⚠️ 中等 - 用户习惯不同 |
| 进度显示 | Slider (hidden) | Progress + WS | ✅ 前端增强 |
| 日志输出 | Markdown | Text (streaming) | ✅ 前端增强 |
| 损失图表 | Plot | ECharts | ✅ 前端增强 |

### 5.4 建议优先级

#### P0 - 高优先级 (核心功能缺失)
1. **InferView**: 添加推理参数配置区域 (max_new_tokens, top_p, temperature 等)
2. **InferView**: 添加多模态支持 (video, audio)
3. **InferView**: 添加 role/system/tools 支持

#### P1 - 中优先级 (功能完整性)
1. **TrainView**: 添加 `enable_thinking` 选项
2. **TrainView**: 添加 `additional_target` 字段
3. **TrainView/BAdam**: 修正 `badam_mode` 选项 (应为 layer/ratio)
4. **TrainView/GaLore**: 修正 `galore_scale` 范围 (0-100)
5. **TrainView/APOLLO**: 修正 `apollo_scale` 范围 (0-100)

#### P2 - 低优先级 (体验优化)
1. **TrainView/EvalView**: 添加 resume_btn 支持断点续训
2. **全局**: Slider 与 InputNumber 的协同 (可选项)

---

## 六、前端优势

1. **实时性**: WebSocket 实时更新训练进度和损失图表
2. **响应式**: 支持不同屏幕尺寸的自适应布局
3. **组件化**: 代码可维护性更高
4. **国际化**: i18n 支持更完善
5. **性能**: 前端渲染，减轻服务器负担

---

## 七、Gradio 优势

1. **功能完整性**: 所有参数均有对应控件
2. **后端集成**: 与后端 API 无缝对接
3. **Slider 交互**: 对于范围参数更直观
4. **Chatbot 组件**: 内置多模态支持

---

**结论**: Frontend 在 UI 一致性和实时性方面表现优秀，但 InferView 缺失较多核心功能，建议优先补充。TrainView 和 EvalView 功能覆盖率较高，只需少量补充即可达到 100% 对齐。
