import markdown
from pathlib import Path
import frontmatter
import shutil
import argparse
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = SCRIPT_DIR / "template.html"

def generate_index(posts_data, output_folder, template):
    # sort posts by date
    sorted_posts = sorted(posts_data)

    # dynamically create urls
    list_items = []
    for date, title, url in sorted_posts:
        item = f'<li><a href="{url}">{title}</a> - {date}</li>'
        list_items.append(item)

    links_html = "<ul>\n" + "\n".join(list_items) + "\n</ul>"

    index_output = template.replace("{{title}}", "Home").replace("{{content}}", links_html)

    index_path = output_folder / "index.html"
    index_path.write_text(index_output, encoding="utf-8")
    print("Successfully generated index.html.")

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate a static site by converting markdown files to html files."
    )

    parser.add_argument("input", type=Path, help="Path to the input folder")
    parser.add_argument("output", type=Path, help="Path to the output folder")
    parser.add_argument("--clean", action="store_true", help="Clean output folder before creating new files")

    args = parser.parse_args()
    input_path = args.input
    output_path = args.output
    clean = args.clean

    if not input_path.exists():
        print(f"Error: The folder '{input_path}' does not exist.")
        sys.exit(1)

    return input_path, output_path, clean

def clean_output(output_folder):
    if output_folder.exists():
        shutil.rmtree(output_folder)


def load_template():
    if not TEMPLATE_PATH.exists():
        print(f"Error: Template file '{TEMPLATE_PATH}' does not exist.")
        sys.exit(1)

    return TEMPLATE_PATH.read_text(encoding="utf-8")


def get_post_field(post, field_name, file_path):
    try:
        return post[field_name]
    except KeyError:
        print(f"Error: Missing '{field_name}' frontmatter in '{file_path}'.")
        return None

def main():
    input_folder, output_folder, clean = parse_arguments()
    count = 0
    fail_count = 0
    posts_data = []

    if clean:
        clean_output(output_folder)

    # obtain template text
    template = load_template()

    for file_path in input_folder.rglob("*"):
        if file_path.is_dir():
            continue

        if file_path.is_file() and file_path.suffix == ".md":
            # obtain and split frontmatter
            try:
                post = frontmatter.load(file_path)
            except Exception as exc:
                print(f"Error: Could not parse '{file_path}': {exc}")
                fail_count += 1
                continue

            title = get_post_field(post, "title", file_path)
            date = get_post_field(post, "date", file_path)

            if title is None or date is None:
                fail_count += 1
                continue

            # convert markdown to html
            html_content = markdown.markdown(post.content)

            # inject content into template
            output = template.replace("{{title}}", str(title)).replace("{{content}}", html_content)

            # remove content folder from output
            clean_parts = file_path.relative_to(input_folder).parts

            # create output path dynamically with filename
            output_path = output_folder / Path(*clean_parts).with_suffix(".html")

            # create nested folders if they dont exist yet
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # write the file
            output_path.write_text(output, encoding="utf-8")

            # create url for index generation
            url = (f"/{output_path.relative_to(output_folder).as_posix()}")

            # store post data and url for index file later only if file should be listed
            if post.get("listed", True):
                posts_data.append((date, title, url))

        elif file_path.is_file():
            # remove content folder from output
            clean_parts = file_path.relative_to(input_folder).parts

            # create output path dynamically with filename
            output_path = output_folder / Path(*clean_parts)

            # create nested folders if they dont exist yet
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # copy file
            shutil.copy(file_path, output_path)

        count += 1

    print(f"Successfully converted {count} file(s).")
    if fail_count > 0:
        print(f"Failed to convert {fail_count} file(s).")
    generate_index(posts_data, output_folder, template)

if __name__ == "__main__":
    main()