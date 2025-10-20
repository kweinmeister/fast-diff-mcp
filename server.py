import asyncio
import logging
import os
from typing import List, Iterator

from fast_diff_mcp import unified_diff
from fastmcp import FastMCP
import difflib

logger: logging.Logger = logging.getLogger(__name__)
mcp: FastMCP = FastMCP("fast-diff-mcp")


@mcp.tool()
def diff_tool_rust_similar(original_text: str, modified_text: str) -> str:
    """
    Compares two multiline strings and returns the difference in the
    standard unified diff format. This is a high-performance implementation
    written in Rust, using the `similar` crate's Myers diff algorithm.
    """
    logger.info(">>> Tool: 'diff_tool_rust_similar' called")
    return unified_diff(original_text, modified_text)


@mcp.tool()
def diff_tool_python_difflib(original_text: str, modified_text: str) -> str:
    """
    Compares two multiline strings using the standard Python `difflib`
    library, which uses the Ratcliff/Obershelp algorithm.
    """
    logger.info(">>> Tool: 'diff_tool_python_difflib' called")
    original_lines: List[str] = original_text.splitlines(keepends=True)
    modified_lines: List[str] = modified_text.splitlines(keepends=True)
    diff: Iterator[str] = difflib.unified_diff(
        original_lines, modified_lines, "original", "modified"
    )
    return "".join(diff)


if __name__ == "__main__":
    logger.info(f" MCP server started on port {os.getenv('PORT', 8080)}")
    logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)
    asyncio.run(
        mcp.run_async(
            transport="streamable-http",
            host="0.0.0.0",
            port=int(os.getenv("PORT", 8080)),
        )
    )
