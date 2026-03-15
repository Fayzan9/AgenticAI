
from pathlib import Path
from typing import List, Optional
from .models.response import ExplorerFileItem
import shutil


def list_directory(base_path: Path, rel_path: Optional[str] = None) -> List[ExplorerFileItem]:
	path = base_path if rel_path is None else base_path / rel_path
	if not path.exists() or not path.is_dir():
		return []
	def _get_items(p: Path, base: Path) -> List[ExplorerFileItem]:
		items = []
		for entry in p.iterdir():
			if entry.name == "__pycache__":
				continue
			item = ExplorerFileItem(
				name=entry.name,
				path=str(entry.relative_to(base)),
				type="directory" if entry.is_dir() else "file",
				children=_get_items(entry, base) if entry.is_dir() else None
			)
			items.append(item)
		return sorted(items, key=lambda x: (x.type != "directory", x.name))
	return _get_items(path, path)

def get_file_content(base_path: Path, rel_path: str) -> Optional[str]:
	file_path = base_path / rel_path
	if not file_path.exists() or not file_path.is_file():
		return None
	return file_path.read_text()

def agent_list_files(agent_path: Path) -> list:
	if not agent_path.exists() or not agent_path.is_dir():
		return []
	def get_files(path):
		items = []
		for p in path.iterdir():
			if p.name == "__pycache__":
				continue
			item = {"name": p.name, "path": str(p.relative_to(agent_path))}
			if p.is_dir():
				item["type"] = "directory"
				item["children"] = get_files(p)
			else:
				item["type"] = "file"
			items.append(item)
		return sorted(items, key=lambda x: (x["type"] != "directory", x["name"]))
	return get_files(agent_path)

def agent_get_file_content(agent_path: Path, file_path: str) -> dict:
	full_path = agent_path / file_path
	if not full_path.exists() or not full_path.is_file():
		return {"error": "File not found"}
	return {"content": full_path.read_text()}

def agent_create_file_or_directory(agent_path: Path, rel_path: str, type_: str) -> dict:
	full_path = agent_path / rel_path
	if full_path.exists():
		return {"error": "Path already exists"}
	if type_ == "directory":
		full_path.mkdir(parents=True, exist_ok=True)
	else:
		full_path.parent.mkdir(parents=True, exist_ok=True)
		full_path.touch()
	return {"status": "ok"}

def agent_save_file_content(agent_path: Path, file_path: str, content: str) -> dict:
	full_path = agent_path / file_path
	if not full_path.exists() or not full_path.is_file():
		return {"error": "File not found"}
	full_path.write_text(content)
	return {"status": "ok"}

def agent_rename_file_or_directory(agent_path: Path, old_path: str, new_path: str) -> dict:
	old_full_path = agent_path / old_path
	new_full_path = agent_path / new_path
	if not old_full_path.exists():
		return {"error": "Source path not found"}
	if new_full_path.exists():
		return {"error": "Destination path already exists"}
	old_full_path.rename(new_full_path)
	return {"status": "ok"}

def agent_delete_file_or_directory(agent_path: Path, rel_path: str) -> dict:
	full_path = agent_path / rel_path
	if not full_path.exists():
		return {"error": "Path not found"}
	if full_path.is_dir():
		shutil.rmtree(full_path)
	else:
		full_path.unlink()
	return {"status": "ok"}
