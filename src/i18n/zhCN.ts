// 中文文案表，仅提供简易的 key-value 映射。
// 如需英文界面，可在后续增加 enUS.ts 并扩展此结构。

export const zhCN: Record<string, string> = {
  // 通用
  "app.title": "Data Formulator 数据探索",

  // About 页面
  "about.hero.description": "用 AI 智能体把几乎任何数据都变成洞见，同时保留你对探索路径的掌控。",
  "about.hero.button.start": "开始探索",
  "about.hero.button.whatsNew": "v0.5 更新内容",
  "about.hero.button.github": "GitHub 仓库",
  "about.hero.button.installLocally": "本地安装",
  "about.hero.button.tryOnlineDemo": "在线体验 Demo",
  "about.hero.demoTip": "小提示：本地安装功能更完整，当前在线 Demo 的能力仍然有限。",

  "about.feature.loadAny.title": "加载几乎任何数据",
  "about.feature.loadAny.desc": "加载结构化数据、连接数据库，并让 AI 智能体从截图、文本块等临时数据中提取和清洗小规模数据。",
  "about.feature.agentMode.title": "智能体模式",
  "about.feature.agentMode.desc": "与数据“对话”，只给出高层目标，就让智能体自动探索并生成可视化图表。",
  "about.feature.interactive.title": "交互式控制",
  "about.feature.interactive.desc": "结合界面操作与自然语言，精确描述图表设计；向智能体要推荐；用数据线程回溯、分支或跟进。",
  "about.feature.verifyShare.title": "验证并分享洞见",
  "about.feature.verifyShare.desc": "与图表互动，查看数据、公式和代码，生成报告，用你自己的探索过程来支撑结论。",

  "about.screenshot.prices": "探索 2005–2025 年的消费者价格走势",
  "about.screenshot.movies": "报告：按收入统计的票房最高导演",
  "about.screenshot.renewable": "各国可再生能源占比",
  "about.screenshot.unemployment": "报告：2008 年金融危机对失业率的影响",
  "about.screenshot.claude": "对比不同 Claude 模型在多种任务上的表现",

  "about.dataHandling.title": "Data Formulator 如何处理你的数据？",
  "about.dataHandling.storage": "📦 数据存储：上传的数据（CSV、XLSX、JSON、剪贴板、脏数据等）仅存储在浏览器本地。",
  "about.dataHandling.processing": "⚙️ 数据处理：本地安装版本在你的机器上运行 Python；在线 Demo 会将数据发送到服务器进行转换，但不会长期存储。",
  "about.dataHandling.database": "🗄️ 数据库：仅在本地安装的 Data Formulator 中提供（在临时目录创建 DuckDB 数据库文件）；在线 Demo 不支持数据库功能。",
  "about.dataHandling.llm": "🤖 LLM 端点：会将小样本数据连同提示词发送至 LLM 端点。如需处理敏感数据，请优先使用你信任的模型服务商。",
  "about.dataHandling.footer": "来自 Microsoft Research 的研究原型",

  // 顶部导航 / 菜单
  "nav.data": "数据",
  "nav.session": "会话",
  "nav.settings": "设置",
  "nav.modelConfig": "模型配置",
  "nav.about": "关于",
  "nav.app": "应用",

  // Session 菜单
  "session.menu": "会话",
  "session.import": "导入会话",
  "session.export": "导出会话",
  "session.saveLocally.tooltip": "将当前会话保存到本地文件",
  "session.databaseFile": "数据库文件",
  "session.downloadDb": "下载数据库文件",
  "session.importDb": "导入数据库文件",
  "session.dbWarning": "当前会话包含存储在数据库中的数据，如需下次继续，请导出并重新导入数据库。",

  // Reset Dialog
  "session.reset.button": "重置会话",
  "session.reset.title": "重置会话？",
  "session.reset.desc": "重置后，所有未导出的内容（图表、派生数据、概念等）都会丢失。",
  "common.reset": "重置会话",
  "common.cancel": "取消",

  // Settings Dialog
  "settings.button": "设置",
  "settings.title": "设置",
  "settings.frontend": "前端设置",
  "settings.backend": "后端设置",
  "settings.defaultChartWidth": "默认图表宽度",
  "settings.defaultChartHeight": "默认图表高度",
  "settings.defaultChartWidth.helper": "取值需在 100 到 1000 像素之间",
  "settings.defaultChartHeight.helper": "取值需在 100 到 1000 像素之间",
  "settings.formulateTimeout": "生成超时时间（秒）",
  "settings.formulateTimeout.helper": "生成过程允许的最大耗时，超时后将终止本次生成（1~3600 秒）",
  "settings.maxRepairAttempts": "代码修复最大尝试次数",
  "settings.maxRepairAttempts.helper": "代码执行失败时，LLM 自动修复的最大尝试次数（推荐 1，过大可能导致变慢）",
  "settings.resetToDefault": "恢复默认设置",
  "settings.apply": "应用",

  // DataFormulator 首屏
  "home.subtitle": "用 AI 智能体探索数据，让你掌控分析路径。",
  "home.loadData.section": "加载数据",
  "home.loadData.messy": "脏数据（图片/文本文本）",
  "home.loadData.examples": "示例数据",
  "home.loadData.files": "文件",
  "home.loadData.clipboard": "剪贴板",
  "home.loadData.database": "数据库",
  "home.loadData.description.prefix": "从 CSV、Excel、JSON、数据库加载结构化数据，或使用 AI 从",
  "home.loadData.description.suffix": "中提取数据。",
  "home.examples.section": "或者，浏览示例",

  "home.loadData.screenshots": "截图",
  "home.loadData.textBlocks": "文本块",
  "home.loadData.tooltip.screenshot.title": "数据截图示例：",
  "home.loadData.tooltip.textBlock.title": "脏文本块示例：",

  // 示例会话
  "examples.gasPrices.title": "汽油价格",
  "examples.gasPrices.desc": "按油品类别查看每周汽油价格。",
  "examples.globalEnergy.title": "全球能源",
  "examples.globalEnergy.desc": "探索全球能源消耗与二氧化碳排放数据。",
  "examples.movies.title": "电影票房",
  "examples.movies.desc": "分析电影的票房表现、预算和评分数据。",
  "examples.unemployment.title": "失业率",
  "examples.unemployment.desc": "按行业查看随时间变化的失业率。",

  // 顶部 Data 菜单（与首页 loadData 含义类似，但用于主菜单）
  "data.menu.database": "数据库",
  "data.menu.cleanData": "清洗脏数据（图片/文本）",
  "data.menu.examples": "示例数据",
  "data.menu.files": "上传数据文件（CSV/TSV/JSON）",
  "data.menu.clipboard": "粘贴表格数据（CSV/TSV）",

  // Model 选择覆盖层
  "overlay.model.first": "首先，请选择要使用的模型",
  "overlay.model.tip": "💡 建议选择具备较强代码生成能力的模型（如 gpt-5、claude-sonnet-4-5），以获得更好体验。",

  // 图表推荐 / 探索（ChartRecBox）
  "chart.mode.interactive": "交互模式",
  "chart.mode.agent": "智能体模式",
  "chart.nlTable.tooltip.selectTables": "选择用于数据整理的数据表",
  "chart.nlTable.required": "必选",

  "chart.prompt.agent.default": "帮我挖掘这个数据里有意思的发现",
  "chart.prompt.interactive.default": "先给我看看这个数据里有什么有趣的模式",
  "chart.prompt.tooltip.generate": "根据描述生成图表",
  "chart.prompt.label.agent": "你想让智能体从哪里开始探索？",
  "chart.prompt.label.interactive": "你想先看看什么内容？",

  "chart.ideas.caption.question": "需要灵感？",
  "chart.ideas.tooltip.getSome": "获取一些探索思路",
  "chart.ideas.tooltip.refresh": "刷新灵感（重新向模型请求问题）",
  "chart.ideas.sectionTitle": "灵感建议",
  "chart.agentIdeas.sectionTitle": "探索方向",
  "chart.agentIdeas.directionsLabel": "探索路径",
  "chart.agentIdeas.tooltip.deepDive": "深入挖掘当前方向",
  "chart.agentIdeas.tooltip.branch": "展开更多分支问题",

  // ModelSelectionDialog
  "models.assignments.title": "模型槽位分配",
  "models.assignments.slot.generation": "探索规划、代码生成",
  "models.assignments.slot.hint": "后台类型推断、代码讲解",
  "models.assignments.noModel": "未分配模型",
  "models.assignments.modelFor": "用于 {slot} 的模型",
  "models.assignments.modelReady": "模型已就绪，可正常使用",
  "models.assignments.modelClickToTest": "点击测试该模型是否可用",
  "models.assignments.modelErrorPrefix": "错误：",
  "models.assignments.modelErrorClickRetest": "。点击重新测试。",
  "models.assignments.summaryTip": "提示：为生成任务选择更强模型，为提示/辅助任务选择更快模型。",
  "models.assignments.noAssignment": "未分配",
  "models.assignments.unknownModel": "未知模型",

  "models.table.provider": "提供方",
  "models.table.apiKey": "API Key",
  "models.table.model": "模型",
  "models.table.apiBase": "API 地址",
  "models.table.apiVersion": "API 版本",
  "models.table.status": "状态",
  "models.table.actions": "操作",
  "models.table.default": "默认",
  "models.table.none": "无",

  "models.status.unknown": "未知",
  "models.status.testing": "测试中",
  "models.status.ok": "可用",
  "models.status.error": "错误",
  "models.status.button.ready": "已就绪",
  "models.status.button.test": "测试",
  "models.status.button.retest": "重新测试",

  "models.tooltip.remove": "移除该模型",
  "models.tooltip.addTest": "添加并测试模型",
  "models.tooltip.modelExists": "该 provider + model + base + key 已存在",

  "models.new.provider.placeholder": "提供方（如 openai/azure/ollama 等）",
  "models.new.provider.examples": "示例",
  "models.new.apiKey.placeholder": "可选：如果是无需 Key 的本地服务可以留空",
  "models.new.model.placeholder": "模型名称，如 gpt-4o 或 gpt-oss-20b",
  "models.new.apiBase.placeholder": "自定义 API 地址，如 http://localhost:8080/v1",
  "models.new.apiVersion.placeholder": "可选：API 版本",
  "models.new.clear": "清空",

  "models.footer.config": "配置基于 LiteLLM。如需查看支持的提供方，请访问文档。对兼容 OpenAI 协议的服务，请使用 'openai' 提供方。",

  "models.button.select": "选择模型",
  "models.button.tooltip": "为不同任务配置模型槽位",
  "models.dialog.title": "为不同任务配置模型",
  "models.dialog.available": "可用模型",
  "models.button.showKeys": "显示 Key",
  "models.button.hideKeys": "隐藏 Key",
  "models.button.applySlots": "应用槽位分配",
  "models.button.cancel": "取消",

  // 视图模式切换
  "viewMode.explore": "探索",
  "viewMode.report": "报告",

  // 路由错误
  "error.route.generic": "发生错误，请刷新页面。如果问题仍然存在，可以尝试关闭会话后重新进入。",

  // 顶部关于页工具提示
  "nav.tooltip.watchVideo": "观看演示视频",
  "nav.tooltip.viewOnGitHub": "在 GitHub 上查看",
  "nav.tooltip.pipInstall": "使用 pip 安装",
  "nav.tooltip.joinDiscord": "加入 Discord 社区",

  // 数据集 URL 对话框
  "dataset.urlDialog.placeholder": "请输入以 .csv/.tsv/.json 结尾的数据地址",
  "dataset.urlDialog.helper.invalid": "URL 需指向 .csv/.tsv/.json 文件",
  "dataset.urlDialog.label": "数据 URL",
  "dataset.urlDialog.title": "通过 URL 加载数据",
  "dataset.upload.tooltip.disabled": "当前线上演示环境不支持文件上传，如需使用文件上传功能，请在本地安装并运行 Data Formulator。",

  // 粘贴数据对话框 & 上传提示
  "dataset.pasteDialog.title": "粘贴并上传数据",
  "dataset.pasteDialog.placeholder": "在此粘贴 CSV、TSV 或 JSON 内容，然后上传。",
  "dataset.pasteDialog.largeContent.preview": "检测到内容较大（约 {kb} KB），当前显示预览以提升性能。",
  "dataset.pasteDialog.largeContent.showFull": "查看全部",
  "dataset.pasteDialog.largeContent.showPreview": "仅看预览",
  "dataset.pasteDialog.sizeWarning": "⚠️ 内容大小超过 {mbLimit}MB 限制，当前约 {mb}MB。请改用“数据库”方式上传大数据集。",
  "dataset.button.loadDataset": "加载示例数据集",
  "dataset.dialog.explore.title": "浏览示例数据集",
  "dataset.preview.shape": "（{columns} 列 ⨉ {rows} 行）",
  "dataset.preview.rowsPart": " ⨉ {rows} 行",
  "dataset.preview.sourcePrefix": "来源：",

  // 上传内容大小限制
  "upload.sizeLimit.prefix": "内容大小超过 ",
  "upload.sizeLimit.suffix": " MB 的限制。",

  // 文件上传错误
  "upload.error.fileTooLarge.prefix": "文件 ",
  "upload.error.fileTooLarge.middle": " 过大（",
  "upload.error.fileTooLarge.suffix": "MB），请改用“数据库”方式上传。",
  "upload.error.unsupportedFormat.prefix": "不支持的文件格式：",
  "upload.error.unsupportedFormat.suffix": "。请使用 CSV、TSV、JSON 或 Excel 文件。",
  "upload.error.excelParse.prefix": "解析 Excel 文件失败：",
  "upload.error.excelParse.suffix": "。请检查文件格式后重试。",

   // 数据库与数据连接 / db.*
  "db.sidebar.dataTables": "数据表",
  "db.sidebar.derivedViews": "派生视图",
  "db.sidebar.noTables": "暂时没有可用的数据表。",
  "db.sidebar.refreshTables": "刷新表列表",
  "db.sidebar.cleanDerivedViewsTooltip": "清理未被当前会话引用的派生视图",

  "db.emptyState.noTables": "数据库当前为空，请刷新表列表或导入一些数据以开始使用。",

  "db.upload.tab.fileUpload": "文件上传",
  "db.upload.uploading": "正在上传…",
  "db.upload.cta": "上传 CSV/TSV 文件到本地数据库",

  "db.table.header.columnStatsPrefix": "字段统计 - ",
  "db.table.header.samplePrefix": "数据样本 - ",
  "db.table.header.shape": "（{columns} 列 × {rows} 行）",

  "db.table.button.showSamples": "查看数据样本",
  "db.table.button.showStats": "查看字段统计",
  "db.table.button.drop": "删除数据表",

  "db.loader.title": "数据连接器（{type}）",
  "db.loader.header": "数据连接器",
  "db.loader.mode.viewTables": "浏览远端表",
  "db.loader.mode.queryData": "编写查询",
  "db.loader.label.filter": "表名过滤",
  "db.loader.placeholder.filter": "仅加载名称包含关键字的表",
  "db.loader.button.connect": "连接",
  "db.loader.button.refresh": "刷新",
  "db.loader.button.disconnect": "断开连接",

  "db.message.ingestSuccess": "数据已成功导入会话。",
  "db.message.loadSuccess": "已成功加载查询示例数据。",
  "db.message.importSuccess": "查询结果已成功导入为数据表。",
  "db.message.viewQueryError": "获取查询样本失败，请稍后重试。",
  "db.message.importError": "导入查询结果失败，请稍后重试。",
  "db.message.tableRenamed": "表 {originalName} 已存在，已重命名为 {tableName}。",

  "db.query.clearResult": "清空结果",
  "db.query.label.importAs": "导入表名",
  "db.query.button.importData": "导入数据",
  "db.query.prefix.queryFromTables": "查询来源表：",
  "db.query.button.aiComplete": "根据选中表智能补全查询",
  "db.query.button.aiFix": "帮我修复当前错误",
  "db.query.button.run": "运行查询",

  "db.error.fetchTables": "获取表列表失败，请检查服务器是否已启动。",
  "db.error.uploadTable": "上传表失败，请检查服务器是否已启动或稍后重试。",
  "db.error.resetDatabase": "重置数据库失败，请稍后重试。",
  "db.error.deleteTable": "删除数据表失败，请检查服务器是否已启动。",
  "db.error.downloadDb": "下载数据库文件失败，请稍后重试。",

  "db.confirm.cleanDerivedViews": "确定要删除以下未被引用的派生视图吗？",
  "db.message.cleanedDerivedViews": "已删除 {count} 个未被引用的派生视图：{views}",
  "db.confirm.dropLoadedTable": "确定要删除数据表 {tableName} 吗？\n{tableName} 当前已加载到会话中，同时也会从数据库中移除。",
  "db.button.reset": "重置",
  "db.text.resetDatabase": " 后端数据库",

  // 编码货架 / EncodingShelfCard
  "encoding.tooltip.addBaseTables": "为当前数据整理添加更多基础数据表",
  "encoding.button.formulate": "整理数据",
  "encoding.tooltip.formulateOverride": "使用当前指令重新整理数据，并覆盖表 {tableId}。",

  "encoding.mode.ideas": "灵感模式",
  "encoding.mode.editor": "编辑模式",

  "encoding.ideas.header.ideas": "灵感",
  "encoding.ideas.button.ideas": "灵感列表",
  "encoding.ideas.button.get": "获取灵感",
  "encoding.ideas.button.different": "换一批灵感",
  "encoding.ideas.tooltip.getForVisualization": "根据当前图表和数据获取可视化灵感",
  "encoding.ideas.status.ideating": "正在生成灵感…",

  "encoding.devDialog.title": "来自开发者的一句话",
  "encoding.devDialog.body": "没想到你会点进这里，我们很高兴你在认真探索这个工具！如果有任何想法或建议，欢迎到 GitHub 给我们留言：",
  "encoding.devDialog.linkLabel": "github.com/microsoft/data-formulator",
  "encoding.devDialog.footer": "期待听到你的反馈。",

  "encoding.placeholder.visualize": "你想要可视化什么？",
  "encoding.placeholder.visualizeWithHint": "✏️ 描述一下你想看到的图表",
  "encoding.placeholder.formulate": "整理数据",
  "encoding.placeholder.formulateWithHint": "✏️ 描述你想如何整理数据",
  "encoding.placeholder.newFieldName": "输入新字段名称",
  "encoding.placeholder.field": "字段",

  // 概念解释 / ExplComponents
  "expl.concepts.tooltip.showFewer": "收起部分概念",
  "expl.concepts.tooltip.showAll": "展开全部概念",
  "expl.concepts.button.showFirst": "仅显示前 {count} 个概念",
  "expl.concepts.button.showAll": "显示全部 {count} 个概念",

  // 编码线程面板 / EncodingShelfThread
  "encoding.editor.open": "展开编辑器",
  "encoding.editor.hide": "收起编辑器",
  "encoding.editor.header": "编辑器",

  // Report 相关（简单翻译）
  "report.style.shortNote": "简短说明",
  "report.mode.compose": "撰写",
  "report.mode.post": "查看报告",

  // 报表视图 ReportView（常用 UI 文案）
  "report.style.shortNote.label": "简短说明",
  "report.style.blogPost.label": "博客文章",
  "report.style.socialPost.label": "社交媒体帖子",
  "report.style.socialThread.label": "社交媒体长帖",
  "report.style.execSummary.label": "管理层摘要",
  "report.mode.compose.label": "撰写报告",
  "report.mode.post.label": "已生成报告",
  "report.button.generate": "生成报告",
  "report.button.shareImage": "复制报告为图片",
  "report.button.copyMarkdown": "复制 Markdown 文本",
   "report.button.composing": "正在生成报告...",
  "report.error.noChartSelected": "请至少选择一个图表。",
  "report.error.generateFailed": "生成报告失败：{message}",
  "report.error.noModel": "尚未为生成槽位选择模型。",
  "report.message.captureNotFound": "无法找到要截图的报告内容。",
  "report.message.imageFailed": "生成报告图片失败，请重试。",
  "report.message.imageCopied": "报告图片已复制到剪贴板，可以粘贴到任意位置分享。",
  "report.message.imageCopyFailed": "复制到剪贴板失败，可能是浏览器不支持此功能。",
  "report.message.clipboardNotSupported": "当前浏览器不支持图片剪贴板，请使用现代浏览器。",
  "report.message.deleteConfirm": "当前报告已删除。",

  "report.compose.selectedCount": "已选择 {count} 个图表",
  "report.compose.noCharts": "当前没有可用于报告的图表，请先创建一些可视化。",
  "report.compose.loadingPreviews": "正在加载图表预览…",
  "report.compose.noAvailableCharts": "暂无可用图表，图表可能仍在加载或不可用。",

  // 顶部导航与模式切换
  "report.nav.backToExplore": "返回探索视图",
  "report.nav.viewReports": "查看报告",
  "report.style.createPrefix": "生成一份",
  "report.post.createNew": "重新创建报告",
  "report.post.aiWarning": "以下内容由 AI 基于所选图表生成，可能存在不准确之处，请务必审阅确认。",

  "report.tooltip.deleteReport": "删除报告",
  "report.tooltip.createChartifact": "在 Chartifact 中打开该报告",
  "report.button.createChartifact": "打开 Chartifact 报告",

  // 可视化视图 VisualizationView / vis.*
  "vis.sample.adjustLabel": "调整采样大小：{current} / {total} 行",
  "vis.sample.sliderLabel": "采样大小",
  "vis.sample.resample": "重新采样",
  "vis.sample.visualizingPrefix": "正在基于采样数据生成图表（",
  "vis.sample.rowsLabel": "行样本）",
  "vis.sample.tooltip.resample": "使用当前行数重新抽样",

  "vis.data.prefix": "数据源：",
  "vis.data.virtualTooltip": "该表存储在后端数据库中，当前仅加载部分样本用于可视化。",

  "vis.message.tablePrompt": "请先描述你想要看到的内容（例如：按年份汇总销售额）。",
  "vis.message.autoPrompt": "用自然语言描述你想看的图表，系统会推荐合适的可视化。",
  "vis.message.encodingEmpty": "请在左侧将字段拖入编码通道，或用自然语言描述你想看的图表。",
  "vis.message.chartUnavailable": "当前编码与数据不兼容，请调整字段或聚合方式后重试。",
  "vis.message.synthesisInProgress": "正在根据你的描述生成或更新图表…",
  "vis.message.aiResultWarning": "当前图表基于 AI 生成结果，可能存在偏差，请结合数据仔细核查。",

  "vis.zoom.out": "缩小图表",
  "vis.zoom.in": "放大图表",

  "vis.concepts.title": "派生概念与度量",
  "vis.explain.codeTitle": "数据转换代码",
  "vis.explain.explTitle": "数据转换说明",

  // 其他通用
  "common.ok": "确定",
  "common.close": "关闭",
  "common.save": "保存",
  "common.delete": "删除",
  "common.load": "加载",
  "common.upload": "上传",
  "common.edit": "编辑",
  "common.apply": "应用",
  "common.loading": "正在加载…",
  "common.or": "或",

  // 概念面板 / 字段
  "concept.group.newFields": "新建字段",
  "concept.cleanUnused.tooltip": "清理未使用的字段",
  "concept.showAll.prefix": "… 展开全部 ",
  "concept.showAll.suffix": " 个字段 ▾",
  "concept.panel.title": "数据字段",
  "concept.panel.operators": "字段运算",

  // 表格视图 / SelectableDataGrid
  "table.tooltip.viewRandom10k": "查看该表的 10000 行随机样本",

  // 概念卡片 / 派生字段
  "concept.form.nameLabel": "概念名称",
  "concept.form.nameExists": "该名称已存在，请使用其他名称。",
  "concept.form.deriveFrom": "来源字段：",
  "concept.form.sampleResult": "样例数据结果",
  "concept.form.codeTitle": "转换代码",
  "concept.form.sampleResult.full": "在示例数据上的转换结果",
  "concept.form.codeTitle.full": "转换代码",
  "concept.form.dialog.title.prefix": "从 ",
  "concept.form.dialog.title.middle": " 转换为 ",
  "concept.form.dialog.title.suffix": " 的变换",
  "concept.form.dialog.sampleTitle": "在示例数据上的转换结果",
  "concept.form.dialog.codeTitle": "转换代码",
  "concept.form.button.cancel": "取消",
  "concept.form.button.save": "保存",
  "concept.form.button.delete": "删除",
  "concept.form.button.zoom": "放大编辑",
  "concept.form.sampleTable.title": "在示例数据上的结果",
  "concept.form.preview.title": "预览：将概念 ",
  "concept.form.preview.middle": " 应用到表 ",

  // 概念重应用对话框 / Concept reapply dialog
  "concept.dialog.reapply.tooltip": "应用到表 {table}",
  "concept.dialog.reapply.title.prefix": "预览：将概念 ",
  "concept.dialog.reapply.title.middle": " 应用到表 ",
  "concept.dialog.reapply.title.suffix": "",
  "concept.dialog.reapply.codeLabel": "转换代码",
  "concept.dialog.reapply.previewLabel": "应用结果预览",

  // 编码面板 / 通道
  "encoding.channel.xAxis": "X 轴",
  "encoding.channel.yAxis": "Y 轴",
  "encoding.label.dataType": "数据类型",
  "encoding.label.stack": "堆叠方式",
  "encoding.label.sortBy": "排序依据",
  "encoding.label.sortOrder": "排序顺序",
  "encoding.label.colorScheme": "配色方案",
  "encoding.dtype.auto": "自动",
  "encoding.dtype.quantitative": "数值型",
  "encoding.dtype.nominal": "类别型",
  "encoding.dtype.temporal": "时间型",
  "encoding.stack.default": "默认",
  "encoding.stack.layered": "层叠",
  "encoding.stack.center": "居中",
  "encoding.stack.normalize": "百分比",
  "encoding.sort.auto": "自动",
  "encoding.sort.orderLabel": "排序顺序：",
  "encoding.sort.button.infer": "推断智能排序",
  "encoding.sortOrder.auto": "自动",
  "encoding.sortOrder.asc": "升序",
  "encoding.sortOrder.desc": "降序",
  "encoding.colorScheme.default": "默认",

  // Agent 规则对话框
  "agentRules.button": "智能体规则",
  "agentRules.title": "智能体规则",
  "agentRules.coding.title": "数据处理与代码规则",
  "agentRules.coding.subtitle": "约束智能体在编写数据转换与可视化推荐代码时的行为。",
  "agentRules.exploration.title": "探索与提问规则",
  "agentRules.exploration.subtitle": "约束智能体在生成问题、探索数据和发现洞见时的行为。",
  "agentRules.saveCoding": "保存代码规则",
  "agentRules.saveExploration": "保存探索规则",
  "agentRules.coding.placeholder": "示例规则：\n\n## 计算约定\n- ROI（投资回报率）统一按 (revenue - cost) / cost 计算。\n- 对日期字段做移动平均时，默认使用 7 天窗口。\n- 做预测任务时，默认先尝试线性模型。\n\n## 编码规范\n- 字符串列中用 '-' 代表缺失值时，统一转换为 ''.\n- 日期统一格式化为 'YYYY-MM-DD'。",
  "agentRules.exploration.placeholder": "示例规则：\n\n## 简洁优先\n- 问题要简明清晰，不要过度复杂化探索路径。\n\n## 提问生成\n- 当发现明显异常值时，生成问题进一步分析这些异常。\n\n## 领域知识\n- 在探索大规模商品数据时，优先关注按不同指标排序的前 20 名。",

  // 数据线程 / DataThread
  "dataThread.metadata.title.prefix": "为 ",
  "dataThread.metadata.title.suffix": " 附加元数据",
  "dataThread.metadata.label": "元数据",
  "dataThread.metadata.placeholder": "附加额外上下文或说明，帮助智能体更好理解和处理数据。",
  "dataThread.agent.thinking": "思考中…",
  "dataThread.agent.status.warning": "嗯…",
  "dataThread.agent.status.failed": "出错了",
  "dataThread.agent.status.completed": "已完成",
  "dataThread.agent.tooltip.delete": "删除消息",
  "dataThread.tableName.tooltip.edit": "编辑表名",
  "dataThread.chart.tooltip.delete": "删除图表",

  // 数据加载聊天（DataLoadingChat）
  "dataLoading.thinking": "正在提取数据…",
  "dataLoading.noData": "当前没有可预览的数据。",
  "dataLoading.button.extractFromImage": "从图片中提取数据",
  "dataLoading.button.loadTable": "加载为表格",
  "dataLoading.dialog.title": "智能清洗数据",
  "dataLoading.dialog.resetTooltip": "重置对话",
  "dataLoading.placeholder.image": "请描述你想从这张图片中提取的数据",
  "dataLoading.placeholder.followUp": "继续补充指令（例如：修正表头、去掉合计行、生成 15 行示例等）",
  "dataLoading.placeholder.initial": "粘贴网站、图片或文本内容，并说明要提取或清洗成什么样的数据",
  "dataLoading.preview.imageUrlPrefix": "图片地址：",
  "dataLoading.preview.dataUrlTitle": "数据地址",
  "dataLoading.preview.imageAlt": "来自 {name} 的图片",
  "dataLoading.preview.dataSource": "数据源",

  "dataLoading.button.stop": "停止生成",
  "dataLoading.button.deleteTable": "删除表",

  // 派生数据对话框 / DerivedDataDialog
  "derivedData.dialog.title": "派生数据候选",
  "derivedData.source.prefix": "转换来源：",
  "derivedData.button.deleteAll": "删除所有候选",
  "derivedData.button.save": "将候选 {index}（{tableId}）保存为结果",

  // ChatDialog 对话历史
  "chatDialog.title": "与智能体的对话",
  "chatDialog.noHistory": "当前还没有对话记录。",
  "chatDialog.role.user": "你",
  "chatDialog.role.assistant": "助手",

  // 系统消息 / Snackbar
  "messages.panel.tooltip.view": "查看系统消息",
  "messages.panel.header": "系统消息 ({count})",
  "messages.panel.clearAll": "清空所有消息",
  "messages.panel.empty": "当前还没有消息",
  "messages.detail.section": "[详情]",
  "messages.code.section": "[生成的代码]",
  "messages.last.detail.section": "[详情]",
  "messages.last.code.section": "[生成的代码]",

  // 探索 / 图表构建 过程中使用的消息
  "messages.example.loading": "正在加载示例会话：",
  "messages.example.loaded": "示例会话加载成功：",
  "messages.example.loadFailed": "加载示例会话失败：",
  "messages.chart.noTable": "尚未选择用于生成图表的数据表。",
  "messages.chart.formulationFailed": "数据整理失败，请重试。",
  "messages.chart.formulationSuccess": "字段 {fields} 的数据整理已完成。",
  "messages.chart.ideasFailed": "获取探索建议失败，请稍后重试。",
  "messages.chart.stepCompleted.prefix": "探索步骤 ",
  "messages.chart.stepCompleted.suffix": " 已完成：",
  "messages.chart.explorationCompleted": "数据探索已完成。",
  "messages.chart.agentLost.desc": "智能体在探索过程中迷路了。",
  "messages.chart.agentLost.toast": "智能体在数据中迷路了，请重试。",
  "messages.chart.explorationError.title": "数据探索出错",
  "messages.chart.explorationError.toast": "数据探索出错，请重试。",
  "messages.chart.explorationTimeout": "数据探索超时，请重试。",
  "messages.chart.explorationFailed.prefix": "数据探索失败：",
  "messages.encoding.autoSortFailed": "无法完成智能排序。",
  "messages.encoding.autoSortServerFailed": "由于服务器问题，无法完成智能排序。",
  "messages.chart.noResultReturned": "未从智能体获得有效结果，请重试。",
  "messages.chart.formulationTimeout": "数据整理在 {seconds} 秒后超时。请尝试拆分任务、更换模型或提高超时时间。",
  "messages.dataLoading.noResultReturned": "未能从响应中提取出有效的数据表。",
  "messages.dataLoading.stoppedByUser": "已按你的请求停止生成。",
  "messages.dataLoading.serverError.prefix": "服务器在处理数据时出错：",
  "messages.common.unknownError": "未知错误",

  // 概念相关系统消息
  "messages.concept.candidatesFound": "为概念 \"{name}\" 找到 {count} 个候选转换。",
  "messages.concept.candidatesEmpty": "未能为概念 \"{name}\" 找到合适的转换，请重试。",
  "messages.concept.generateFailed": "无法生成期望的转换，请重试。",

  // 页脚
  "footer.privacy": "隐私和 Cookie",
  "footer.terms": "使用条款",
  "footer.contact": "联系我们",
};
