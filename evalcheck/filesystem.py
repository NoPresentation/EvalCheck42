from pathlib import Path
import sys  


def get_path():
	if len(sys.argv) == 2:
		return Path(sys.argv[1]).resolve()
	else:
		return Path.cwd()


def get_files(path: Path, files: list):
	try:
		for item in path.iterdir():
			if item.is_dir():
				if not item.name.startswith('.'):
					get_files(item, files)
			else:
				files.append(item)
	except PermissionError as e:
		print(f"Permission denied: {e}")
		sys.exit(1)
