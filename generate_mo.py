import os.path
import subprocess

for locale in os.listdir("./locale"):
    if locale.endswith(".py"):
        continue
    file = os.path.join("./locale", locale, "LC_MESSAGES/bot.po")
    subprocess.call(
        [
            "msgfmt",
            file,
            "-o",
            os.path.join("./locale", locale, "LC_MESSAGES/bot.mo"),
        ]
    )
