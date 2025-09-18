import subprocess
import os
import json
import sys
from pathlib import Path
from argparse import ArgumentParser


def main():
    parser = ArgumentParser(
        description="Fetch pull requests from Github for repository in the current working directory.",
    )
    parser.add_argument(
        "--dest",
        default="pull-requests",
        help="destination directory name"
    )

    args = parser.parse_args()

    prs = _get_prs()

    for pr in prs:
        pr_url = pr.get("url")
        desc = _get_pr_description(pr_url)
        diff = _get_pr_diff(pr_url)
        title = pr.get("title")
        item_to_save = desc + "\n" + diff

        _save_to_file(item_to_save, args.dest, title)


def _fetch_from_gh(command):
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error when fetching from Github: {e}")
        return sys.exit(1)


def _get_prs():
    return json.loads(_fetch_from_gh(["gh", "pr", "list", "--json", "url", "--json", "title"]))


def _get_pr_description(pr_handle):
    return _fetch_from_gh(["gh", "pr", "view", pr_handle, "--comments"])


def _get_pr_diff(pr_handle):
    return _fetch_from_gh(["gh", "pr", "diff", pr_handle])


def _save_to_file(content, directory, filename):
    try:
        dest_dir = Path(directory)
        dest_dir.mkdir(parents=True, exist_ok=True)

        safe_filename = "".join(c for c in filename.strip(
        ) if c.isalnum() or c in (' ', '-', '_'))

        file_path = dest_dir / f"{safe_filename}.md"

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"Saved file {file_path}")
        return file_path

    except PermissionError:
        print(f"Error: Permission denied for directory {directory}")
        return sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}")
        return sys.exit(1)


if __name__ == "__main__":
    main()
