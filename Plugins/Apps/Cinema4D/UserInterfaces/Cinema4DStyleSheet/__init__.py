import os


def load_stylesheet():
    sFile = os.path.dirname(__file__) + "/Cinema4D.qss"
    if not os.path.exists(sFile):
        return ""

    with open(sFile, "r") as f:
        stylesheet = f.read()

    ssheetDir = os.path.dirname(sFile)
    ssheetDir = ssheetDir.replace("\\", "/") + "/"

    repl = {
        "qss:": ssheetDir,
        "@mainBackground1": "rgb(43, 43, 43)",
        "@borders": "rgb(90, 90, 90)",
        "@tableHeader": "rgb(35, 35, 35)",
        "@selectionBackgroundColor": "rgb(63, 68, 115)",
        "@selectionBackgroundHoverColor": "rgb(60, 80, 110)",
        "@selectionHoverColor": "rgb(43, 43, 43)",
        "@selectionColor": "rgb(255, 255, 255)",
        "@menuBackground": "rgb(26, 26, 26)",
        "@menuhoverbackground": "rgb(87, 87, 87)",
        "@menuSelectionbackground": "rgb(77, 77, 77)",
        "@buttonBackgroundDefault": "rgb(61, 61, 61)",
        "@buttonBackgroundDisabled": "rgb(55, 55, 55)",
        "@buttonBackgroundHover": "rgb(77, 77, 77)",
        "@buttonBackgroundBright1": "rgb(67, 67, 67)",
        "@buttonBackgroundBright2": "rgb(26, 26, 26)",
        "@white": "rgb(192, 192, 192)",
        "@tableBackground": "rgb(36, 36, 36)",
        "@inputHover": "rgb(35, 35, 35)",
        "@inputBackground": "rgb(28, 28, 28)",
        "@inputFocus": "rgb(28, 28, 28)",
        "@test": "rgb(200, 49, 49)",
        "@lightgrey": "rgb(190, 190, 190)",
        "@disabledText": "rgb(105, 105, 105)",
        "@tableBorders": "rgb(90, 90, 90)",
        "@scrollHandleColor": "rgb(75, 75, 75)",
        "@scrollHandleHoverColor": "rgb(87, 87, 87)",
    }

    for key in repl:
        stylesheet = stylesheet.replace(key, repl[key])

    return stylesheet
