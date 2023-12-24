class style:
    BOLD_START = "\033[1m"
    RESET = "\033[0m"


class colors:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    UNDERLINE = "\033[4m"


def bold(text: str, restore_to: str = ""):
    return style.BOLD_START + str(text) + style.RESET + restore_to


def color(text: str, color: str):
    return color + str(text) + style.RESET
