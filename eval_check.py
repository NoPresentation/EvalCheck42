import os
import sys
import subprocess
import re
from pathlib import Path

def get_path():
    if len(sys.argv) == 2:
        return Path(sys.argv[1]).resolve()
    else:
        return Path.cwd()



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
	extensions = {".h", ".c", ".cpp", ".md"}
	print("Extra files check (allowed: .c, .cpp, .h, .md): ")
	for file in files:
		if file.name.startswith('.') and file.name != ".gitignore":
			extra_files.add(file.name)
		elif file.suffix and file.suffix not in extensions:
			extra_files.add(file.suffix)

	if len(extra_files) != 0:
		print("\t⚠️ Found extra files", end=" ")
		for suffix in extra_files:
			print(suffix, end=" ")
		print()
	else:
		print("✅ No extra files")



def check_readme(files: list[Path]):
	readme = None
	required_sections = {"description", "instructions", "resources"}
	found_sections = set()
	pattern = r"^[*_]this project has been created as part of the 42 curriculum by .+[*_]$"

	print("README.md check:")
	for file in files:
		if file.name == "README.md":
			readme = file
			break
	if readme == None:
		print("\t❌README.md not found")
		return
	else:
		print("\t✅ Found README.md")

	with open(readme, 'r') as f:
		lines = f.readlines()
		if not lines:
			print("❌ Empty readme")
		first_line = lines[0].strip()
		if re.match(pattern, first_line, re.IGNORECASE):
			print("\t✅ First line format OK")
		else:
			print("\t❌ First line format invalid")
		for line in lines:
			if line.lstrip().startswith("#"):
				l = line.lower()
				if "description" in l:
					found_sections.add("description")
				elif "instructions" in l:
					found_sections.add("instructions")
				elif "resources" in l:
					found_sections.add("resources")
	missing = required_sections - found_sections
	if len(missing):
		print("\t❌ Missing sections: ", end='')
		for section in missing:
			print(f"{section}", end=' ')
		print()
	else:
		print("\t✅ Found all sections")




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
		print("\t❌ Makefile not found")
		return 
	else:
		print("\t✅ Found Makefile")

	with open(make, 'r') as f:
		for line in f:
			if not line.startswith('#'):
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