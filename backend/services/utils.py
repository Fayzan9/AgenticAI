from pathlib import Path
from typing import Optional


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