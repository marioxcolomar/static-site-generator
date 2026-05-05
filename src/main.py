import os
import shutil
from os import listdir, makedirs, path
from pathlib import Path

from block_markdown import extract_title, markdown_to_html_node


def main():
    source_dir = Path("static")
    destination_dir = Path("public")
    copy_directory(source_dir, destination_dir)
    generate_pages_recursive(Path("content"), "template.html", Path("public"))


def copy_directory(source, destination):
    if not source.exists() or not source.is_dir():
        raise ValueError(f"source directory does not exists: {source}")
    # empty the destination directory before beginning
    if destination.exists():
        shutil.rmtree(destination)

    destination.mkdir(parents=True, exist_ok=True)

    def copy(curr_source, curr_destination):
        for item in curr_source.iterdir():
            target = curr_destination / item.name

            if item.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                copy(item, target)
            else:
                shutil.copy2(item, target)
                print(f"copied: {item} -> {target}")

    copy(source, destination)


def generate_page(from_path, template_path, destination_path):
    print(
        f"Generating page from {from_path} to {destination_path} using {template_path}"
    )
    destination = path.dirname(destination_path)
    if destination != "":
        makedirs(destination, exist_ok=True)
    with (
        open(from_path, "r") as from_file,
        open(template_path, "r") as template_file,
        open(destination_path, "w") as new_page,
    ):
        markdown = from_file.read()
        template = template_file.read()
        content = markdown_to_html_node(markdown).to_html()
        title = extract_title(markdown)
        template = template.replace("{{ Title }}", title)
        template = template.replace("{{ Content }}", content)
        new_page.write(template)


def generate_pages_recursive(dir_path, template_path, dest_path):
    for directory in listdir(dir_path):
        full_path = path.join(dir_path, directory)
        destination = path.join(dest_path, directory)
        if os.path.isfile(full_path):
            if directory.endswith(".md"):
                destination = destination.replace(".md", ".html")
                generate_page(full_path, template_path, destination)
        else:
            generate_pages_recursive(Path(full_path), template_path, Path(destination))


if __name__ == "__main__":
    main()
