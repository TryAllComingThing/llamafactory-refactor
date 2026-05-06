# 前端 UI 风格规范

## 核心原则
所有视图组件（TrainView、EvalView、InferView、ExportView）必须保持一致的 UI 风格，与 Gradio 界面保持功能和视觉上的一致性。

## 组件风格

### 表单组件尺寸
- **所有** `n-form-item`、`n-input`、`n-input-number`、`n-select`、`n-button` 使用 `size="tiny"`
- **例外**：独立的大按钮（如加载模型、开始导出）使用 `size="large"` 并占据整行

### Grid 布局
- 标准网格使用 `:cols="5"` 或根据字段数量调整
- 间距统一：`:x-gap="8" :y-gap="6"`
- 多行网格之间使用 `style="margin-top:6px"`

### 字体
- Section 标签：`var(--font-size-sm)`、`var(--font-weight-medium)`
- 普通文本：`var(--font-size-base)`
- 次要文本/日志：`var(--font-size-xs)`、`var(--font-mono)`

### 颜色
- 背景：`var(--bg-surface)`（卡片背景）、`var(--bg-elevated)`（elevated 区域）
- 边框：`var(--border-default)`
- 文本：`var(--text-primary)`（主文本）、`var(--text-secondary)`（次要文本）、`var(--text-tertiary)`（标签）

### 间距
- Section 之间：`margin-bottom: var(--spacing-4)`
- Section 内边距：`padding: var(--spacing-3)`
- 圆角：`var(--radius-sm)`（小元素）、`var(--radius-md)`（卡片）

## 布局模式

### 标准 Form Section
```vue
<div class="form-section">
  <span class="section-label">{{ $t('section_title') }}</span>
  <n-grid :cols="5" :x-gap="8" :y-gap="6">
    <!-- 表单项 -->
  </n-grid>
</div>
```

### 大按钮
```vue
<div class="button-section">
  <n-button type="primary" size="large" @click="handleAction" style="width: 100%">
    {{ $t('action_btn') }}
  </n-button>
</div>
```

### Collapse 面板（TrainView）
- 默认收起：`:default-expanded-names="[]"`
- Header 样式：小字体、浅色背景
- Content 内边距：`var(--spacing-3)`

## 交互方式
- 所有操作使用 `useMessage()` 提供反馈
- 成功：`message.success()`
- 错误：`message.error()`
- 提示：`message.info()`

## 各页面特殊规范

### TrainView
- Collapse 面板布局
- Action 按钮一行：预览命令 | 保存参数 | 载入参数 | 中断 | 开始
- Output 和 DeepSpeed 为独立卡片
- 右侧 Loss 图表 sticky 定位

### EvalView
- 简洁平铺布局
- Action 按钮在 section 内右侧

### InferView
- 第一行：推理引擎 | 推理数据类型 | 额外参数
- 第二行：加载/卸载模型大按钮
- 第三行：ChatBox 对话区域

### ExportView
- 第一行 5 列：分块大小（含 slider）| 量化等级 | 量化数据集 | 设备 | 旧格式
- 第二行 3 列：导出目录 | HF Hub ID | 额外参数
- 导出大按钮独立一行
- 输出日志在底部独立显示

## 禁止事项
- 不要使用 `n-card` 包裹 form-section（EvalView 除外）
- 不要在 form-section 内添加不必要的标题
- 不要修改既定的组件尺寸和间距
- 不要添加未请求的动画或过渡效果
- 不要改变既定的颜色方案
