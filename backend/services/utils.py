from pathlib import Path
from typing import Optional, Dict


def calculate_cost(usage: dict) -> dict:
    """
    Calculate cost based on token usage and current model pricing.
    
    Args:
        usage: Dictionary containing input_tokens, cached_input_tokens, and output_tokens
    
    Returns:
        Dictionary with detailed token counts and costs
    """
    from config import ACTIVE_MODEL, PRICES

    prices = PRICES[ACTIVE_MODEL]

    input_tokens = usage.get("input_tokens", 0)
    cached_tokens = usage.get("cached_input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0)

    input_cost = (input_tokens / 1_000_000) * prices["input_tokens"]
    cached_cost = (cached_tokens / 1_000_000) * prices["cached_input_tokens"]
    output_cost = (output_tokens / 1_000_000) * prices["output_tokens"]

    total_tokens = input_tokens + cached_tokens + output_tokens
    total_cost = input_cost + cached_cost + output_cost

    return {
        "model": ACTIVE_MODEL,
        "input_tokens": input_tokens,
        "cached_tokens": cached_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "input_cost": round(input_cost, 6),
        "cached_cost": round(cached_cost, 6),
        "output_cost": round(output_cost, 6),
        "total_cost": round(total_cost, 6),
    }


def insert_user_request(markdown_path: str, user_request: str, execution_id: Optional[str] = None, write_back: bool = False) -> str:
    """
    Reads a markdown file and inserts the user request at the {users request} placeholder
    and optionally replaces {execution_id} placeholder.

    Args:
        markdown_path (str): Path to the markdown file
        user_request (str): The user's request to insert
        execution_id (Optional[str]): The execution ID to insert (if placeholder exists)
        write_back (bool): If True, overwrite the file with updated content

    Returns:
        str: Updated markdown content
    """

    path = Path(markdown_path)

    if not path.exists():
        raise FileNotFoundError(f"Markdown file not found: {markdown_path}")

    content = path.read_text(encoding="utf-8")

    placeholder = "{users request}"

    if placeholder not in content:
        raise ValueError("Placeholder '{users request}' not found in markdown file")

    updated_content = content.replace(placeholder, user_request)
    
    # Replace execution_id placeholder if provided
    if execution_id:
        execution_id_placeholder = "{execution_id}"
        if execution_id_placeholder in updated_content:
            updated_content = updated_content.replace(execution_id_placeholder, execution_id)

    if write_back:
        path.write_text(updated_content, encoding="utf-8")

    return updated_content