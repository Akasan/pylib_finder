from stdlib_list import stdlib_list
import os
import click
from glob import glob


def _find_python_files(folder):
    return glob(os.path.join(folder, "*.py"))


def _get_root_lib_name(libname):
    return libname.split(".")[0]


def _is_python_file(filename):
    return filename[-3:] == ".py"


def get_files(root_folder, result=[]):
    for path, subfolders, files in os.walk(root_folder):
        for subfolder in subfolders:
            result = get_files(os.path.join(path, subfolder), result)
        for filename in files:
            if _is_python_file(filename):
                result.append(os.path.join(path, filename))

    return result


@click.command()
@click.option("-f", "--filename", "filenames", multiple=True)
@click.option("--o", "--output", "is_output", is_flag=True)
@click.option("--r", "--recursive", "search_recursive", is_flag=True)
@click.option("--of", "--output_filename", "output_filename", default="requirements.txt")
@click.option("--ow", "--over_write", "is_over_write", is_flag=True)
def main(filenames, is_output, search_recursive, output_filename, is_over_write):
    libs = []
    std_libs = stdlib_list()

    if len(filenames) == 0 and search_recursive:
        filenames = get_files(os.getcwd())


    for filename in filenames:
        with open(filename, "r", encoding="utf-8-sig") as f:
            for line in f.readlines():
                line = line[::-1].strip()[::-1].strip()

                if line[:4] == "from" or line[:6] == "import":
                    as_idx = line.find("as")
                    if as_idx >= 0:
                        line = line[:as_idx]          
                        line = line.strip()

                    split = line.split(" ")
                    if split[0] == "from":
                        libname = split[1]
                    else:
                        libname =split[-1]

                    if libname[0] == ".":
                        continue

                    libname = _get_root_lib_name(libname)
                    if not libname in libs and not libname in std_libs:
                        libs.append(libname)

    if is_output:
        write_mode = "a+" if is_over_write else "w"
        with open(output_filename, write_mode) as f:
            for lib in libs:
                f.write(f"{lib}\n")


if __name__ == "__main__":
    main()
