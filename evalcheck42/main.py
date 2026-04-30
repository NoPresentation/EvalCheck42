from pathlib import Path
from evalcheck42.checks import check_norm, check_extra_files, check_make, check_readme
from evalcheck42.filesystem import get_files, get_path
from evalcheck42.output_utils import ok, fail, info

def run_checks(path: Path, files: list[Path]):
	if not files:
		fail("No files found in directory")
		return
	check_norm(path)
	check_readme(files)
	check_make(files)
	check_extra_files(files)


def main():
	path = get_path()
	files = []
	get_files(path, files)
	run_checks(path, files)


if __name__ == "__main__":
	main()