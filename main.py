import subprocess


def get_package_list():
    res = subprocess.run(['pacman', '-Q'], stdout=subprocess.PIPE)
    list = res.stdout.decode("utf-8").split("\n")
    parsed_list = []
    for i in range(0, len(list) - 2):
        parsed_list.append(list[i].split(" ")[0])
    return parsed_list


def main():
    print(get_package_list())


if __name__ == "__main__":
    main()
