from pathlib import Path
import re
import subprocess
from evalcheck42.output_utils import ok, fail, info


def check_norm(path: Path):
	try:
		result = subprocess.run(["norminette", str(path)], capture_output=True, text=True)
	except FileNotFoundError:
		fail("Norminette isn't installed on this machine.")
		return

	output = (result.stdout or "") + (result.stderr or "")

	if result.returncode == 0:
		ok("No norm errors found")
	else:
		if "Error" in output:
			fail("Found norm errors")
		if "Global" in output:
			info("Global variable detected")


def check_extra_files(files: list[Path]):
	hidden = set()
	extra_extensions = set()
	extra_files = set()
	extensions = {".h", ".c", ".cpp", ".md"}
	allowed_files = {"makefile", "readme.md", "license", ".gitignore"}

	for file in files:
		if file.name.startswith('.') and file.name != ".gitignore":
			hidden.add(file.name)
		elif file.suffix and file.suffix not in extensions:
			extra_extensions.add(file.suffix)
		elif file.suffix == "" and file.name.lower() not in allowed_files:
			extra_files.add(file.name)

	if hidden or extra_extensions or extra_files:
		if hidden:
			fail("Hidden files: " + " ".join(hidden))
		if extra_extensions:
			info("Extra extensions: " + " ".join(extra_extensions))
		if extra_files:
			fail("Extra files: " + " ".join(extra_files))
	else:
		ok("No extra files")


def check_readme(files: list[Path]):
	readme = None
	required_sections = {"description", "instructions", "resources"}
	found_sections = set()
	pattern = r"^([*_])this project has been created as part of the 42 curriculum by .+\1$"

	for file in files:
		if file.name == "README.md":
			readme = file
			break

	if readme is None:
		fail("README.md not found")
		return
	else:
		ok("Found README.md")

	try:
		with open(readme, 'r') as f:
			lines = f.readlines()
	except PermissionError:
		fail("Can't read file: Permission denied")
		return
	
	if not lines:
		fail("Empty readme")
		return

	first_line = lines[0].strip()

	if re.match(pattern, first_line, re.IGNORECASE):
		ok("First line format OK")
	else:
		fail("First line format invalid")

	for line in lines:
		if line.lstrip().startswith("#"):
			l = line.lstrip('#').strip().lower()
			if "description" in l:
				found_sections.add("description")
			elif "instructions" in l:
				found_sections.add("instructions")
			elif "resources" in l:
				found_sections.add("resources")

	missing = required_sections - found_sections
	if len(missing):
		fail("Missing sections: " + " ".join(missing))
	else:
		ok("Found all sections")


def check_make(files: list[Path]):
	required_rules = {"all", "clean", "fclean", "re", ".PHONY"}
	found_rules = set()
	make = None

	for file in files:
		if file.name == "Makefile":
			make = file
			break

	if make is None:
		fail("Makefile not found")
		return
	else:
		ok("Found Makefile")
	
	try:
		with open(make, 'r') as f:
			lines = f.readlines()
	except PermissionError:
		fail("Can't read file: Permission denied")
		return
	
	for line in lines:
		line = line.strip()
		if not line.startswith('#'):
			if line.startswith(".PHONY"):
				found_rules.add(".PHONY")
			elif ':' in line and not any(op in line for op in (":=", "+=", "?=")):
				rule = line.split(':')[0].strip()
				if rule in required_rules:
					found_rules.add(rule)

	if found_rules == required_rules:
		ok("Found all rules")
	else:
		missing = required_rules - found_rules
		fail("Missing rules: " + " ".join(missing))

	result = subprocess.run(["make", "all"], cwd=make.parent, capture_output=True)

	if result.returncode == 0:
		ok("No compilation errors")
	else:
		fail("Found compilation errors")

	subprocess.run(["make", "fclean"], cwd=make.parent, capture_output=True)
