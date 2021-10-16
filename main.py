import subprocess


def get_package_list():
    res = subprocess.run(["pacman", "-Q"], stdout=subprocess.PIPE)
    list = res.stdout.decode("utf-8").split("\n")
    parsed_list = []
    for i in range(0, len(list) - 2):
        parsed_list.append(list[i].split(" ")[0])
    return parsed_list


def get_info(package_name: str):
    return subprocess.run(["pacman", "-Qi", package_name],
                          stdout=subprocess.PIPE).stdout.decode("utf-8").split("\n")


def parse_info(info: list[str]):
    for i in range(0, len(info)):
        each = info[i].split(":")[0]
        if each.startswith("Optional Deps"):
            begin = i
        elif each.startswith("Required By"):
            end = i
            break

    out_list = []
    first = info[begin].split(":")[1].strip()

    if first != "None":
        out_list.append(first)
    else:
        return []

    for j in range(begin + 1, end):
        out_list.append(info[j].strip())
    return out_list


def main():
    print(get_package_list())


if __name__ == "__main__":
    main()
