#!/usr/bin/python3

import os
import urwid
import shlex
import argparse
import platform
import subprocess


def shlex_split(string: str, delimeter="->"):
    lex = shlex.shlex(string.strip(), posix=True)
    lex.whitespace = delimeter
    lex.whitespace_split = True
    return list(lex)


def open_with_default_app(url: str):
    if platform.system() == "windows":
        os.startfile(url)
    else:
        subprocess.Popen(
            ["open", url], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL
        )


def parse(file: str):
    paths = {"/": {}}

    with open(file, "r") as file:
        for line in file:
            path, url = shlex_split(line)
            path, url = path.strip(), url.strip()
            curr = paths["/"]
            tokens = path.split("/")

            for i, token in enumerate(tokens):
                if token == "" or token.isspace():
                    continue

                if i == len(tokens) - 1:
                    curr[token] = url
                else:
                    curr = curr.setdefault(token, {})

    return paths


def get_args():
    parser = argparse.ArgumentParser(
        prog="CLI Bookmarker",
        description="A command-line tool to read and store bookmarks from a simple .txt file. "
        "Each line in the file should contain a path and a URL separated by '->'.",
    )

    parser.add_argument(
        "-f",
        "--filename",
        required=True,
        help="The path to the .txt file containing the bookmarks. Each line in the file should "
        "be formatted as 'path -> URL'.",
    )

    return parser.parse_args()


class History:
    __paths: list[dict[str, dict | str]]

    def __init__(self, paths: list[dict[str, dict | str]]):
        self.__paths = paths

    def go_back(self):
        if len(self.__paths) == 1:
            return

        self.__paths.pop()

    def push(self, path: dict[str, dict | str]):
        self.__paths.append(path)

    def get_current(self):
        return self.__paths[-1]


def get_contents(
    btn: urwid.Button,
    data: tuple[History, dict[str, dict | str], urwid.SimpleListWalker, urwid.MainLoop],
):
    history, path, list_walker, loop = data
    history.push(path)
    generate_buttons(path, loop, list_walker, history)


def generate_buttons(
    path: dict[str, dict],
    loop: urwid.MainLoop,
    list_walker: urwid.SimpleListWalker,
    history: History,
):
    buttons: list[urwid.Button] = []

    for key in path:
        is_dir = isinstance(path[key], dict)

        if is_dir:
            btn = urwid.Button(
                f"📁 {key}", get_contents, (history, path[key], list_walker, loop)
            )
        else:
            btn = urwid.Button(
                f"🌐 {key}", lambda _, url=path[key]: open_with_default_app(url)
            )

        styled_btn = urwid.AttrMap(btn, "normal", focus_map="reversed")
        buttons.append(styled_btn)

    list_walker[:] = buttons
    loop.draw_screen()


def on_start(
    loop: urwid.MainLoop, data: tuple[History, dict[str, dict], urwid.ListWalker]
):
    history, path, list_walker = data
    generate_buttons(path, loop, list_walker, history)


def handle_keypress(
    key: str,
    loop: urwid.MainLoop,
    list_walker: urwid.SimpleListWalker,
    history: History,
):
    if key == "esc":
        history.go_back()
        generate_buttons(history.get_current(), loop, list_walker, history)


def main():
    args = get_args()
    paths = parse(args.filename)

    palette = [
        ("reversed", "standout", "default"),
        ("button normal", "default", "default"),
        ("button select", "white", "default"),
    ]

    history = History([paths["/"]])

    footer_text = urwid.Text("SPACE - Select item     ESC - Go back")
    list_walker = urwid.SimpleListWalker([])
    list_box = urwid.ListBox(list_walker)
    frame = urwid.Frame(list_box, footer=footer_text)
    loop = urwid.MainLoop(
        frame,
        palette=palette,
        unhandled_input=lambda key: handle_keypress(key, loop, list_walker, history),
    )

    loop.set_alarm_in(0, on_start, (history, history.get_current(), list_walker))
    loop.run()


if __name__ == "__main__":
    main()
