# Homework - northern.tech

Command line tool for finding and documenting dependencies and their versions.

## Requirements

- Python 3.10 or newer

## Usage

The usage syntax is as follows:

```bash
python3 sbom.py <directory>
```

** Example **

```bash
python3 sbom.py /home/leander/
```

Note that absolute paths are not required when running the script like this. If you decide to import any functions from this file though make sure to use them.

## Assumptions & potential bugs

_Most assumptions are also listed in the code as comments. I suggest you read them there to get the full context._

- `.git` directories are always valid
- There is only one type of dependency file in each repository
- `requirements.txt` contains version numbers for all dependencies. The file is not malformed in any way and there are no comments.
- `package.json` always has dependencies listed i.e there's always a `dependencies` key.
- DevDependencies shall be ignored for `package.json`
- The file paths are not invalidated during runtime. In other words, not deleted, moved or modified.
- The script is run by a user that has privileges to read and write the files in the needed files and directories.

These assumptions are made to simplify the implementation. I might take my time to fix some of them before the deadline.

## TODO

- [ ] Write unit tests
- [ ] Create github workflows that run said tests, as well as linting
- [ ] Add more error handling i.e output human-friendly error messages
- [ ] Add support for `package-lock.json`
- [ ] Add git commit hash to the output
- [ ] Fix potential issues listed in the section above
- [ ] Docstrings for functions

## Ideas

- Add automatic CVE-scanning. Though this might be the task of a separate piece of software
- Support for more types of dependency files
