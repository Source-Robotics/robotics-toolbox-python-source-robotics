# Releasing & Publishing Wheels

This document covers how to build and publish prebuilt wheels, including the
Linux ARM64 wheel needed for Raspberry Pi 5 installs.

---

## One-time setup — PyPI Trusted Publishing

Trusted Publishing lets GitHub Actions push to PyPI without a stored token.
Do this once per PyPI project.

1. Log in to [pypi.org](https://pypi.org) and open the project
   `roboticstoolbox-python-source-robotics`.
2. Go to **Manage → Publishing → Add a new publisher**.
3. Fill in:
   | Field | Value |
   |---|---|
   | Owner | `Source-Robotics` |
   | Repository | `robotics-toolbox-python-source-robotics` |
   | Workflow filename | `cibuildwheel.yml` |
   | Environment name | `pypi` |
4. Save.

Then in the GitHub repository:

1. Go to **Settings → Environments → New environment**.
2. Name it **`pypi`** (must match the workflow's `environment: pypi`).
3. Optionally add protection rules (e.g. require approval before publishing).

No API tokens or secrets are needed after this.

---

## How to trigger a wheel build + PyPI publish

### Automated path (recommended)

1. Make sure `pyproject.toml` has the correct version (e.g. `1.3.0.post2`).
2. Push all changes to `master`.
3. On GitHub, go to **Releases → Draft a new release**.
4. Set the tag to `v1.3.0.post2` (prefix `v` is stripped automatically).
5. Click **Publish release**.

GitHub Actions will then:

| Job | Runner | What it does |
|---|---|---|
| `Wheels (ubuntu-latest x86_64)` | x86_64 Linux | Builds `manylinux_2_28` x86_64 wheels |
| `Wheels (ubuntu-24.04-arm aarch64)` | **native ARM64** | Builds `manylinux_2_28` aarch64 wheels |
| `Wheels (macos-15-intel x86_64)` | macOS Intel | Builds macOS x86_64 wheels |
| `Wheels (macos-latest arm64)` | macOS Apple Silicon | Builds macOS arm64 wheels |
| `Wheels (windows-latest AMD64)` | Windows x86_64 | Builds Windows AMD64 wheels |
| `Wheels (windows-11-arm ARM64)` | Windows ARM64 | Builds Windows ARM64 wheels |
| `sdist` | Linux | Builds source distribution |
| `publish` | Linux | Collects all artifacts → uploads to PyPI |

The Linux aarch64 job runs on GitHub's native `ubuntu-24.04-arm` runner — no
QEMU emulation is used, so build times are fast and identical to a real ARM
machine.

### Manual build only (no publish)

Use **Actions → Build wheels (release + manual) → Run workflow** to build all
wheels without publishing. All wheel artifacts are uploaded and downloadable
from the workflow run summary page.

---

## Verifying the aarch64 wheel

After a successful release, check PyPI:

```
pip index versions roboticstoolbox-python-source-robotics
```

You should see a file like:

```
roboticstoolbox_python_source_robotics-1.3.0.post2-cp311-cp311-manylinux_2_28_aarch64.whl
```

On a Raspberry Pi 5 (Ubuntu 24.04, Python 3.11, aarch64):

```bash
pip install --only-binary=:all: roboticstoolbox-python-source-robotics==1.3.0.post2
python -c "import roboticstoolbox as rtb; print(rtb.__version__)"
```

If pip falls back to the sdist and tries to compile from source, the wheel
either wasn't built or the platform tags don't match. Confirm with:

```bash
pip install --only-binary=:all: --dry-run \
    roboticstoolbox-python-source-robotics==1.3.0.post2
```

---

## Downstream `requirements.txt` update

If `Source-Robotics/RCB-Runtime` pins an older version, update:

```
# was:
roboticstoolbox-python-source-robotics==1.3.0.post1

# update to:
roboticstoolbox-python-source-robotics==1.3.0.post2
```

The new version is the first release that ships a prebuilt ARM64 wheel on PyPI,
so downstream Raspberry Pi installs will no longer need to compile from source.

---

## Why `1.3.0.post2` and not `1.3.0.post1`?

`1.3.0.post1` may already have files on PyPI (sdist, or wheels from a prior
run). PyPI rejects uploads of files that already exist for a version. Using
`1.3.0.post2` guarantees a clean slate and avoids `File already exists` errors.
If you know `1.3.0.post1` has no files on PyPI, you can revert the version bump
and tag as `v1.3.0.post1` instead.
