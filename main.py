import subprocess
import os

my_env = os.environ.copy()
my_env["LANG"] = "en_US.utf8"

filter_regex = r"\[installed\]"


def get_package_list():
    res = subprocess.run(["pacman", "-Q"], stdout=subprocess.PIPE)
    list = res.stdout.decode("utf-8").split("\n")
    parsed_list = []
    for i in range(0, len(list) - 2):
        parsed_list.append(list[i].split(" ")[0])
    return parsed_list


def get_info(package_name: str):
    return (
        subprocess.run(
            ["pacman", "-Qi", package_name],
            stdout=subprocess.PIPE,
            env=my_env,
        )
        .stdout.decode("utf-8")
        .split("\n")
    )


def parse_info(info: list[str]):
    for i in range(0, len(info)):
        each = info[i].split(":")[0]
        if each.startswith("Optional Deps"):
            begin = i
        elif each.startswith("Required By"):
            end = i
            break

    out_list = []
    lst = info[begin].split(":")
    first = lst[1].strip()

    if first == "None":
        return []

    try:
        reason = lst[2].strip()
    except:
        reason = ""

    if (first + reason).rfind("[installed]") == -1:
        out_list.append(first + ": " + reason)

    for j in range(begin + 1, end):
        temp = info[j].strip()

        if temp.rfind("[installed]") == -1:
            out_list.append(temp)

    return out_list


def main():
    lst = get_package_list()
    for el in lst:
        deps = parse_info(get_info(el))
        if len(deps) != 0:
            print(el)
            for d in deps:
                print("\t" + d)
            print("\n")


if __name__ == "__main__":
    main()
