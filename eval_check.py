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
		print("Extra files check: ✅ No extra files")



def check_readme(files: list[Path]):
	pass



def check_make(files: list[Path]):
	required_rules = {"all", "clean", "fclean", "re", ".PHONY"}
	found_rules = set()
	make = None

	print("Makefile check:")
	for file in files:
		if file.name == "Makefile" or file.name == "Make":
			make = file
			break

	if make == None:
		print("\t❌ No Makefile in this project")
		return 
	else:
		print("\t✅ Found Makefile")

	with open(make, 'r') as f:
		for line in f:
			line = line.strip()
			if ".PHONY" in line:
				found_rules.add(".PHONY")
				# add phony checks
			elif ':' in line:
				rule = line.split(':')[0].strip()
				if rule in required_rules:
					found_rules.add(rule)

	if found_rules == required_rules:
		print("\t✅ Found all rules")
	else:
		missing = required_rules - found_rules
		print("\t❌ Missing rules: ", end='')
		for rule in missing:
			print(rule, end=' ')
		print()

	result = subprocess.run(["make", "all"], cwd=make.parent, capture_output=True)

	if result.returncode == 0:
		print("\t✅ No compilation errors")
	else:
		print("\t❌ Found compilation errors")

	result = subprocess.run(["make", "fclean"], cwd=make.parent)
	

def run_checks(path: Path, files: list[Path]):
	check_norm(path)
	check_extra_files(files)
	check_make(files)
	check_readme(files)


def main():
	path = get_path()
	print("Path: ", path)
	files = []
	get_files(path, files)
	run_checks(path, files)

if __name__ == "__main__":
	main()