import markdown
from pathlib import Path
import frontmatter
import shutil

input_folder = Path("content")
output_folder = Path("site")
count = 0

# obtain template text
template = Path("template.html").read_text(encoding="utf-8")

for file_path in input_folder.rglob("*"):
    if file_path.is_dir():
        continue

    if file_path.is_file() and file_path.suffix == ".md":
        # obtain and split frontmatter
        post = frontmatter.load(file_path)

        # convert markdown to html
        html_content = markdown.markdown(post.content)

        # inject content into template
        output = template.replace("{{title}}", str(post['title'])).replace("{{content}}", html_content)

        # remove content folder from output
        clean_parts = file_path.parts[1:]

        # create output path dynamically with filename
        output_path = output_folder / Path(*clean_parts).with_suffix(".html")

        # create nested folders if they dont exist yet
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # write the file
        output_path.write_text(output, encoding="utf-8")

        count += 1
    elif file_path.is_file():
        # remove content folder from output
        clean_parts = file_path.parts[1:]

        # create output path dynamically with filename
        output_path = output_folder / Path(*clean_parts)

        # create nested folders if they dont exist yet
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # copy file
        shutil.copy(file_path, output_path)

        count += 1

print(f"Successfully created {count} files.")