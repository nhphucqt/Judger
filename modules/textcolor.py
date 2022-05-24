# Reference: https://stackabuse.com/how-to-print-colored-text-in-python/

# Text styles:
# 0 : normal     | n
# 1 : bold       | b
# 2 : light      | l
# 3 : italicized | i
# 4 : underlined | u
# 5 : blink      | k

styles_code = {
    "n": {
        "id": 0,
        "name": "normal"
    },
    "b": {
        "id": 1,
        "name": "bold"
    },
    "l": {
        "id": 2,
        "name": "light"
    },
    "i": {
        "id": 3,
        "name": "italicized"
    },
    "u": {
        "id": 4,
        "name": "underlined"
    },
    "k": {
        "id": 5,
        "name": "blink"
    }
}

def style(text, _style):
    return f"\033[{_style}m{text}\033[0;0m"

def normal(text):
    return style(text, 0)

def bold(text):
    return style(text, 1)

def light(text):
    return style(text, 2)

def italic(text):
    return style(text, 3)

def underl(text):
    return style(text, 4)

def blink(text):
    return style(text, 5)

def fore(text, color):
    return f"\033[38;5;{color}m{text}\033[0;0m"

def back(text, color):
    return f"\033[48;5;{color}m{text}\033[0;0m"

def foreback(text, fore_color, back_color):
    return f"\033[48;5;{back_color}m\033[38;5;{fore_color}m{text}\033[0;0m"

def trans(text, fr = -1, bk = -1, st = ""):
    if fr != -1:
        text = fore(text, fr)
    if bk != -1:
        text = back(text, bk)
    for s in st:
        if s in styles_code:
            text = style(text, styles_code[s]["id"])
    return text

def list():
    for color in range(0, 256):
        num = str(color).ljust(4, ' ')
        print(fore(num, color), end='')
        if (color % 16 == 15): print()
    print()
    for color in range(0, 256):
        num = str(color).ljust(4, ' ')
        print(back(num, color), end='')
        if (color % 16 == 15): print()
    print()
    for color in range(0, 256):
        num = str(color).ljust(4, ' ')
        print(foreback(num, color, color), end='')
        if (color % 16 == 15): print()

if __name__ == "__main__":
    list()