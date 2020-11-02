from pathlib import Path

from ismain import is_main

# create both 0.0.1 and 0.0.2 versions, but have the installer be of 0.0.1 to demo upgrade to 0.0.2

if is_main():

    # start with 0.0.2 to create and upload the clip
    version_key = "__version__ = "
    version_file_path = Path("pyshipexample", "__version__.py")
    for version in ["0.0.2", "0.0.1"]:
        version_file_path.write_text(f'{version_file_path.read_text().split(version_key)[0]}{version_key}{version}')
