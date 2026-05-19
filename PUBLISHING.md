# Publishing Source Robotics Robotics Toolbox

This fork is published as the PyPI distribution
`roboticstoolbox-python-source-robotics`, while the Python import package remains
`roboticstoolbox`.

Because this project ships compiled C/C++ extensions, source installs require a
working compiler. For the smoothest user install experience, publish wheels for
the platforms you support.

## Local Build Check

Use a clean virtual environment with Python 3.10 or newer.

```shell
py -m pip install -U pip build twine
py -m build
```

This creates release artifacts in `dist/`.

## Local Install Check

```shell
py -m pip uninstall -y roboticstoolbox-python roboticstoolbox-python-source-robotics
py -m pip install dist/*.whl
cd ..
py -c "import roboticstoolbox as rtb; print(rtb.__version__)"
```

Run the import check from outside the repository root. If you run it from the
project directory, Python imports the local `roboticstoolbox` source folder
instead of the installed wheel, and the compiled extension modules such as
`roboticstoolbox.fknm` will not be present in that source folder.

## TestPyPI Upload

TestPyPI and PyPI use separate accounts and separate API tokens. A token from
`pypi.org` will not work on `test.pypi.org`.

For the first upload of a new project name, create an account-scoped API token
on TestPyPI. A project-scoped token only works after that project already
exists.

```shell
py -m twine upload --repository testpypi dist/*
```

When prompted, paste the TestPyPI token. If your Twine version asks for a
username and password instead, use `__token__` as the username and the TestPyPI
token as the password.

Then test installation from TestPyPI:

```shell
py -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ roboticstoolbox-python-source-robotics
```

## PyPI Upload

Only upload to real PyPI after the TestPyPI install works.

PyPI needs its own token from `pypi.org`; the TestPyPI token will not work here.
For the first real upload, use an account-scoped PyPI token.

```shell
py -m twine upload dist/*
```

Users can then install the fork with:

```shell
pip3 install roboticstoolbox-python-source-robotics
```

If they already have the upstream package installed, they should remove it first
because both distributions provide the same `roboticstoolbox` import package:

```shell
pip3 uninstall roboticstoolbox-python
pip3 install roboticstoolbox-python-source-robotics
```
