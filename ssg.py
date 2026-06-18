import markdown
from pathlib import Path
import frontmatter

# main filepath
file_path = "content/index.md"

# obtain both the frontmatter and split it out to obtain content
post = frontmatter.load(file_path)
title = str(post['title'])
print(title)

# convert content into html
template = Path("template.html").read_text()

output = template.replace("{{title}}", title).replace("{{content}}", post.content)

html = markdown.markdown(output)

print(html)