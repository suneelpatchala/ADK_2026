import os
import re
import sys
from google.adk import Agent
from google.adk.models import LlmResponse
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from google.genai import types
from mcp import StdioServerParameters

# Import the arithmetic functions directly from our MCP server module
from server import add, multiply, subtract

# Path to the MCP server script
SERVER_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "server.py")
)

# 1. MCP Toolset: Exposes MCP tools to the agent via Standard I/O (stdio)
calculator_mcp_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=sys.executable,
            args=[SERVER_PATH],
        )
    )
)


def parse_math_operation(text: str):
    """Detects numbers and math keywords/symbols from user prompt."""
    text = text.strip()

    # Pattern 1: "add 10 and 20" or "multiply 5 and 6"
    m = re.search(
        r"\b(add|sum|multiply|times)\b\s+(\d+(?:\.\d+)?)\s+(?:and|by|,|\+)\s+(\d+(?:\.\d+)?)",
        text,
        re.I,
    )
    if m:
        op = m.group(1).lower()
        a, b = float(m.group(2)), float(m.group(3))
        tool = "multiply" if op in ("multiply", "times") else "add"
        return tool, a, b

    # Pattern 2: "subtract 4 from 10" -> 10 - 4
    m = re.search(
        r"\bsubtract\b\s+(\d+(?:\.\d+)?)\s+from\s+(\d+(?:\.\d+)?)", text, re.I
    )
    if m:
        return "subtract", float(m.group(2)), float(m.group(1))

    # Pattern 3: "subtract 10 and 4" -> 10 - 4
    m = re.search(
        r"\bsubtract\b\s+(\d+(?:\.\d+)?)\s+(?:and|by|,|-)\s+(\d+(?:\.\d+)?)",
        text,
        re.I,
    )
    if m:
        return "subtract", float(m.group(1)), float(m.group(2))

    # Pattern 4: Math symbols or operators: "15 + 27", "100 - 35", "6 * 7", "10 plus 5", "8 minus 3"
    m = re.search(
        r"(\d+(?:\.\d+)?)\s*([\+\-\*]|\bplus\b|\bminus\b|\btimes\b)\s*(\d+(?:\.\d+)?)",
        text,
        re.I,
    )
    if m:
        a = float(m.group(1))
        op = m.group(2).lower()
        b = float(m.group(3))
        if op in ("+", "plus"):
            return "add", a, b
        elif op in ("-", "minus"):
            return "subtract", a, b
        elif op in ("*", "times"):
            return "multiply", a, b

    return None


def intercept_math_before_model(
    callback_context, llm_request
) -> LlmResponse | None:
    """Pre-model callback: intercepts math requests before calling the LLM.

    If arithmetic symbols or math keywords are found with numbers, it directly invokes
    the MCP server tool and short-circuits the LLM call, saving latency and tokens.
    """
    if not llm_request.contents:
        return None

    # Extract text from the latest turn
    last_turn = llm_request.contents[-1]
    prompt_text = " ".join(
        part.text for part in (last_turn.parts or []) if part.text
    )

    parsed = parse_math_operation(prompt_text)
    if not parsed:
        # Not a direct math calculation -> proceed to Gemini model normally
        return None

    tool_name, a, b = parsed

    # Call the MCP server function
    if tool_name == "add":
        result = add(a, b)
        symbol = "+"
    elif tool_name == "subtract":
        result = subtract(a, b)
        symbol = "-"
    elif tool_name == "multiply":
        result = multiply(a, b)
        symbol = "*"
    else:
        return None

    # Returning an LlmResponse skips the model call entirely
    return LlmResponse(
        content=types.Content(
            role="model",
            parts=[
                types.Part(
                    text=f"[⚡ Intercepted before model by MCP Calculator Server]\nResult: {a} {symbol} {b} = {result}"
                )
            ],
        )
    )


# Root agent definition
root_agent = Agent(
    model="gemini-3.5-flash",
    name="mcp_calculator_agent",
    description="Agent with MCP calculator tools and pre-model math interception.",
    instruction=(
        "You are a helpful assistant equipped with an MCP calculator server. "
        "Use the calculator tools whenever mathematical computations are needed."
    ),
    tools=[calculator_mcp_toolset],
    before_model_callback=intercept_math_before_model,
)
