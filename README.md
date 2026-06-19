# Static Site Generator

A small Python static site generator that converts Markdown files in a given input folder into HTML pages using `template.html` and copies any non-Markdown assets into the output folder.

## Overview

The generator walks the given input directory, turns each `.md` file into an `.html` file, and preserves the rest of the folder structure. It also builds an `index.html` page from the generated posts.

Each Markdown file should include frontmatter with at least:

* `title`
* `date`

Files missing either field are skipped with an error message.

## Requirements

* Python 3.10 or newer
* The packages listed in `requirements.txt`

Install dependencies with:

```powershell
pip install -r requirements.txt
```

## Project Structure

* `ssg.py` - generator entry point
* `template.html` - HTML template used for generated pages
* `content/` - example input folder and static assets
* `content/posts/` - example blog posts
* `content/style.css` - stylesheet copied to the output folder

## Usage

Run the generator from the project root:

```powershell
python ssg.py content dist --clean
```

Arguments:

* `input` - source content folder
* `output` - destination folder for generated files
* `--clean` - remove the output folder before generating new files

Example output from the command above will be written to `dist/`.

## Content Format

Markdown files use YAML frontmatter at the top of the file. Example:

```markdown
---
title: Getting Started With Python Automation
date: 2024-01-15
---

# Getting Started

Your Markdown content goes here.
```

The `title` is used for the page title and the `date` is included in the generated index.

## Template Notes

The template must include these placeholders:

* `{{title}}`
* `{{content}}`

`ssg.py` reads `template.html` relative to the script location, so the generator can be run from any working directory as long as the project files stay together.

## License

See [LICENSE](LICENSE) for details.