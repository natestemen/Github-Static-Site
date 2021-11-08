"""
Generate a file tree table of contents for a directory of pdf files

run from command line:

    $ python generate_index.py pdf_index.md

will generate a  markdown index of all pdf files in the current working
directory and its sub folders and insert it into  a file `pdf_index.md`.
If a previous index exists in the file it will be replaced,
otherwise a new index will be created at the end of the file
or a new file created.

The index will be linked to the files
eg.
`  - [how_to_take_notes.pdf](./notetaking/how_to_take_notes.pdf)`
for a link to a file `how_to_take_notes.pdf` in the sub-folder `notetaking`

original author: elfnor <elfnor.com> (https://gist.github.com/elfnor/bc2176b3fad8581c678b771afb1e3b3e)
modified by: natestemen <github.com/natestemen>
"""
import os
import argparse


def create_index(cwd):
    """create markdown index of all pdf files in cwd and sub folders"""
    base_len = len(cwd)
    base_level = cwd.count(os.sep)
    md_lines = ["<!-- filetree -->\n\n"]
    for dirname, _, files in os.walk(cwd):
        files = sorted(
            [f for f in files if not f[0] == "." and f.lower().endswith(".pdf")]
        )
        if files:
            level = dirname.count(os.sep) - base_level
            indent = "  " * level
            if dirname != cwd:
                indent = "  " * (level - 1)
                md_lines.append(f"{indent} - **{os.path.basename(dirname)}/**\n")
            rel_dir = ".{1}{0}".format(os.sep, dirname[base_len:])
            for pdf in files:
                indent = "  " * level
                md_lines.append(f"{indent} - [{pdf}]({rel_dir}{pdf})\n")

    md_lines.append("\n<!-- filetreestop -->\n")
    return md_lines


def replace_index(filename, new_index):
    """finds the old index in filename and replaces it with the lines in new_index
    if no existing index places new index at end of file
    if file doesn't exist creates it and adds new index
    """

    pre_index = []
    post_index = []
    pre = True
    post = False
    try:
        with open(filename, "r") as md_in:
            for line in md_in:
                if "<!-- filetree" in line:
                    pre = False
                if "<!-- filetreestop" in line:
                    post = True
                if pre:
                    pre_index.append(line)
                if post:
                    post_index.append(line)
    except FileNotFoundError:
        pass

    with open(filename, "w") as md_out:
        md_out.writelines(pre_index)
        md_out.writelines(new_index)
        md_out.writelines(post_index[1:])


def main():
    """generate index optional cmd line arguments"""
    parser = argparse.ArgumentParser(
        description=(
            "generate a markdown index tree of pdf files"
            "in current working directory and its sub folders"
        )
    )

    parser.add_argument(
        "filename", nargs="?", default="README.md", help="markdown output file"
    )

    args = parser.parse_args()

    cwd = os.getcwd()
    md_lines = create_index(cwd)

    md_out_fn = os.path.join(cwd, args.filename)
    replace_index(md_out_fn, md_lines)


if __name__ == "__main__":
    main()
