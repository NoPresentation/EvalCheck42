from pathlib import Path
from evalcheck42.checks import check_norm, check_extra_files, check_make, check_readme
from evalcheck42.filesystem import get_files, get_path
from evalcheck42.output_utils import ok, fail, info

def run_checks():
	path = get_path()
	files = []
	get_files(path, files)
	if not files:
		fail("No files found in directory")
		return
	print("Norminette check:")
	check_norm(path)

	print("README.md check:")
	check_readme(files)

	print("Extra files check (allowed: .c, .cpp, .h, .md):")
	check_extra_files(files)
	
	print("Makefile check:")
	check_make(files)

	files_after = []
	get_files(path, files_after)

	print("Clean up check(after fclean):")
	check_extra_files(files_after)

def main():
	run_checks()


if __name__ == "__main__":
	main()