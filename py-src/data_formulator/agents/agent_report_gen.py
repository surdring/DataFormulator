# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import json
import re

from data_formulator.agents.agent_utils import extract_json_objects, generate_data_summary
from data_formulator.agents.agent_sql_data_transform import  sanitize_table_name, get_sql_table_statistics_str

import logging

logger = logging.getLogger(__name__)


# 原英文提示词（保留作注释备份）
# SYSTEM_PROMPT = '''You are a journalist to help the user generate a short blog post based off the data and visualization provided by the user.
# The user will provide you:
# - the input data summary (the data analysis is based off) 
# - and a list of visualizations (and their corresponding data) that the user wants to include in the report.
# - the report style they want the report to be written in.
# Your job is to generate a short blog post based off the data and visualizations provided by the user. It should be a few paragraphs long, and be easy to read.
#
# Note:
# - You should not make any assumptions or judgments about a person's gender, biological sex, sexuality, religion, race, nationality, ethnicity, political stance, socioeconomic status, mental health, invisible disabilities, medical conditions, personality type, social impressions, emotional state, and cognitive state.
# - If that happens, highlight the the data may include biases, and suggest the user to be careful when interpreting the data.
#
# The report should have two components:
# 1. A short title of the report
# 2. Description of findings based on the charts and data.
#     - connect findings between different charts into a coherent story, write in a way that is easy to read and understand.
#     - include the image as part of the blog. Use a placeholder [IMAGE(chart_id)] to include the chart that will be replaced later.
#     - for each chart, write a bit about the what is the chart trying to answer and its findings (use its data as supporting evidence)
#     - descriptions should all be concise only show 2-3 most important findings for the chart.
# 3. conclude the blog with a summary of the findings and follows up questions.
#
# Writing style rules:
# - The report should be easy to read and understand, the total reading time should be 1 minute for the user, use no more than 200 words.
# - The report should be concise and to the point.
# - The output should be in markdown format:
#     - title should be in `# <title>`
#     - the content should just be paragraphs without subsection headers
#     - put image reference [IMAGE(chart_id)] in its own line among the texts at appropriate places (replace the chart_id with the actual chart_id, keep the format of [IMAGE(...)]).
#     - be flexible about using markdown syntax like bullet points, italics, bold, code blocks, tables, etc. to make the report more readable.
#     - the summary should be in a paragraph start with "**In summary**".
# - Note that the reader won't be able to see sample data or code, and the report should be self-contained (referring to the charts).
# - The user may provide you a desired writing style, that means the overall language should follow the style (not that the post should still be within 1min reading time).
#     - "blog post": "blog post", -- a blogpost that is published on a blog platform
#     - "social post": "social post", -- a social post that is published on a social media platform (should be shorter than a blog post)
#     - "executive summary": "executive summary", -- a summary of the report for executives, with more formal language and more details, and more bullet points
#     - "short note": "short note", -- a short note that is published on a social media platform, with no more than 300 characters in total, and there should be no more than 3 short sentences.
#
# The report should be lightweight, and respect facts in the data. Do not make up any facts or make judgements about the data.
# The report should be based off the data and visualizations provided by the user, do not make up any facts or make judgements about the data.
# Output markdown directly, do not need to include any other text.
# '''

# 新的中文系统提示词：要求用简体中文写 Markdown 报告，
# 具体结构和篇幅由后续 "style" 相关指令决定
SYSTEM_PROMPT = """
你是一名资深数据分析师和写作助手。你会阅读用户提供的数据表摘要和可视化图表说明，
根据这些信息用**简体中文**撰写结构清晰、逻辑严谨的分析报告。

你的总体目标：
1. 帮助非技术业务同事快速理解关键发现；
2. 用通俗易懂的语言解释图表呈现的趋势、对比和异常；
3. 明确给出结论和可执行的业务建议。

通用写作要求（对所有风格都适用）：
- **始终使用简体中文输出**；
- 报告使用 Markdown 格式（# 标题、## 小节、项目符号列表等）；
- 在引用具体图表时，用自然语言描述图表包含的信息和你观察到的现象，不需要输出图表代码；
- 如有不确定之处，要明确指出假设、数据限制或可能的偏差来源；
- 尊重数据事实，不捏造不存在的数据或结论；
- 对可能涉及敏感群体或数据偏差的部分，应提醒读者谨慎解读。

非常重要：
- 报告的**具体结构、篇幅、语气和侧重点**，必须严格遵循后续用户消息中给出的
  「写作风格（style）」与「结构说明」。
- 如果系统指令与你在用户消息中看到的风格说明存在冲突，
  以用户消息中的风格说明为准。
"""


def _build_style_instructions(style: str) -> str:
    """根据 style 决定不同类型报告的结构和篇幅要求。"""

    style_key = (style or "").strip().lower()

    if style_key == "short note":
        # 简短说明：极短、以结论为主，不展开长分析
        return (
            "报告类型：简短说明（short note）。"\
            "\n- 用 1 个一级标题作为报告标题，例如：`# 关键发现总结`；"\
            "\n- 正文总字数建议控制在 **150 字以内**；"\
            "\n- 可以直接使用一个无序列表列出 **2–4 条**核心结论，每条 1 句话为主；"\
            "\n- 不需要单独的小节标题，不必展开详细分析和风险，只保留最关键的结论和 1–2 条简短建议；"\
            "\n- 适合快速同步给已经熟悉业务背景的同事。"
        )

    if style_key == "social post":
        # 社交媒体帖子：语气更口语、适合社交媒体
        return (
            "报告类型：社交媒体帖子（social post）。"\
            "\n- 整体语气可以更口语化，适合发布到社交媒体（如朋友圈、企业内部动态等）；"\
            "\n- 结构建议："\
            "\n  1) 开头 1–2 句吸引注意力的引子（可以点出最有意思的发现）；"\
            "\n  2) 用 2–4 条无序列表列出主要发现，每条尽量简短；"\
            "\n  3) 末尾 1 句话给出简单结论或行动号召。"\
            "\n- 总体字数建议控制在 **200 字以内**，重点在于“好读、好转发”。"
        )

    if style_key == "executive summary":
        # 管理层摘要：正式、压缩、以结论和行动为主
        return (
            "报告类型：管理层摘要（executive summary）。"\
            "\n- 目标读者为时间有限的管理层，语言要正式、克制、以结论和行动为主；"\
            "\n- 建议按如下结构输出："\
            "\n  1) `# 执行摘要`：用 3–6 条无序列表，概括本次分析最重要的结论；"\
            "\n  2) `## 关键指标与发现`：按主题分点解释核心指标的变化和差异，可适当引用图表支撑；"\
            "\n  3) `## 风险与限制`：明确指出数据口径、样本、外部环境等可能带来的偏差；"\
            "\n  4) `## 建议与后续行动`：给出 3–5 条可执行的业务建议，每条最好以动词开头。"\
            "\n- 字数可以略长于简短说明，但仍需控制在**1–2 分钟阅读量**，避免大段叙事。"
        )

    # 默认：博客文章（blog post）或未知值，走相对完整的分析结构
    return (
        "报告类型：博客文章（blog post）。"\
        "\n- 面向希望系统学习数据结论的读者，可以适当展开故事性描述；"\
        "\n- 建议按如下结构输出 Markdown："\
        "\n  1) `# 报告标题`：用 1 句话点出主题；"\
        "\n  2) `## 背景与数据范围`：说明业务背景、数据来源、时间范围、主要字段等；"\
        "\n  3) `## 关键发现`：用 3–6 条无序列表列出整体结论；"\
        "\n  4) `## 细节分析`：按图表或主题分小节，解释趋势、对比和异常，适当引用具体数值；"\
        "\n  5) `## 风险与限制`：说明数据质量、口径假设、样本代表性等限制；"\
        "\n  6) `## 建议与后续行动`：结合前文结论，给出可执行的后续动作。"\
        "\n- 整体篇幅建议控制在 **3–6 个短段落**，既有故事性又不过度冗长。"
    )

class ReportGenAgent(object):

    def __init__(self, client, conn):
        self.client = client
        self.conn = conn

    def get_data_summary(self, input_tables):
        if self.conn:
            data_summary = ""
            for table in input_tables:
                table_name = sanitize_table_name(table['name'])
                table_summary_str = get_sql_table_statistics_str(self.conn, table_name)
                data_summary += f"[TABLE {table_name}]\n\n{table_summary_str}\n\n"
        else:
            data_summary = generate_data_summary(input_tables)
        return data_summary

    def _validate_report_against_data(self, report_text, input_tables, charts):
        """简单结构化校验：检查报告中提到的英文字段名是否存在于数据表/图表数据中。"""

        valid_fields = set()

        # 从 input_tables 收集字段
        for table in input_tables or []:
            rows = table.get("rows") or []
            if rows and isinstance(rows[0], dict):
                valid_fields.update(rows[0].keys())

        # 从每个图表的 chart_data 收集字段
        for chart in charts or []:
            chart_data = chart.get("chart_data") or {}
            rows = chart_data.get("rows") or []
            if rows and isinstance(rows[0], dict):
                valid_fields.update(rows[0].keys())

        if not valid_fields:
            return

        # 在报告中抽取看起来像英文字段名的 token
        candidates = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", report_text or ""))
        if not candidates:
            return

        unmatched = sorted(c for c in candidates if c not in valid_fields)
        if unmatched:
            # 只记录前若干个，避免日志过长
            logger.warning(
                "Report references fields not present in data: %s",
                ", ".join(unmatched[:20]),
            )

    def stream(self, input_tables, charts=[], style="blog post"):
        """derive a new concept based on the raw input data
        Args:
            - input_tables (list): the input tables to the agent
            - charts (list): the charts to the agent of format 
            [
                { 
                    "chart_id": ..., // the id of the chart 
                    "code": ..., // the code that derived this table
                    "chart_data": { "name": ..., "rows": ... }, 
                    "chart_url": ... // base64 encoded image
                }
            ]
            - style (str): the style of the report, can be "blog post" or "social post" or "executive summary" or "short note"
        Returns:
            generator: the result of the agent
        """

        data_summary = self.get_data_summary(input_tables)

        content = []

        content.append({
            'type': 'text',
            'text': f'''{data_summary}'''
        })

        for chart in charts:
            chart_data = chart['chart_data']
            chart_data_summary = self.get_data_summary([chart_data])
            content.append({
                'type': 'text',
                'text': f''' [CHART] - chart_id: {chart['chart_id']} \n\n - data summary:\n\n{chart_data_summary} \n\n - code:\n\n{chart['code']}'''
            })

        # 新的中文用户提示词：根据 style 选择不同的结构模板
        style_instructions = _build_style_instructions(style)

        user_prompt = {
            'role': 'user',
            'content': content + [{
                'type': 'text',
                'text': (
                    "下面是用于生成报告的数据摘要和图表信息。"\
                    "请你根据这些信息，用**简体中文**撰写一份 Markdown 报告。"\
                    f"\n\n{style_instructions}\n\n"\
                    "请严格遵循上述关于结构、篇幅和语气的要求，"\
                    "并确保所有结论和描述都可以在给定的数据与图表中找到依据。"
                )
            }]
        }

        system_message = {
            'role': 'system',
            'content': [ {'type': 'text', 'text': SYSTEM_PROMPT}]
        }

        messages = [
            system_message, 
            user_prompt
        ]
        
        ###### the part that calls open_ai
        stream = self.client.get_completion(messages = messages, stream=True)

        accumulated_content = ""
        
        for part in stream:
            if hasattr(part, 'choices') and len(part.choices) > 0:
                delta = part.choices[0].delta
                if hasattr(delta, 'content') and delta.content:
                    accumulated_content += delta.content
                    
                    # Stream each character for real-time display as JSON
                    yield delta.content

        # 在完整报告生成后做一次结构化一致性校验（仅记录日志，不影响用户体验）
        try:
            self._validate_report_against_data(accumulated_content, input_tables, charts)
        except Exception as e:
            logger.warning("Report validation check failed: %s", e)