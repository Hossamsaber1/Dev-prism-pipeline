import os


def load_stylesheet():
    sFile = os.path.dirname(__file__) + "/AfterEffects.qss"
    if not os.path.exists(sFile):
        return ""

    with open(sFile, "r") as f:
        stylesheet = f.read()

    ssheetDir = os.path.dirname(sFile)
    ssheetDir = ssheetDir.replace("\\", "/") + "/"

    repl = {
        "qss:": ssheetDir,
        "@mainBackground1": "rgb(35, 35, 35)",
        "@borders": "rgb(90, 90, 90)",
        "@tableHeader": "rgb(28, 28, 28)",
        "@selectionBackgroundColor": "rgb(25, 71, 154)",
        "@selectionBackgroundHoverColor": "rgb(168, 168, 168)",
        "@selectionHoverColor": "rgb(43, 43, 43)",
        "@selectionColor": "rgb(255, 255, 255)",
        "@menuBackground": "rgb(29, 29, 29)",
        "@menuhoverbackground": "rgb(69, 69, 69)",
        "@menuSelectionbackground": "rgb(77, 77, 77)",
        "@buttonBackgroundDefault": "rgb(61, 61, 61)",
        "@buttonBackgroundDisabled": "rgb(55, 55, 55)",
        "@buttonBackgroundHover": "rgb(77, 77, 77)",
        "@buttonBackgroundBright1": "rgb(67, 67, 67)",
        "@buttonBackgroundBright2": "rgb(26, 26, 26)",
        "@white": "rgb(192, 192, 192)",
        "@tableBackground": "rgb(28, 28, 28)",
        "@inputHover": "rgb(31, 31, 31)",
        "@inputBackground": "rgb(28, 28, 28)",
        "@inputFocus": "rgb(28, 28, 28)",
        "@test": "rgb(200, 49, 49)",
        "@lightgrey": "rgb(190, 190, 190)",
        "@disabledText": "rgb(105, 105, 105)",
        "@tableBorders": "rgb(90, 90, 90)",
        "@scrollHandleColor": "rgb(49, 49, 49)",
        "@scrollHandleHoverColor": "rgb(69, 69, 69)",
    }

    for key in repl:
        stylesheet = stylesheet.replace(key, repl[key])

    return stylesheet
