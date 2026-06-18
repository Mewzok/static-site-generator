import markdown
from pathlib import Path
import frontmatter

input_folder = Path("content")
output_folder = Path("site")

# obtain template text
template = Path("template.html").read_text(encoding="utf-8")

for file_path in input_folder.rglob("*.md"):
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

    print(f"Generated: {output_path}")

# file_path = "content/index.md"
# output_folder = Path("site")
# output_path = output_folder / "index.html"

# # obtain both the frontmatter and split it out to obtain content
# post = frontmatter.load(file_path)
# title = str(post['title'])

# # convert content into html
# template = Path("template.html").read_text()

# # inject content into template
# output = template.replace("{{title}}", title).replace("{{content}}", post.content)

# # convert markdown into html
# html = markdown.markdown(output)

# # create output folder if doesnt exist
# output_folder.mkdir(parents=True, exist_ok=True)

# output_path.write_text(html, encoding="utf-8")