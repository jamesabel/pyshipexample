# pyshipexample

pyship example program

Learn how to use pyship by using pyshipexample

---

## Create your Python "main" application as a normal package distribution

There is nothing about this step that is particularly special about pyship.  Create your application that can be run
as "main" (e.g. `python -m <your module>`). Package it up as a distribution using whatever tool you like (e.g. `flit`, 
`setup.py`, etc.). The result should be a distribution (e.g. a wheel), typically in the `dist` directory.

## Fill in pyproject.toml with your project name and pyship specific directives

pyproject.toml:
```
[project]
name = "pyshipexample"

[tool.pyship]
is_gui = true
```

## Run pyship
`python -m pyship`

---
