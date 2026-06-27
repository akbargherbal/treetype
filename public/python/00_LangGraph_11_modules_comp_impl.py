# ==============================================================================
# LangGraph_Complete_Implementations.py
#
# This file consolidates the complete, finalized implementations of all 11
# modules. Each module is kept exactly in its original form as provided in
# the course files, preserving the native classes, variables, and namespaces.
# ==============================================================================

# ==============================================================================
# Module 1 — From Raw LLM Calls to a Typed Graph
# ==============================================================================

from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# ── State ──────────────────────────────────────────────────────────────────────
class PipelineState(TypedDict):
    task: str  # the coding task description
    code: str  # current draft; overwritten by each writer pass
    review_notes: str  # feedback from the reviewer; overwritten by each review pass


# ── Nodes ──────────────────────────────────────────────────────────────────────
def writer_node(state: PipelineState) -> dict:
    """Generates a code draft for the given task.

    Module 2 will replace the stub below with a real DeepSeek call:
        deepseek_client.chat.completions.create(model=DEEPSEEK_MODEL, messages=[...])
    For now, we use a hardcoded stub so the graph runs without an API key.
    """
    draft = f"# Task: {state['task']}\ndef solution():\n    pass"
    return {"code": draft}


def reviewer_node(state: PipelineState) -> dict:
    """Reviews the current code draft and records feedback.

    Module 2 will replace the stub below with a real DeepSeek call.
    The key insight: it reads state['code'] (set by the writer) and writes
    state['review_notes'] — the writer never handed anything to the reviewer directly.
    """
    feedback = "Missing implementation — function body is empty."
    return {"review_notes": feedback}


# ── Graph ──────────────────────────────────────────────────────────────────────
builder = StateGraph(PipelineState)

builder.add_node("writer", writer_node)
builder.add_node("reviewer", reviewer_node)

builder.add_edge(START, "writer")
builder.add_edge("writer", "reviewer")
builder.add_edge("reviewer", END)

graph = builder.compile()


# ==============================================================================
# Module 2 — Conditional Routing: Explicit Control Flow
# ==============================================================================

from typing import TypedDict, Optional, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.managed import RemainingSteps

# ── Domain types ──────────────────────────────────────────────────────────────


class CodeFile(TypedDict):
    filename: str
    content: str


class ReviewNotes(TypedDict):
    meets_requirements: bool
    feedback: str


class TestResults(TypedDict):
    passed: bool
    error_log: str


# ── Pipeline state ────────────────────────────────────────────────────────────


class PipelineState(TypedDict):
    requirements: str
    code: Optional[CodeFile]
    review_notes: Optional[ReviewNotes]
    test_results: Optional[TestResults]
    remaining_steps: RemainingSteps  # managed; do NOT pass in invoke() dict


# ── Nodes ─────────────────────────────────────────────────────────────────────


def writer_node(state: PipelineState) -> dict:
    # Module 3: replace stub with deepseek_client.chat.completions.create(...)
    # Revision pass will include state['review_notes']['feedback'] in the prompt.
    if state.get("code") is None:
        content = "def add(a, b): return a + b\n"
    else:
        content = "def add(a, b): return a + b  # fixed per review\n"
    return {"code": CodeFile(filename="add.py", content=content)}


def reviewer_node(state: PipelineState) -> dict:
    # Module 3: replace stub with deepseek_client.chat.completions.create(...)
    # Response parsed into ReviewNotes JSON.
    code = state["code"]
    if code and "fixed" not in code["content"]:
        review = ReviewNotes(
            meets_requirements=False, feedback="needs an inline comment"
        )
    else:
        review = ReviewNotes(meets_requirements=True, feedback="looks good")
    return {"review_notes": review}


def tester_node(state: PipelineState) -> dict:
    # Module 3: replace stub with actual code execution in a sandbox.
    code = state["code"]
    if code and "add" in code["content"]:
        results = TestResults(passed=True, error_log="")
    else:
        results = TestResults(passed=False, error_log="NameError: 'add' not defined")
    return {"test_results": results}


def human_review(state: PipelineState) -> dict:
    print(">>> Human review: code approved and ready to merge.")
    return {}


def needs_human(state: PipelineState) -> dict:
    print(">>> ESCALATION: too many retries — routing to human intervention.")
    print(f"    Last error: {state['test_results']['error_log']}")
    return {}


# ── Routers ───────────────────────────────────────────────────────────────────


def route_after_reviewer(state: PipelineState) -> Literal["tester", "writer"]:
    if state["review_notes"]["meets_requirements"]:
        return "tester"
    return "writer"


def route_after_tester(
    state: PipelineState,
) -> Literal["human_review", "writer", "needs_human"]:
    if state["remaining_steps"] <= 4:
        return "needs_human"
    if state["test_results"]["passed"]:
        return "human_review"
    return "writer"


# ── Graph ─────────────────────────────────────────────────────────────────────

builder = StateGraph(PipelineState)
builder.add_node("writer", writer_node)
builder.add_node("reviewer", reviewer_node)
builder.add_node("tester", tester_node)
builder.add_node("human_review", human_review)
builder.add_node("needs_human", needs_human)

builder.add_edge(START, "writer")
builder.add_edge("writer", "reviewer")
builder.add_conditional_edges(
    "reviewer",
    route_after_reviewer,
    {"tester": "tester", "writer": "writer"},
)
builder.add_conditional_edges(
    "tester",
    route_after_tester,
    {"human_review": "human_review", "writer": "writer", "needs_human": "needs_human"},
)
builder.add_edge("human_review", END)
builder.add_edge("needs_human", END)

graph = builder.compile()


# ==============================================================================
# Module 3 — Reflection & Self-Correction Loops: Building a Self-Healing Code Pipeline
# ==============================================================================

import operator
import subprocess
import sys
from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage


class PipelineState(TypedDict):
    task: str
    code: str
    review_notes: str
    test_results: dict
    attempt_count: int
    history: Annotated[list, operator.add]


# ── Nodes ─────────────────────────────────────────────────────────────────────


def writer_node(state: PipelineState) -> dict:
    base_prompt = f"Task: {state['task']}\n\nCurrent code (if any): {state.get('code', 'None')}\n\n"

    review_notes = state.get("review_notes")
    test_results = state.get("test_results")

    if review_notes and review_notes != "approved":
        prompt = (
            base_prompt
            + f"A code reviewer rejected this code with the following notes:\n{review_notes}\n\nFix the code. Return ONLY the corrected Python code, no extra text."
        )
    elif test_results and test_results.get("failures"):
        failures_text = "\n".join(test_results["failures"])
        prompt = (
            base_prompt
            + f"The previous code failed with these test errors:\n{failures_text}\n\nFix the code. Return ONLY the corrected Python code, no extra text."
        )
    else:
        prompt = (
            base_prompt + "Write the Python code. Return ONLY the code, no extra text."
        )

    response = llm.invoke(
        [
            SystemMessage(content="You are a code writer."),
            HumanMessage(content=prompt),
        ]
    )
    return {"code": response.content.strip()}


def reviewer_node(state: PipelineState) -> dict:
    prompt = f"""Task: {state['task']}

Code:
{state['code']}

Does this code satisfy every requirement in the task description? Answer YES or NO on the first line. If NO, give specific, actionable notes about exactly what is missing or wrong."""
    response = llm.invoke(
        [
            SystemMessage(content="You are a careful code reviewer."),
            HumanMessage(content=prompt),
        ]
    )
    verdict = response.content.strip()
    if verdict.upper().startswith("YES"):
        return {"review_notes": "approved"}
    return {"review_notes": verdict}


def tester_node(state: PipelineState) -> dict:
    with open("/tmp/temp_code.py", "w") as f:
        f.write(state["code"])

    result = subprocess.run(
        [sys.executable, "/tmp/test_runner.py"],
        capture_output=True,
        text=True,
    )

    failures = []
    if result.returncode != 0:
        for line in (result.stdout + result.stderr).splitlines():
            if "FAIL" in line or "AssertionError" in line:
                failures.append(line.strip())
        if not failures:
            failures.append("Execution failed. Check for syntax or runtime errors.")

    passed = result.returncode == 0

    new_count = state.get("attempt_count", 0) + 1

    return {
        "test_results": {
            "passed": passed,
            "failures": failures,
            "logs": result.stdout + result.stderr,
        },
        "attempt_count": new_count,
        "history": [f"attempt {new_count}: {'passed' if passed else 'failed'}"],
    }


def human_review_node(state: PipelineState) -> dict:
    return state


def needs_human_node(state: PipelineState) -> dict:
    return state


# ── Routers ───────────────────────────────────────────────────────────────────


def route_after_reviewer(state: PipelineState) -> Literal["tester", "writer"]:
    if state["review_notes"] == "approved":
        return "tester"
    return "writer"


def route_after_tester(
    state: PipelineState,
) -> Literal["human_review", "writer", "needs_human"]:
    if state["attempt_count"] >= 4:
        return "needs_human"
    if state["test_results"]["passed"]:
        return "human_review"
    return "writer"


# ── Graph Assembly ────────────────────────────────────────────────────────────

builder = StateGraph(PipelineState)
builder.add_node("writer", writer_node)
builder.add_node("reviewer", reviewer_node)
builder.add_node("tester", tester_node)
builder.add_node("human_review", human_review_node)
builder.add_node("needs_human", needs_human_node)

builder.add_edge(START, "writer")
builder.add_edge("writer", "reviewer")
builder.add_conditional_edges(
    "reviewer",
    route_after_reviewer,
    {"tester": "tester", "writer": "writer"},
)
builder.add_conditional_edges(
    "tester",
    route_after_tester,
    {"writer": "writer", "human_review": "human_review", "needs_human": "needs_human"},
)
builder.add_edge("human_review", END)
builder.add_edge("needs_human", END)

graph = builder.compile()


# ==============================================================================
# Module 4 — Multi-Agent Orchestration — Command, Supervisors, and When Not to Over-Engineer
# ==============================================================================

from typing import TypedDict, Optional, Annotated, Literal, List
import operator
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command


# ── Pipeline State ────────────────────────────────────────────────────────────
class PipelineState(TypedDict):
    task: str
    code: Optional[str]
    review_notes: Optional[dict]
    test_results: Optional[dict]
    attempt_count: int
    history: Annotated[List[str], operator.add]


# ── Node Functions ────────────────────────────────────────────────────────────
def writer_node(state: PipelineState) -> dict:
    attempt = state.get("attempt_count", 0) + 1
    code = (
        f"def solve(x):\n"
        f"    # Attempt {attempt} at: {state['task']}\n"
        f"    return x  # placeholder"
    )
    return {
        "code": code,
        "attempt_count": attempt,
        "history": [f"writer: attempt {attempt}"],
    }


def reviewer_node_v1(
    state: PipelineState,
) -> Command[Literal["tester_node", "writer_node"]]:
    approved = state.get("attempt_count", 0) >= 2
    notes = {
        "approved": approved,
        "feedback": "Good to go." if approved else "Needs work — try again.",
    }
    dest = "tester_node" if notes["approved"] else "writer_node"
    return Command(
        goto=dest,
        update={
            "review_notes": notes,
            "history": [f"reviewer: {'approved' if approved else 'rejected'}"],
        },
    )


def tester_node_v1(state: PipelineState) -> Command[Literal["__end__", "writer_node"]]:
    results = {"passed": True, "output": "All assertions pass."}
    dest = END if results["passed"] else "writer_node"
    return Command(
        goto=dest,
        update={
            "test_results": results,
            "history": ["tester: all tests passed"],
        },
    )


# ── Graph Assembly ────────────────────────────────────────────────────────────
final_builder = StateGraph(PipelineState)
final_builder.add_node("writer_node", writer_node)
final_builder.add_node("reviewer_node", reviewer_node_v1)
final_builder.add_node("tester_node", tester_node_v1)
final_builder.add_edge(START, "writer_node")
final_builder.add_edge("writer_node", "reviewer_node")
# reviewer_node and tester_node route themselves via Command

final_graph = final_builder.compile()


# ==============================================================================
# Module 5 — Cyclic Agent Loops — Building a ReAct Tester
# ==============================================================================

import subprocess
from typing import Annotated, TypedDict, Literal
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.errors import GraphRecursionError
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import Command


# ── State Schema ──────────────────────────────────────────────────────────────
class PipelineState(TypedDict):
    code: str  # current version of the code under review
    test_path: str  # path to the test file
    test_results: dict  # filled in by the tester; read by the writer


# ── Outer Nodes ───────────────────────────────────────────────────────────────
def writer_node(state: PipelineState) -> dict:
    feedback = state.get("test_results", {}).get("feedback", "no feedback yet")
    print(f"  [writer] received feedback → {feedback[:120]}")
    return {}


def reviewer_node(state: PipelineState) -> dict:
    print("  [reviewer] reviewing code… approved")
    return {}


def human_review_node(state: PipelineState) -> dict:
    print("  [human_review] tests passed — code is ready for merge")
    return {}


# ── ReAct Loop Tools ──────────────────────────────────────────────────────────
@tool
def run_pytest(test_path: str) -> str:
    """Run pytest on the given test file. Returns stdout + stderr."""
    result = subprocess.run(
        ["python", "-m", "pytest", test_path, "-v", "--tb=short", "--no-header"],
        capture_output=True,
        text=True,
        cwd=DEMO_DIR,
    )
    return result.stdout + result.stderr


@tool
def read_file(file_path: str) -> str:
    """Read and return the full contents of a file."""
    try:
        with open(file_path) as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: file not found at {file_path}"


# ── ReAct Loop State Definition and Outer Compilation ─────────────────────────
# (tester_loop compiled structure and tool node assignments)
tester_tools = [run_pytest, read_file]
tester_llm = llm.bind_tools(tester_tools)


def reason(state: MessagesState) -> dict:
    response = tester_llm.invoke(state["messages"])
    return {"messages": [response]}


loop_builder = StateGraph(MessagesState)
loop_builder.add_node("reason", reason)
loop_builder.add_node("tools", ToolNode(tester_tools))
loop_builder.add_edge(START, "reason")
loop_builder.add_conditional_edges("reason", tools_condition)
loop_builder.add_edge("tools", "reason")  # ← loop back!
tester_loop = loop_builder.compile()


# ── Upgraded Tester Node with Graceful Escalation ─────────────────────────────
def tester_node(
    state: PipelineState,
) -> Command[Literal["human_review_node", "writer_node"]]:
    """
    LLM-powered tester.  Invokes an inner ReAct loop (capped at 10 steps)
    to run pytest and, if needed, read source files before producing a verdict.
    If the loop does not converge, routes to human_review_node with a clear
    failure description so the run does not silently hang.
    """
    prompt = (
        f"Test the code at '{state['test_path']}'. "
        "Run the tests. If they fail, also read the relevant source files "
        "to understand whether the bug is in the test or the implementation. "
        "End your response with exactly one of:\n"
        "  • 'ALL TESTS PASSED' — if every test passed.\n"
        "  • A specific description of what needs to be fixed and where."
    )

    try:
        inner_result = tester_loop.invoke(
            {"messages": [HumanMessage(content=prompt)]},
            config={"recursion_limit": 10},  # private cap for this episode
        )
        final_msg = inner_result["messages"][-1]
        passed = final_msg.content.strip().rstrip(".*` ").endswith("ALL TESTS PASSED")
        feedback = final_msg.content

    except GraphRecursionError:
        passed = False
        feedback = (
            "Tester exceeded maximum steps and could not determine the test result. "
            "Manual review required."
        )

    return Command(
        update={"test_results": {"passed": passed, "feedback": feedback}},
        goto="human_review_node" if passed else "writer_node",
    )


# ── Graph Assembly ────────────────────────────────────────────────────────────
outer_v2 = StateGraph(PipelineState)
outer_v2.add_node("writer_node", writer_node)
outer_v2.add_node("reviewer_node", reviewer_node)
outer_v2.add_node("tester_node", tester_node)
outer_v2.add_node("human_review_node", human_review_node)

outer_v2.add_edge(START, "writer_node")
outer_v2.add_edge("writer_node", "reviewer_node")
outer_v2.add_edge("reviewer_node", "tester_node")
outer_v2.add_edge("human_review_node", END)

pipeline_v2 = outer_v2.compile()


# ==============================================================================
# Module 6 — Human-in-the-Loop — Interrupts, Checkpointing, and Resumption
# ==============================================================================

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt
from langgraph.checkpoint.memory import MemorySaver


# ── State Schema ──────────────────────────────────────────────────────────────
class PipelineState(TypedDict):
    task: str
    code: str
    review_feedback: str
    test_results: str
    attempt_count: int
    human_decision: str
    review_notes: dict


# ── Node Functions ────────────────────────────────────────────────────────────
def writer_node(state: PipelineState) -> Command[Literal["reviewer_node"]]:
    new_code = (
        f"# Implementation for: {state['task']} (attempt {state['attempt_count']})"
    )
    return Command(goto="reviewer_node", update={"code": new_code})


def reviewer_node(
    state: PipelineState,
) -> Command[Literal["writer_node", "tester_node"]]:
    if "needs work" in state.get("review_feedback", ""):
        return Command(
            goto="writer_node", update={"attempt_count": state["attempt_count"] + 1}
        )
    return Command(goto="tester_node", update={"review_feedback": "approved"})


def tester_node(
    state: PipelineState,
) -> Command[Literal["writer_node", "human_review_node"]]:
    if "fail" in state.get("test_results", ""):
        return Command(
            goto="writer_node", update={"attempt_count": state["attempt_count"] + 1}
        )
    return Command(
        goto="human_review_node", update={"test_results": "all tests passing"}
    )


def human_review_node(
    state: PipelineState,
) -> Command[Literal["merge_node", "writer_node"]]:
    # Pure computation only before interrupt — safe to repeat on re-entry.
    payload = {
        "task": state["task"],
        "code": state["code"],
        "test_results": state["test_results"],
        "question": "Approve this code for merge?",
    }

    decision = interrupt(payload)

    # Side effects after interrupt — execute exactly once per human response.
    print(f"[human_review_node] decision received: '{decision}'")

    if decision == "approve":
        return Command(goto="merge_node", update={"human_decision": decision})

    # Prevent unbounded loops: after five rejections, escalate rather than loop.
    if state["attempt_count"] >= 5:
        print("[human_review_node] Max attempts reached. Escalating to merge.")
        return Command(
            goto="merge_node",
            update={
                "human_decision": decision,
                "review_notes": {"escalated": True, "reason": "max attempts reached"},
            },
        )

    # Any non-approve response is a rejection with feedback for the Writer.
    return Command(
        goto="writer_node",
        update={
            "human_decision": decision,
            "review_notes": {"human_rejected": True, "reason": decision},
            "attempt_count": state["attempt_count"] + 1,
        },
    )


def merge_node(state: PipelineState) -> dict:
    notes = state.get("review_notes", {})
    if notes.get("escalated"):
        print(f"[merge_node] Escalated merge: {state['code']}")
    else:
        print(f"[merge_node] Approved merge: {state['code']}")
    return {}


# ── Graph Assembly ────────────────────────────────────────────────────────────
builder = StateGraph(PipelineState)
builder.add_node("writer_node", writer_node)
builder.add_node("reviewer_node", reviewer_node)
builder.add_node("tester_node", tester_node)
builder.add_node("human_review_node", human_review_node)
builder.add_node("merge_node", merge_node)

builder.add_edge(START, "writer_node")
builder.add_edge("merge_node", END)

graph = builder.compile(checkpointer=MemorySaver())


# ==============================================================================
# Module 7 — Durable Execution & Resumability in LangGraph
# ==============================================================================

import operator
from typing import Annotated, TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver


# ── State Schema ──────────────────────────────────────────────────────────────
class PipelineState(TypedDict):
    messages: Annotated[list[str], operator.add]
    draft: str | None
    review_feedback: str | None
    approved: bool | None
    test_results: str | None


# ── Node Functions ────────────────────────────────────────────────────────────
def writer_node(state):
    feedback = state.get("review_feedback")
    draft = (
        "draft v1: a rough first pass"
        if feedback is None
        else "draft v2: a good, much improved pass"
    )
    return {"draft": draft, "messages": [f"Writer produced: {draft}"]}


def reviewer_node(state):
    draft = state["draft"]
    approved = "good" in draft
    feedback = (
        None if approved else "Please revise: the draft needs to be good enough to ship"
    )
    return {
        "approved": approved,
        "review_feedback": feedback,
        "messages": [f"Reviewer: approved={approved}"],
    }


def tester_node(state):
    # In production this would shell out to pytest or call a CI API.
    return {
        "test_results": "All tests passed",
        "messages": ["Tester: All tests passed"],
    }


def should_continue(state) -> Literal["tester_node", "writer_node"]:
    return "tester_node" if state.get("approved") else "writer_node"


# ── Graph Assembly ────────────────────────────────────────────────────────────
builder = StateGraph(PipelineState)
builder.add_node("writer_node", writer_node)
builder.add_node("reviewer_node", reviewer_node)
builder.add_node("tester_node", tester_node)
builder.add_edge(START, "writer_node")
builder.add_edge("writer_node", "reviewer_node")
builder.add_conditional_edges(
    "reviewer_node",
    should_continue,
    {"tester_node": "tester_node", "writer_node": "writer_node"},
)
builder.add_edge("tester_node", END)

with SqliteSaver.from_conn_string("pipeline_checkpoints.db") as checkpointer:
    durable_graph = builder.compile(checkpointer=checkpointer)


# ==============================================================================
# LangGraph Module 8: Time-Travel Debugging
# ==============================================================================

import operator
from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver


# ── State Schema ──────────────────────────────────────────────────────────────
class SafeAccumState(TypedDict):
    code: str
    review_notes: dict
    test_results: Annotated[list, operator.add]  # Reducer accumulates all test results
    attempt_count: int


# ── Node Functions ────────────────────────────────────────────────────────────
def smart_writer_node(state: SafeAccumState) -> dict:
    attempt = state.get("attempt_count", 0)
    history_list = state.get("test_results", [])

    # Analyze the accumulated history of failures
    consecutive_failures = sum(1 for res in history_list if "FAIL" in res)

    # If the smart writer sees 2 or more consecutive failures, it realizes
    # that its structural comments are cosmetic and writes the true max() fix.
    if consecutive_failures >= 2:
        code = """def find_max(lst):
    return max(lst)  # Intelligent fix based on accumulated failures"""
    else:
        code = call_fixer_llm(state["code"], attempt=attempt)

    print(f"  [smart-writer] attempt {attempt} generated code")
    return {"code": code, "attempt_count": attempt + 1}


def tester_node_v2(state: SafeAccumState) -> dict:
    # We return to the strict test suite to prove logical correctness
    results = run_tests_strict(state["code"])
    print(f"  [tester] result: {results}")
    return {
        "test_results": [results]
    }  # Return as list to trigger the operator.add reducer


# ── Graph Assembly ────────────────────────────────────────────────────────────
fixed_builder = StateGraph(SafeAccumState)
fixed_builder.add_node("writer_node", smart_writer_node)
fixed_builder.add_node("reviewer_node", reviewer_node)
fixed_builder.add_node("tester_node", tester_node_v2)
fixed_builder.add_node("human_review_node", human_review_node)

fixed_builder.add_edge(START, "writer_node")
fixed_builder.add_edge("writer_node", "reviewer_node")

fixed_builder.add_conditional_edges(
    "reviewer_node",
    next_after_reviewer,
    {"writer_node": "writer_node", "tester_node": "tester_node"},
)
fixed_builder.add_conditional_edges(
    "tester_node",
    # Adapt next_after_tester to inspect the latest item in the accumulated list
    lambda s: "human_review_node" if s["test_results"][-1] == "PASS" else "writer_node",
    {"writer_node": "writer_node", "human_review_node": "human_review_node"},
)
fixed_builder.add_edge("human_review_node", END)

fixed_checkpointer = InMemorySaver()
fixed_graph = fixed_builder.compile(checkpointer=fixed_checkpointer)


# ==============================================================================
# Module 9: Streaming Intermediate State
# ==============================================================================

import time
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver
from langgraph.config import get_stream_writer


# ── State Schema ──────────────────────────────────────────────────────────────
class PipelineState(TypedDict):
    code: str
    review_feedback: str
    test_results: dict
    attempt_count: int
    human_approved: bool


# ── Node Functions ────────────────────────────────────────────────────────────
def writer_node(state: PipelineState) -> dict:
    time.sleep(0.5)
    new_code = state.get("code", "") + "\ndef test():\n    return 42"
    return {"code": new_code}


def reviewer_node(state: PipelineState) -> dict:
    time.sleep(0.5)
    return {"review_feedback": "looks good"}


def tester_node(state: PipelineState) -> dict:
    stream = get_stream_writer()
    for i in range(3):
        time.sleep(1)
        stream({"phase": "test_step", "step": i, "total": 3})
    if state["attempt_count"] % 2 == 0:
        return {"test_results": {"passed": True}}
    else:
        return {"test_results": {"passed": False}}


def human_review_node(state: PipelineState) -> dict:
    decision = interrupt(f"Approve code: {state['code']}? (y/n)")
    return {"human_approved": decision == "y"}


def route_after_review(state: PipelineState) -> str:
    return (
        "tester_node"
        if state.get("review_feedback") == "looks good"
        else "human_review_node"
    )


def route_after_test(state: PipelineState) -> str:
    return "human_review_node" if state["test_results"]["passed"] else "writer_node"


# ── Graph Assembly ────────────────────────────────────────────────────────────
builder = StateGraph(PipelineState)

builder.add_node("writer_node", writer_node)
builder.add_node("reviewer_node", reviewer_node)
builder.add_node("tester_node", tester_node)
builder.add_node("human_review_node", human_review_node)

builder.add_edge(START, "writer_node")
builder.add_edge("writer_node", "reviewer_node")
builder.add_conditional_edges("reviewer_node", route_after_review)
builder.add_conditional_edges("tester_node", route_after_test)
builder.add_edge("human_review_node", END)

graph = builder.compile(checkpointer=MemorySaver())


# ==============================================================================
# Module 10: Subgraphs and Parallel Fan-Out
# ==============================================================================

import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from langgraph.checkpoint.memory import MemorySaver

# ── Pattern 1: Formal Subgraph Mounting ───────────────────────────────────────
builder = StateGraph(PipelineState)
builder.add_node("writer_node", writer_node)
builder.add_node("reviewer_node", reviewer_node)
builder.add_node("tester_node", compiled_tester_graph)
builder.add_node("human_review_node", human_review_node)

builder.add_edge(START, "writer_node")
builder.add_edge("writer_node", "reviewer_node")
builder.add_edge("reviewer_node", "tester_node")
builder.add_edge("tester_node", "human_review_node")
builder.add_edge("human_review_node", END)

graph = builder.compile(checkpointer=MemorySaver())


# ── Pattern 2: Dynamic Parallel Fan-out via Send ──────────────────────────────
class CandidateState(TypedDict):
    task: str
    num_candidates: int
    candidates: Annotated[list[dict], operator.add]


candidate_builder = StateGraph(CandidateState)
candidate_builder.add_node("writer_variant", writer_variant)
candidate_builder.add_conditional_edges(START, fan_out_to_candidates)
candidate_builder.add_edge("writer_variant", END)

candidate_graph = candidate_builder.compile()


# ==============================================================================
# Module 11 — LangGraph Capstone: A Code-Review Pipeline, Built Piece by Piece
# ==============================================================================

from typing import TypedDict, Literal, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.config import get_stream_writer
from langgraph.managed import RemainingSteps


class PipelineState(TypedDict):
    task: str
    code: str
    review_notes: dict
    test_results: dict
    attempt_count: int
    human_decision: str
    remaining_steps: RemainingSteps


# ── Nodes ─────────────────────────────────────────────────────────────────────


def writer_node(state: PipelineState) -> dict:
    attempt = state.get("attempt_count", 0)
    code = call_writer_llm(
        task=state["task"],
        attempt=attempt,
        review_notes=state.get("review_notes"),
        test_results=state.get("test_results"),
    )
    print(f"  [writer] attempt {attempt} → {code.splitlines()[0]}")
    return {"code": code, "attempt_count": attempt + 1}


def reviewer_node(
    state: PipelineState,
) -> Command[Literal["tester_node", "writer_node"]]:
    notes = call_reviewer_llm(state["task"], state["code"])
    print(f"  [reviewer] approved={notes['approved']} — {notes['feedback']}")
    destination = "tester_node" if notes["approved"] else "writer_node"
    return Command(goto=destination, update={"review_notes": notes})


def tester_node(state: PipelineState) -> dict:
    writer = get_stream_writer()
    writer({"status": "running test suite", "attempt": state["attempt_count"]})
    results = run_tests(state["code"])
    label = "PASS ✓" if results["passed"] else f"FAIL — {results['errors']}"
    print(f"  [tester] {label}")
    writer({"status": "test suite complete", "passed": results["passed"]})
    return {"test_results": results}


def route_after_test(
    state: PipelineState,
) -> Literal["human_review_node", "writer_node", "__end__"]:
    if state["test_results"]["passed"]:
        return "human_review_node"
    if state.get("remaining_steps", 1) <= 2:
        print("  [router] remaining_steps exhausted — exiting")
        return "__end__"
    return "writer_node"


def human_review_node(
    state: PipelineState,
) -> Command[Literal["merge_node", "writer_node"]]:
    decision = interrupt(
        {
            "task": state["task"],
            "code": state["code"],
            "test_results": state["test_results"],
            "question": "Approve this code for merge?",
        }
    )
    print(f"  [human] decision: {decision!r}")
    if decision == "approve":
        return Command(goto="merge_node", update={"human_decision": "approve"})
    return Command(
        goto="writer_node",
        update={
            "human_decision": decision,
            "review_notes": {
                "approved": False,
                "feedback": f"Human rejected: {decision}",
            },
        },
    )


def merge_node(state: PipelineState) -> dict:
    do_merge(state["code"])
    return {}


# ── Graph assembly ────────────────────────────────────────────────────────────

final_builder = StateGraph(PipelineState)
final_builder.add_node("writer_node", writer_node)
final_builder.add_node("reviewer_node", reviewer_node)
final_builder.add_node("tester_node", tester_node)
final_builder.add_node("human_review_node", human_review_node)
final_builder.add_node("merge_node", merge_node)

final_builder.add_edge(START, "writer_node")
final_builder.add_edge("writer_node", "reviewer_node")
final_builder.add_conditional_edges(
    "tester_node",
    route_after_test,
    {
        "human_review_node": "human_review_node",
        "writer_node": "writer_node",
        "__end__": END,
    },
)
final_builder.add_edge("merge_node", END)
