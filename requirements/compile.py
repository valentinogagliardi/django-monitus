import os
import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    os.environ["CUSTOM_COMPILE_COMMAND"] = "requirements/compile.py"
    common_args = ["-m", "piptools", "compile", "--generate-hashes"] + sys.argv[1:]

    subprocess.run(
        [
            "python3.8",
            *common_args,
            "-P",
            "Django>=3.0a1,<3.1",
            "-o",
            "py38-django30.txt",
        ],
        check=True,
    )
    subprocess.run(
        [
            "python3.8",
            *common_args,
            "-P",
            "Django>=3.1a1,<3.2",
            "-o",
            "py38-django31.txt",
        ],
        check=True,
    )
