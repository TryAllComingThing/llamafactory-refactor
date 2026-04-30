## Project Context
LLaMA Factory: 开源的大模型微调系统，提供完整的训练、评估、对话、导出功能。

## Analysis Constraints
- 仅需提供架构摘要和模块划分，不需要具体的 API 设计方案
- 提供文件级的模块依赖关系，使用表格或列表清晰呈现
- 只分析 `src/llamafactory/webui/` 目录，不需要分析其他目录
- 优先标注：入口模块（Engine）、组件管理器（Manager）、子进程管理（Runner）
- 输出格式：Markdown 格式的分层架构地图