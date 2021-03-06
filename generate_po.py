import os
import re
import shutil
import subprocess
import sys
from contextlib import suppress

if len(sys.argv) == 1:
    print("missing required argument <language>")
    sys.exit(1)
locale = sys.argv[-1]
file = f"./locale/{locale}/LC_MESSAGES/bot.po"
if not os.path.isdir(f"locale/{locale}/LC_MESSAGES"):
    os.makedirs(f"locale/{locale}/LC_MESSAGES")
with suppress(FileNotFoundError):
    shutil.copy(file, file + ".bak")
with suppress(FileNotFoundError):
    os.remove(file)
all_files = """import os
for dir, subdirs, files in os.walk("."):
    if 'venv' in dir or 'locale' in dir:
        continue
    for file in files:
        if file.endswith('.py'):
            fname = os.path.join(dir, file)
            print(fname)"""
if not os.path.isfile("./locale/all_files.py"):
    with open("./locale/all_files.py", "w") as f:
        f.write(all_files)

stuff = subprocess.run(
    [sys.executable, "./locale/all_files.py"], capture_output=True
)
content = stuff.stdout

subprocess.run(
    [
        "xgettext",
        "--files-from=-",
        "--from-code=UTF-8",
        "--keyword",
        "--keyword=_t",
        "--keyword=_l",
        "-o",
        file,
    ],
    input=content,
)
with open(file) as f:
    data = f.read()

data = re.sub(
    r'^"Language: \\n"$', fr'"Language: {locale}\\n"', data, flags=re.MULTILINE
)
data = re.sub(
    r'^"Content-Type: text/plain; charset=CHARSET\\n"$',
    r'"Content-Type: text/plain; charset=UTF-8\\n"',
    data,
    flags=re.MULTILINE,
)

with open(file, "w") as f:
    f.write(data)

if os.path.exists(file + ".bak"):
    subprocess.run(
        [r"msgcat", file, file + ".bak", "-o", file + ".cat", "--use-first"]
    )
# os.remove(file)
with suppress(FileNotFoundError):
    os.rename(file + ".cat", file)
