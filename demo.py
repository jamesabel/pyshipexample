from pathlib import Path
import subprocess

from balsa import Balsa, get_logger
import appdirs
from ismain import is_main
from pyshipupdate import rmdir

# create both 0.0.1 and 0.0.2 versions, but have the installer be of 0.0.1 to demo the upgrade to 0.0.2

app_name = "pyshipexample"
author = "abel"

log = get_logger(app_name)

if is_main():

    python_exe_path = Path("venv", "Scripts", "python.exe")

    balsa = Balsa(app_name, author)
    balsa.init_logger()

    # remove any old clips
    for d in Path(appdirs.user_data_dir(app_name, author)).glob(f"{app_name}_0.0.*"):
        if d.is_dir():
            log.info(f"removing {str(d)}")
            rmdir(d)

    # start with 0.0.2 to create and upload the clip
    version_key = "__version__ = "
    version_file_path = Path(app_name, "__version__.py")
    for version in ["0.0.2", "0.0.1"]:

        # write out the version
        text_up_to_the_version = version_file_path.read_text().split(version_key)[0]
        version_file_path.write_text(f'{text_up_to_the_version}{version_key}"{version}"\n')

        # create this particular dist using flit
        rmdir(Path("dist"))
        subprocess.run([python_exe_path, "-m", "flit", "build"], capture_output=True)

        # change the -p (AWS profile) if you need to use a different profile than default
        subprocess.run([python_exe_path, "-m", "pyship", "-p", "default"])
