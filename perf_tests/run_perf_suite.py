import sys
import time
from pathlib import Path
from typing import Any, List, Dict


# Ensure py-src is on sys.path so that `data_formulator` can be imported
REPO_ROOT = Path(__file__).resolve().parents[1]
PY_SRC = REPO_ROOT / "py-src"
if str(PY_SRC) not in sys.path:
    sys.path.insert(0, str(PY_SRC))

from data_formulator.agents.agent_utils import generate_data_summary  # type: ignore
from data_formulator.agents.agent_sql_data_transform import get_sql_table_statistics_str  # type: ignore
from data_formulator.agents.agent_interactive_explore import InteractiveExploreAgent  # type: ignore
from data_formulator.agents.agent_report_gen import ReportGenAgent  # type: ignore


def _build_in_memory_table(n_rows: int = 10000, n_cols: int = 30) -> Dict[str, Any]:
    """Construct a synthetic in-memory table for performance testing."""
    columns = [f"col_{i}" for i in range(n_cols)]
    rows: List[Dict[str, Any]] = []
    for i in range(n_rows):
        row = {col: (i % 100) for col in columns}
        rows.append(row)
    return {"name": "perf_table", "rows": rows, "attached_metadata": ""}


def _build_wide_table(n_rows: int = 1000, n_cols: int = 120) -> Dict[str, Any]:
    """Construct a very wide table to test summary truncation (many columns)."""
    columns = [f"col_{i}" for i in range(n_cols)]
    rows: List[Dict[str, Any]] = []
    for i in range(n_rows):
        row = {col: i for col in columns}
        rows.append(row)
    return {"name": "wide_table", "rows": rows, "attached_metadata": ""}


def benchmark_generate_data_summary() -> None:
    """Measure caching effect for generate_data_summary on a large in-memory table."""
    table = _build_in_memory_table()

    t1 = time.perf_counter()
    _ = generate_data_summary([table], include_data_samples=False)
    t2 = time.perf_counter()
    _ = generate_data_summary([table], include_data_samples=False)
    t3 = time.perf_counter()

    first_call = t2 - t1
    second_call = t3 - t2

    print("[generate_data_summary]")
    print(f"  first call:  {first_call:.4f} s")
    print(f"  second call: {second_call:.4f} s (should be significantly faster if cache works)")
    print()


def benchmark_sql_stats_cache() -> None:
    """Measure caching effect for get_sql_table_statistics_str using an in-memory DuckDB table."""
    try:
        import duckdb  # type: ignore
    except ImportError:
        print("[get_sql_table_statistics_str] duckdb not installed, skipping SQL stats benchmark.")
        print()
        return

    conn = duckdb.connect(":memory:")

    # Create a reasonably large table
    n_rows = 200_000
    conn.execute(
        """
        CREATE TABLE perf_sql AS
        SELECT
            i AS id,
            i % 100 AS category,
            i % 50 AS group_id,
            i * 0.1 AS value
        FROM range(?) t(i)
        """,
        [n_rows],
    )

    t1 = time.perf_counter()
    _ = get_sql_table_statistics_str(
        conn,
        "perf_sql",
        row_sample_size=5000,
        field_sample_size=20,
        max_val_chars=80,
    )
    t2 = time.perf_counter()
    _ = get_sql_table_statistics_str(
        conn,
        "perf_sql",
        row_sample_size=5000,
        field_sample_size=20,
        max_val_chars=80,
    )
    t3 = time.perf_counter()

    first_call = t2 - t1
    second_call = t3 - t2

    print("[get_sql_table_statistics_str]")
    print(f"  first call:  {first_call:.4f} s")
    print(f"  second call: {second_call:.4f} s (should be significantly faster if cache works)")
    print()


class DummyDelta:
    def __init__(self, content: str = "") -> None:
        self.content = content


class DummyChoice:
    def __init__(self, content: str = "") -> None:
        self.delta = DummyDelta(content)


class DummyPart:
    def __init__(self) -> None:
        self.choices = [DummyChoice("")]


class DummyStream:
    def __iter__(self):
        # Empty iterator – we don't need actual model output for context size checks
        return iter(())


class DummyClient:
    """Stub client that records messages passed to get_completion."""

    def __init__(self) -> None:
        self.last_messages = None

    def get_completion(self, messages, stream: bool = False):  # type: ignore[override]
        self.last_messages = messages
        return DummyStream()


def benchmark_interactive_explore_context_size() -> None:
    """Check that InteractiveExploreAgent builds a bounded-size context for large tables."""
    client = DummyClient()
    agent = InteractiveExploreAgent(client=client, agent_exploration_rules="", db_conn=None)

    # Build a large logical table: many rows and columns
    base_table = _build_in_memory_table(n_rows=10_000, n_cols=40)
    input_tables = [base_table]

    gen = agent.run(input_tables=input_tables, start_question=None, exploration_thread=None)

    # Trigger get_completion once so that DummyClient captures messages
    try:
        next(gen)
    except StopIteration:
        pass

    messages = client.last_messages or []
    if not messages:
        print("[InteractiveExploreAgent context] no messages captured, skipping.")
        print()
        return

    # For text-only mode, user message is a single string context
    user_msg = messages[1] if len(messages) > 1 else messages[-1]
    context = user_msg.get("content", "") if isinstance(user_msg, dict) else ""

    context_len = len(context)
    print("[InteractiveExploreAgent context]")
    print(f"  context length: {context_len} characters")

    # Soft check: context length should be bounded and not explode with raw data size
    hard_limit = 80_000
    if context_len > hard_limit:
        print(f"  WARNING: context length exceeds hard limit ({hard_limit}). Context trimming may not be effective.")
    else:
        print(f"  OK: context is under hard limit ({hard_limit}).")
    print()


def benchmark_multi_agent_summary_cache() -> None:
    """Check that multiple agents share cached data summaries instead of recomputing.

    为了避免依赖各 Agent 内部实现细节，这里只选择显式暴露了
    get_data_summary 方法的 Agent（ReportGenAgent、InteractiveExploreAgent），
    比较它们在缓存冷启动与缓存命中情况下的总耗时差异。
    """

    class DummyClient:
        def get_completion(self, *args, **kwargs):  # type: ignore[override]
            # Agents won't call this method in get_data_summary(), but define anyway.
            return None

    large_table = _build_in_memory_table(n_rows=20_000, n_cols=40)
    input_tables = [large_table]

    client = DummyClient()

    def run_all_agents_once() -> None:
        # ReportGenAgent
        report_agent = ReportGenAgent(client=client, conn=None)
        _ = report_agent.get_data_summary(input_tables)

        # InteractiveExploreAgent（非 SQL 分支）
        explore_agent = InteractiveExploreAgent(client=client, agent_exploration_rules="", db_conn=None)
        _ = explore_agent.get_data_summary(input_tables)

    # First pass: cold cache
    t1 = time.perf_counter()
    run_all_agents_once()
    t2 = time.perf_counter()

    # Second pass: warm cache (all agents ask for same table summary again)
    run_all_agents_once()
    t3 = time.perf_counter()

    first_pass = t2 - t1
    second_pass = t3 - t2

    print("[multi_agent_summary_cache]")
    print(f"  first pass (cold cache):  {first_pass:.4f} s")
    print(f"  second pass (warm cache): {second_pass:.4f} s")
    print("  Expect warm pass to be noticeably faster if generate_data_summary cache is shared across agents.")
    print()


def benchmark_summary_truncation_checks() -> None:
    """Verify that very wide/large tables produce truncated summaries within reasonable length."""

    # Table with many rows and many columns
    wide_table = _build_wide_table(n_rows=6000, n_cols=120)

    summary = generate_data_summary([wide_table], include_data_samples=False)
    length = len(summary)

    print("[generate_data_summary truncation]")
    print(f"  summary length: {length} characters")

    # Heuristic checks based on MAX_SUMMARY_ROWS/MAX_SUMMARY_COLUMNS design:
    # 1) Should contain truncated-columns indicator when there are more columns than limit.
    truncated_marker = "more columns truncated"
    if truncated_marker in summary:
        print(f"  OK: found truncation marker '{truncated_marker}'.")
    else:
        print(f"  WARNING: truncation marker '{truncated_marker}' not found; column truncation may not be applied.")

    # 2) Length should be large but not explode (soft upper bound).
    soft_upper = 200_000
    if length > soft_upper:
        print(f"  WARNING: summary length exceeds soft upper bound ({soft_upper}).")
    else:
        print(f"  OK: summary length under soft upper bound ({soft_upper}).")
    print()


def main() -> None:
    print("=== Performance regression suite ===")
    print(f"Repo root: {REPO_ROOT}")
    print()

    benchmark_generate_data_summary()
    benchmark_sql_stats_cache()
    benchmark_interactive_explore_context_size()
    benchmark_multi_agent_summary_cache()
    benchmark_summary_truncation_checks()


if __name__ == "__main__":
    main()
