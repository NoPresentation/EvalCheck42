import os
import sys
import subprocess
from pathlib import Path

def get_path():
	if len(sys.argv) != 2:
		print("evalcheck <path>")
		sys.exit(1)
	return Path(os.path.abspath(sys.argv[1])) # gets the absolute path, handles the .


def get_files(path: Path, files: list):
	try:
		for item in path.iterdir():
			if item.is_dir():
				get_files(item, files)
			else:
				files.append(item)
	except PermissionError as e:
		print(f"Permission denied: {e}")


def check_norm(path: Path):
	try:
		result = subprocess.run(["norminette", str(path)], capture_output=True)
	except FileNotFoundError:
		print("Norminette isn't installed on this machine. Abort.")
		sys.exit(1)
	if result.returncode == 0:
		print("Norminette check: ✅")
	else:
		print("Norminette check: ❌")


def check_extra_files(files: list[Path]):
	extra_files = set()

	for file in files:
		if file.suffix != ".h" and file.suffix != ".c":
			extra_files.add(file.suffix)

	if len(extra_files) != 0:
		print("Extra files check:\n\t⚠️ Found files other than .c and .h:", end=" ")
		for suffix in extra_files:
			print(suffix, end=" ")
		print()
	else:
		print("Extra files check: ✅")


def check_readme(files: list[Path]):
	pass

def check_make(files: list[Path]):
	pass

def run_checks(path: Path, files: list[Path]):
	check_norm(path)
	check_extra_files(files)
	check_readme(files)
	check_make(files)



def main():
	path = get_path()
	print("Path: ", path)
	files = []
	get_files(path, files)
	run_checks(path, files)

if __name__ == "__main__":
	main()