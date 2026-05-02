# Evalcheck42

A command-line tool for checking 42 projects before evaluations to help avoid common errors and mistakes.

It performs automated checks for common submission requirements such as Norminette compliance, Makefile correctness, README structure, and unexpected files.

## What it checks

### Norminette

* Detects norm errors and warnings.

### README.md

* Ensures file exists
* Checks first-line format
* Validates required sections:
  * Description
  * Instructions
  * Resources

### Makefile

* Checks required rules:

  * `all`, `clean`, `fclean`, `re`, `.PHONY`
* Runs (`make all`) to check for any compilation errors
* Runs (`make fclean`) to check if it leaves any extra files

### Extra files

* Reports extra extensions, extra files, and hidden files

---

## Installation

### From pipx (recommended)

```bash
pipx install evalcheck42
```

or:

```bash
pip install evalcheck42
```

---

## Usage

You can run it in the current directory:
```bash
evalcheck
```
Or using a path:
```bash
evalcheck <path>
```
---


## Requirements

* Python 3.10+
* `norminette` installed and available in PATH
* `make` available in PATH
