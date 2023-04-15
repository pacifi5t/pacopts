import subprocess
import os
from termcolor import colored

env = os.environ.copy()
env['LANG'] = 'en_US.utf8'
env['LC_ALL'] = 'C'


def get_package_list():
    process = subprocess.run(['pacman', '-Q'], env=env, capture_output=True, text=True)
    lst = process.stdout.strip().split('\n')
    parsed_list = [package.split(' ')[0] for package in lst]
    return parsed_list


def get_optional_deps(package_name: str):
    process = subprocess.run(['pacman', '-Qi', package_name], env=env, capture_output=True, text=True)
    info = process.stdout.strip().split('\n')

    filtered = []
    optional_deps_started = False
    for line in info:
        if line.startswith('Required By'):
            break

        if optional_deps_started:
            filtered.append(line.strip())

        if line.startswith('Optional Deps'):
            optional_deps_started = True
            filtered.append(''.join(line.split(':', 1)[1]).strip())

    return [each for each in filtered if '[installed]' not in each and each != 'None']


def print_output(optional_deps, package_name):
    if not optional_deps:
        return

    print(f'{colored(package_name, "cyan", attrs=["bold"])}:')
    for dep in optional_deps:
        split = dep.split(':', 1)
        if len(split) > 1:
            print(f'  - {split[0].strip()} {colored(split[1].strip(), "dark_grey")}')
        else:
            print(f'  - {split[0].strip()}')
    print()


def main():
    package_list = get_package_list()
    for package_name in package_list:
        optional_deps = get_optional_deps(package_name)
        print_output(optional_deps, package_name)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nExit by keyboard interrupt')
