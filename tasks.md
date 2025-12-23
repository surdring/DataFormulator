# Data Formulator 性能优化任务清单

> 说明：本清单用于跟踪本地改造版 Data Formulator 的性能优化任务。每个任务完成后，将对应条目标记为 `[x]`，并在条目后简要备注完成日期与实现方式。

## 一、前端性能优化

- [x] **拆分前端 bundle，按需加载大模块**  （2025-12-03：已通过 React.lazy + Suspense 懒加载 ReportView、DataLoadingChatDialog、ChartRecBox、EncodingShelfThread 等大模块，并在 Vite manualChunks 中拆分 vendor-react/mui/vega/d3/editor/markdown 等依赖，减小首屏 JS 体积。）  
  - 将 `ReportView`、`DataLoadingChatDialog`/`DataLoadingThread`、`ChartRecBox`、`EncodingShelfCard` 等通过 `React.lazy + Suspense` 懒加载。  
  - 在构建配置中使用 `manualChunks` 等方式拆分 `vendor-react`、`vendor-mui`、`vendor-vega/d3`、`editor/markdown` 等大依赖，减小首屏 JS 体积。

- [x] **CSV 文本解析结果缓存**  （2025-12-03：已在 createTableFromText 中增加基于 cleanedText 的解析缓存 Map）  
  - 以 `text` 内容（或其 hash）为 key，在前端缓存 `createTableFromText` 的解析结果，避免同一段 CSV 在多个组件中重复解析。  
  - 对超大 CSV 增加“预览行数上限”（例如仅预览前 1000 行），防止表格渲染卡顿。

- [x] **图表推荐 & 灵感结果缓存**  （2025-12-03：已在 ChartRecBox 中增加基于 tableId + mode + encodingMap 快照 的前端缓存，并提供“刷新灵感”按钮，避免相同上下文重复请求后端。）  
  - 在 `ChartRecBox` 中，以 `(tableId, mode, encodingMap 快照)` 为 key 缓存 `/api/agent/get-recommendation-questions` 的结果。  
  - 当数据/编码不变时直接使用缓存，提供“刷新灵感”按钮主动重新请求。

- [x] **图表区域懒加载与可视化容器优化**  （2025-12-03：已在 DataThread 中为 Vega-Lite 图表缩略图引入 IntersectionObserver 懒加载，仅在接近视窗时挂载 VegaLite 组件，其余使用轻量骨架占位，减少多图场景下同时渲染的图表数量。）  
  - 对重量级可视化组件（Vega/Vega-Lite 渲染区域）使用懒加载或基于可见性的渲染控制（如 IntersectionObserver）。  
  - 在多图场景中限制同时在 DOM 中的图表数量，对超出视窗部分进行卸载或简化展示。

## 二、后端性能与资源利用

- [x] **数据摘要 generate_data_summary 结果缓存**  （2025-12-03：已在 agent_utils.generate_data_summary 中增加基于 session_id + 表名 + 行数 + schema 列集合 hash 的缓存 Map，并对大表做行数与列数抽样，控制摘要长度，所有调用该函数的 Agent 自动复用缓存。）  
  - 在后端为 `generate_data_summary` 增加缓存层，以 `(session_id, table_name, row_count, schema hash)` 为 key 复用摘要。  
  - 适用 Agent：`DataLoadAgent`、`PythonDataRecAgent`、`InteractiveExploreAgent`、`ExplorationAgent`、`PythonDataTransformationAgent` 等。  
  - 对大表仅抽样部分行/列生成摘要，控制摘要长度在大模型上下文可接受范围内。

- [x] **LLM Client 连接复用**  （2025-12-03：已在 agents.client_utils.Client 中增加基于 endpoint + model + api_base + api_key + api_version 的进程级 Client 缓存，并在 openai 分支复用 OpenAI 客户端；agent_routes.get_client 统一走 Client.from_config，从而在多 Agent、多请求之间复用底层 HTTP 连接池。）  
  - 在 `Client` 层面对 `(endpoint, model, api_base, api_key)` 做简单进程级缓存，避免频繁 new client 和重复初始化 HTTP 连接池。  
  - 检查 `check-available-models` 与 `test-model` 的调用频率，避免无谓的健康检查。

- [x] **探索 / 报表流程中的冗余计算收敛**  （2025-12-03：已通过 agent_utils.generate_data_summary 的会话级摘要缓存，以及 agent_sql_data_transform.get_sql_table_statistics_str 的基于连接 + 表名 + 采样参数的进程级统计缓存，避免 ExplorationAgent / InteractiveExploreAgent / ReportGen 等在多轮探索与报表生成中对相同表重复计算字段统计与摘要。）  
  - 在 `run_exploration_flow_streaming` 等工作流中，避免对相同表重复计算统计信息。  
  - 对多步 Agent 流程中可共享的中间结果（如中间派生表的摘要）进行缓存与复用。

## 三、多模态与网络传输

- [x] **截图图片压缩与下采样**  （2025-12-03：已在 DataLoadingThread 中为粘贴图片和示例图片引入 `compressImageDataUrl`，使用 `<canvas>` 将最长边限制在约 1600 像素并以 JPEG 质量 0.7 重新编码，仅将压缩后的 data URL 通过 `/api/agent/clean-data-stream` 发送到后端，显著减小多模态清洗请求体积。）  
  - 在前端粘贴图片时，将原始图片通过 `<canvas>` 进行缩放（例如最长边限制在 1280–1600 像素）与 JPEG 压缩（质量约 0.7）。  
  - 仅将压缩后的 data URL 发送到 `/api/agent/clean-data-stream`，在保证 OCR 可读性的前提下显著减少请求体大小和带宽占用。

- [x] **多模态清洗请求的错误与重试策略**  （2025-12-03：已在 `/clean-data-stream` 路由和 DataCleanAgentStream 中统一错误返回结构（包含 message/error_type/retryable），并在 DataLoadingThread 前端根据最后一次错误时间增加冷却窗口与更清晰的错误提示，避免用户在短时间内频繁手动重试造成模型与网络压力。）  
  - 为 `/clean-data-stream` 增加更清晰的错误状态与前端重试策略，避免用户在失败后多次手动重试造成模型/网络压力。

## 四、可视化与大数据表

- [x] **可视化层的 Top-K 与聚合策略优化**  （2025-12-03：已在 app/utils.tsx 的 `assembleVegaChart` 中引入 `CHART_NOMINAL_LIMITS`，按图表类型分别限制 x/y 轴、color 和 facet 的 nominal 上限，并在现有 Top-K 与自动排序逻辑基础上统一使用这些上限，避免高基数分类图在前端渲染过多类别；配合现有 `prepVisTable` 聚合路径，仅对聚合后的表进行可视化。）  
  - 基于当前 `assembleVegaChart` 中的 Top-K 与自动排序逻辑，结合配置（如 `config.maxNominalValues`）细化不同图表类型下的默认上限。  
  - 对大表优先在后端进行聚合（groupby + agg），仅传递聚合结果到前端绘制图表。

- [x] **字段元数据与语义类型推断缓存**  （2025-12-03：已在前端 dfSlice.fetchFieldSemanticType thunk 中增加基于表 id + 现有 metadata 的语义类型缓存判断，当 Redux state 中该表所有字段已具备非空 semanticType 时直接返回 cached，不再调用 `/process-data-on-load`，避免同一表在多视图、多工作流中重复请求后端推断字段语义。）  
  - 对 `fetchFieldSemanticType` 的结果进行持久化缓存（基于表 id + schema），避免同一表在多视图中重复请求后端推断字段语义。

## 五、模型调用与上下文控制

- [x] **灵感问题（get-recommendation-questions）上下文裁剪**  （2025-12-03：已在 `InteractiveExploreAgent` 中通过缩小 `generate_data_summary`/`get_sql_table_statistics_str` 的字段示例与字符上限，并在 exploration_thread 部分仅保留表名、行列规模与简短描述，显著压缩上下文；同时在系统提示中显式限制问题数量（≤4 个）与单条问题/goal 的长度，减小对大模型的 token 与输出长度压力。）  
  - 在构造 `InteractiveExploreAgent` 的 `context` 时，对非常大的数据摘要进行截断或分层摘要（schema 概览 + 少量示例），减小对大模型的 token 压力。  
  - 在保证问题质量的前提下，进一步约束输出长度与问题数量。

- [x] **多 Agent 协作场景下的上下文共享**  （2025-12-03：已通过 `agent_utils.generate_data_summary` 与 `get_sql_table_statistics_str` 的会话级/进程级缓存，以及在 InteractiveExploreAgent/ExplorationAgent/ReportGen/PythonDataRecAgent 等 Agent 中统一引用这些摘要与统计，配合前面对摘要长度与字段示例的裁剪，实现探索、报表、推荐多 Agent 之间复用统一的数据上下文，而不在每个 prompt 内重复构造大段字段说明。）  
  - 在探索、报表、数据推荐等多个 Agent 之间共享关键上下文（字段列表、重要统计结果），避免在每个 Agent 的 system/user prompt 中重复塞入同一大段说明。

---

> 使用说明：
> - 每当完成一个优化任务，请在对应项目前将 `[ ]` 改为 `[x]`，并在行尾追加简短备注，如：`（2025-12-03：已实现，见 commit abc123）`。  
> - 如需新增任务，请按上述分区风格追加条目，以便后续统一跟踪。
