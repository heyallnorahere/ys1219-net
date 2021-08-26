from pkgdependencymanager import PackageConfig
from subprocess import Popen, PIPE, call as subprocess_call
from tempfile import TemporaryDirectory
from os.path import join
from argparse import ArgumentParser
import yaml
def call(args: list[str]):
    return_code = subprocess_call(args)
    if return_code != 0:
        exit(1)
def sync_deps(arguments):
    pkg_cfg = PackageConfig("dependencies.yml")
    pkg_cfg.install()
    with Popen(["find", "/usr/lib", "/usr/local/lib", "-name", "libacme_lw.a"], stdout=PIPE, stderr=PIPE) as command:
        output = command.communicate()
        stdout_output = output[0].decode("utf-8")
        entries = stdout_output.strip()
        if len(entries) <= 1:
            # we need to install acme-lw
            print("acme-lw not found - building and installing...")
            temp_dir = TemporaryDirectory()
            temp_dir_path = temp_dir.name
            build_dir = join(temp_dir_path, "build")
            # clone, build, and install
            call(["git", "clone", "https://github.com/jmccl/acme-lw", temp_dir_path])
            call([arguments.cmake, temp_dir_path, "-B", build_dir, "-G", "Unix Makefiles", "-DCMAKE_BUILD_TYPE=Release"])
            call(["make", "-C", build_dir, "-j", "8"])
            call(["sudo", "make", "install", "-C", build_dir, "-j", "8"])
            temp_dir.cleanup()
def read_options():
    with open("options.yml", "r") as stream:
        try:
            data = yaml.load(stream, Loader=yaml.Loader)
        except yaml.YAMLError as exc:
            print(exc)
        output = ""
        for option in data:
            if len(output) > 0:
                output += " "
            output += f"-D{option['name']}={option['value']}"
        return output
def configure(arguments):
    if arguments.debug:
        build_type = "Debug"
    else:
        build_type = "Release"
    arguments_list = [
        arguments.cmake,
        ".",
        "-B",
        "build/",
        "-G",
        "Unix Makefiles",
        "-DCMAKE_BUILD_TYPE=" + build_type
    ]
    for argument in read_options().split(" "):
        arguments_list.append(argument)
    call(arguments_list)
SCRIPTS = {
    "sync-deps": sync_deps,
    "configure": configure
}
argument_parser = ArgumentParser(description="runs a script associated with this project")
argument_parser.add_argument("script", help="specifies the name of the script to execute")
argument_parser.add_argument("--cmake", default="cmake", type=str, help="specifies the name of the cmake command to run")
argument_parser.add_argument("--debug", action="store_true")
arguments = argument_parser.parse_args()
try:
    function = SCRIPTS[arguments.script]
    function(arguments)
except KeyError:
    print("The specified command was not found!")
    exit(1)