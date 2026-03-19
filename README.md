# tiss-cli

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
![PyPI - Version](https://img.shields.io/pypi/v/miss-cli)

`tiss-cli` is a minimal cli application that allows users to track exam dates easily
from [tiss], the platform to register for exams at the TU Wien.

This project is not affiliated with TU Wien and only aims to support students plan their studies.

To start tracking exams, add courses first

```bash
$ tiss add 123.123

# optionally give the course a name
$ tiss add 123.123 -name=MyCourse
```

Next synchronise the tracked courses with [tiss]

```bash
$ tiss sync
```

Now you can inspect the list of exams sorted by date

```bash
$ tiss list
```

[just]: https://github.com/casey/just
[uv]: https://docs.astral.sh/uv/getting-started/installation/
[tiss]: https://tiss.tuwien.ac.at/
