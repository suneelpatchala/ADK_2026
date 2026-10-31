from mcp.server.fastmcp import FastMCP

# Initialize the MCP Server
mcp = FastMCP("calculator-server")


@mcp.tool()
def add(a: float, b: float) -> float:
    """Adds two numbers (a + b).

    Args:
        a: First number.
        b: Second number.
    """
    return a + b


@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtracts the second number from the first number (a - b).

    Args:
        a: First number.
        b: Second number.
    """
    return a - b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers (a * b).

    Args:
        a: First number.
        b: Second number.
    """
    return a * b


if __name__ == "__main__":
    # Runs the MCP server communicating via Standard Input/Output (stdio)
    mcp.run(transport="stdio")
