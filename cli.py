#!/usr/bin/env python3
"""
Code Snippet Translator CLI

Translate code snippets between Python, JavaScript, and Java
"""

import click
from translators import translate_snippet


@click.command()
@click.option(
    "--from-lang",
    type=click.Choice(["py", "js", "java"]),
    default="py",
    help="Source language",
)
@click.option(
    "--to-lang",
    type=click.Choice(["py", "js", "java"]),
    default="js",
    help="Target language",
)
@click.argument("path", type=click.Path(exists=True))
def cli(from_lang, to_lang, path):
    """Translate a code snippet from PATH"""
    try:
        with open(path, "r") as f:
            src = f.read()

        out = translate_snippet(src, from_lang, to_lang)
        print(out)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        return 1


if __name__ == "__main__":
    cli()
