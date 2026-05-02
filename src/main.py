import shutil
from pathlib import Path


def main():
    source_dir = Path("static")
    destination_dir = Path("public")
    copy_directory(source_dir, destination_dir)


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


if __name__ == "__main__":
    main()
