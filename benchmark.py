import logging
import random

import pyperf
from faker import Faker
from fastmcp import Client

from server import mcp


def generate_test_texts() -> tuple[str, str]:
    """Generate a pair of texts for benchmarking."""
    fake = Faker()
    text_a = fake.text(max_nb_chars=10000000)
    words = text_a.split()

    if not words:
        return text_a, text_a

    word_to_replace = random.choice(words)
    replacement_word = fake.word()
    while replacement_word == word_to_replace:
        replacement_word = fake.word()

    text_b = text_a.replace(word_to_replace, replacement_word, 1)
    return text_a, text_b


async def run_bench(tool_name: str, text_a: str, text_b: str) -> None:
    """Asynchronous benchmark function."""

    async with Client(mcp) as client:
        await client.call_tool(
            tool_name,
            {"original_text": text_a, "modified_text": text_b},
        )


def main() -> None:
    """Sets up and runs the benchmarks."""
    logging.basicConfig(level=logging.WARNING)

    text_a, text_b = generate_test_texts()

    runner = pyperf.Runner()

    runner.bench_async_func(
        "Rust (`similar` crate)",
        run_bench,
        "diff_tool_rust_similar",
        text_a,
        text_b,
    )
    runner.bench_async_func(
        "Python (`difflib` stdlib)",
        run_bench,
        "diff_tool_python_difflib",
        text_a,
        text_b,
    )


if __name__ == "__main__":
    main()
