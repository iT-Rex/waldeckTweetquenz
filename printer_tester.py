import sys

from printer import Printer


def main(*words):
    message = " ".join(words)
    if not message:
        message = "Hello world"
    printer = Printer()
    printer.print(message)
    printer.separator()


if __name__ == "__main__":
    main(*sys.argv[1:])
