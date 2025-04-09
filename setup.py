from setuptools import setup, find_packages
import os
import subprocess
from distutils.command.build_py import build_py


class BuildPyCommand(build_py):
    """Custom build command to compile protobuf files."""

    def run(self):
        proto_dir = os.path.join("pymumble_py3", "protos")
        output_dir = "pymumble_py3"

        os.makedirs(output_dir, exist_ok=True)

        if os.path.exists(proto_dir):
            proto_files = [
                os.path.join(proto_dir, f)
                for f in os.listdir(proto_dir)
                if f.endswith(".proto")
            ]

            for proto_file in proto_files:
                subprocess.check_call(
                    [
                        "python",
                        "-m",
                        "grpc_tools.protoc",
                        f"--proto_path={proto_dir}",
                        f"--python_out={output_dir}",
                        proto_file,
                    ]
                )

        build_py.run(self)


with open("pymumble_py3/constants.py") as f:
    tp = f.readline()
    version_from_constant = "0"
    while tp:
        if "PYMUMBLE_VERSION" in tp:
            version_from_constant = tp.split("=")[1].strip().replace('"', "")
            break
        tp = f.readline()


with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="pymumble",
    version=version_from_constant,
    author="Azlux",
    author_email="github@azlux.fr",
    description="Mumble library used for multiple uses like making mumble bot.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/azlux/pymumble",
    license="GPLv3",
    packages=find_packages(),
    install_requires=requirements
    + [
        "grpcio",
        "grpcio-tools",
        "protobuf",
    ],
    include_package_data=True,
    cmdclass={
        "build_py": BuildPyCommand,
    },
    package_data={
        "pymumble_py3.protos": ["*.proto"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    data_files=[("", ["LICENSE", "requirements.txt", "API.md"])],
)
