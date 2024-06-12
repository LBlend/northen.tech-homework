import csv
import json
import os
from dataclasses import asdict, astuple, dataclass
from enum import Enum
from sys import argv


# Unecessary but feels cleaner and less fragile than using strings
# See https://stackoverflow.com/a/71666789 as to why we're inherting from str
class DependencyFileType(str, Enum):
    PIP = "pip"
    NPM = "npm"


@dataclass
class Dependency:
    name: str
    version: str
    path: str
    dependency_file_type: DependencyFileType


def get_all_dependencies(path: str) -> list[Dependency] | None:
    all_formatted_dependencies = []

    for subdir in os.listdir(path):
        # Convert subir to an actual path and not a directory name
        subdir = os.path.join(path, subdir)

        # I'm going to assume that the .git dir is valid
        git_dir = os.path.join(subdir, ".git")
        if not os.path.exists(git_dir):
            print("no git dir", git_dir)
            continue

        # Assumes we only have one type of dependency file in each repo
        # If you're a sane developer you shouldn't mix them anyway so it should be fine
        requirements_txt_path = os.path.join(subdir, "requirements.txt")
        package_json_path = os.path.join(subdir, "package.json")

        if os.path.exists(requirements_txt_path):
            dependencies = parse_requirements_txt(requirements_txt_path)
        elif os.path.exists(package_json_path):
            dependencies = parse_package_json(package_json_path)
        else:
            continue

        all_formatted_dependencies.extend(dependencies)

    return all_formatted_dependencies if all_formatted_dependencies else None


def parse_requirements_txt(path: str) -> list[Dependency]:
    with open(path, "r") as f:
        raw_data = f.readlines()

    dependencies = []
    for dependency in raw_data:
        # This assumes that all dependencies have a version specified and that the file is not malformed
        # Also assumes that there are no comments
        name, version = dependency.split("==")
        dependency = Dependency(name, version.strip("\n"), path, DependencyFileType.PIP)
        dependencies.append(dependency)

    return dependencies


def parse_package_json(path: str) -> list[Dependency]:
    with open(path, "r") as f:
        raw_data = json.loads(f.read())

    # There's potential for an exception here as there might be no dependencies listed at all
    dependencies = [
        Dependency(name, version, path, DependencyFileType.NPM)
        for name, version in raw_data.get("dependencies").items()
    ]

    return dependencies


def write_csv(dependencies: list[Dependency], output_directory: str):
    output_path = os.path.join(output_directory, "sbom.csv")

    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f, delimiter=",")
        for dependency in dependencies:
            writer.writerow(astuple(dependency))

    print(f"Saved SBOM in CSV format to {output_path}")


def write_json(dependencies: list[Dependency], output_directory: str):
    output_path = os.path.join(output_directory, "sbom.json")

    with open(output_path, "w") as f:
        json.dump(
            [asdict(dependency) for dependency in dependencies],
            f,
            indent=2,
        )

    print(f"Saved SBOM in JSON format to {output_path}")


if __name__ == "__main__":
    if len(argv) != 2:
        print("Wrong usage!")
        print("Use the following syntax: python3 sbom.py <directory>")
        exit(1)

    if not os.path.exists(argv[1]):
        print("Given directory not found!")
        exit(1)

    absolute_path = os.path.abspath(argv[1])

    dependencies = get_all_dependencies(absolute_path)
    if not dependencies:
        print("No valid repos containing requirements.txt or package.json found!")
        exit(1)

    write_csv(dependencies, absolute_path)
    write_json(dependencies, absolute_path)
