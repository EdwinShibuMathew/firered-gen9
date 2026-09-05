# Linux development setup

This guide reproduces the pinned build on **Ubuntu 26.04 LTS, x86_64**. The verified environment uses Python 3.14.4, make 4.4.1, host GCC/G++ 15.2.0, ARM GCC 14.2.1, ARM binutils 2.45.50.20251209, grit 0.9.2, and Pillow 12.3.0. Other Linux distributions, WSL, macOS, Windows, and architectures are unverified.

Use a fresh checkout in a path without spaces. Keep full Git history: the documentation audit verifies historical archive hashes. Provisioning writes only local dependencies and ignored upstream outputs after the initial host prerequisites. No ROM download, existing save, Supabase account, or private BPS is needed.

## 1. Check out the orchestration source

Obtain a revision containing this guide and its overlays, then open the project root. For a new clone:

```sh
git clone https://github.com/edwinshibumathew/firered-gen9.git
cd firered-gen9
git status --short
```

All remaining commands assume this root unless a subshell explicitly changes directory. For offline work, local Git mirrors at the same pinned commits can supply the clone sources.

The host needs Git, Bash, make, GCC/G++, Python with venv, dpkg-deb, pkg-config, and zlib development headers. On the verified Ubuntu host these are supplied by `git`, `build-essential`, `python3`, `python3-venv`, `dpkg`, `pkg-config`, and `zlib1g-dev`. Install missing host prerequisites through your normal package-management process. Confirm executable versions; do not silently substitute a different toolchain after a digest failure.

```sh
python3 --version
make --version
gcc --version
g++ --version
```

## 2. Provision the pinned binary packages

[toolchain-archives.json](../data/toolchain-archives.json) records the exact Debian archive filenames, package versions, and SHA-256 values used for the verified build. Place those archives in `.tools/debs/`. A matching local package cache is valid; archives themselves stay ignored. The list includes the optional mGBA frontend archive for runtime testing.

If the pinned versions are available from your configured package repositories, this downloads them without installing them into the host:

```sh
mkdir -p .tools/debs
python3 - <<'PY'
import json, subprocess
from pathlib import Path
for item in json.loads(Path('data/toolchain-archives.json').read_text()):
    subprocess.run(['apt-get', 'download', item['package'] + '=' + item['version']],
                   cwd='.tools/debs', check=True)
PY
```

Repository availability can change. If an exact version is unavailable, obtain that exact archive from the Ubuntu/Debian archive or a known local cache and verify it below. Do not install the latest version as a replacement. If a downloader spells an epoch differently in the filename, rename the downloaded archive to the manifest filename only after verifying its checksum.

The following verifies **all** archives before extracting any of them:

```sh
python3 - <<'PY'
import hashlib, json, subprocess
from pathlib import Path
items = json.loads(Path('data/toolchain-archives.json').read_text())
for item in items:
    archive = Path('.tools/debs') / item['file']
    if hashlib.sha256(archive.read_bytes()).hexdigest() != item['sha256']:
        raise SystemExit('Archive checksum mismatch: ' + str(archive))
for item in items:
    package = item['package']
    category = 'arm-gcc' if package.startswith(('gcc-arm', 'binutils-arm', 'libnewlib')) else 'freeimage'
    if package == 'mgba-sdl':
        category = 'mgba-sdl'
    subprocess.run(['dpkg-deb', '-x', str(Path('.tools/debs') / item['file']),
                    str(Path('.tools') / category)], check=True)
PY
mkdir -p .tools/compiler-path .tools/bin
ln -s ../arm-gcc/usr/bin/arm-none-eabi-as .tools/compiler-path/as
```

On an existing setup, inspect an existing assembler link before replacing it. The expected link above is relative and stays inside this repository. ARM assembler, linker, nm, and objcopy are supplied by the binutils archive inside `.tools/arm-gcc/`.

## 3. Prepare the Python and host-library environment

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install --only-binary=:all: --require-hashes -r requirements-build.txt
export PATH="$PWD/.tools/arm-gcc/usr/bin:$PATH"
export CPATH="$PWD/.tools/freeimage/usr/include"
export LIBRARY_PATH="$PWD/.tools/freeimage/usr/lib/x86_64-linux-gnu"
export LD_LIBRARY_PATH="$PWD/.tools/freeimage/usr/lib/x86_64-linux-gnu"
```

The requirement hash identifies the tested CPython 3.14 Linux x86_64 wheel. For offline installation, first download that wheel to `.tools/wheels/`, then add `--no-index --find-links .tools/wheels` to the installation command. A copied source checkout still needs its own venv; do not copy another developer's environment activation scripts.

Keep this shell active for the following steps. In a later shell, reactivate the venv and repeat the four exports from the root. The host-library variables allow pret's native graphics tools and grit to use the locally extracted PNG/FreeImage headers and libraries.

## 4. Clone the pinned upstreams and compiler sources

```sh
python3 - <<'PY'
import json, subprocess
from pathlib import Path
lock = json.loads(Path('build-lock.json').read_text())
Path('.upstream').mkdir(exist_ok=True)
for key, directory in [('pret_pokefirered', 'pret'), ('dpe_gen9', 'dpe'), ('cfru_expansion', 'cfru')]:
    item = lock['upstreams'][key]
    path = '.upstream/' + directory
    subprocess.run(['git', 'clone', item['url'], path], check=True)
    subprocess.run(['git', '-C', path, 'switch', '--detach', item['commit']], check=True)
    actual = subprocess.check_output(['git', '-C', path, 'rev-parse', 'HEAD'], text=True).strip()
    assert actual == item['commit'], (path, actual)
PY
git clone https://github.com/pret/agbcc.git .tools/agbcc
git -C .tools/agbcc switch --detach da598c1d918402c42c0c0d7128ba14567f3175e9
git clone https://github.com/devkitPro/grit.git .tools/grit-src
git -C .tools/grit-src switch --detach 5209ac206360dacf2a2e64d5a6a60ea3a38f512e
```

Do not run this clone block over existing checkouts. Inspect their pins and edits first. The compiler-source commits are also recorded in `build-lock.json`.

## 5. Build agbcc and grit locally

```sh
(cd .tools/agbcc && bash build.sh && bash install.sh ../../.upstream/pret)
python3 - <<'PY'
import re, subprocess
from pathlib import Path
root = Path.cwd()
grit = root / '.tools/grit-src'
libraries = root / '.tools/freeimage/usr/lib/x86_64-linux-gnu'
sources = re.findall(r'\b[\w/]+\.cpp\b', (grit / 'Makefile.am').read_text())
subprocess.run(['g++', '-O2', '-DPACKAGE_VERSION="0.9.2"',
    *['-I' + str(grit / name) for name in ('cldib', 'libgrit', 'extlib')],
    '-I' + str(root / '.tools/freeimage/usr/include'),
    *[str(grit / name) for name in sources], '-L' + str(libraries), '-lfreeimage',
    '-Wl,-rpath-link,' + str(libraries), '-o', str(root / '.tools/bin/grit')], check=True)
PY
```

The explicit grit source list comes from its pinned `Makefile.am`; compiling every `.cpp` also includes unused legacy files and fails. This build avoids an extra autotools dependency. The resulting executable uses `LD_LIBRARY_PATH` above at runtime.

```sh
arm-none-eabi-gcc --version
arm-none-eabi-as --version
.tools/bin/grit --version
python3 -c 'import PIL; print(PIL.__version__)'
```

Some upstream tools print warnings or a nonzero help/version exit status. Inspect their printed version and require actual build commands to succeed. No tool path should refer to another developer's checkout.

## 6. Apply overlays, audit, and build

```sh
python3 scripts/apply_overlays.py
python3 scripts/apply_overlays.py --check
python3 -m unittest discover -s tests -v
.codex/run-audits.sh
BUILD_JOBS=4 .codex/build-and-verify.sh
git diff --check
git status --short
```

The overlay applicator validates the declared patch chain and patch hashes. The generator checks compare materialized headers and ledgers. Builds verify every stage against `build-lock.json`, including payload and boot-layout checks. A successful build ends with the current CFRU SHA-256 from [STATUS.md](STATUS.md). The output is `.upstream/cfru/test.gba`; it is private and ignored. Audits and builds must not change tracked files.

The fresh-clone setup, locally rebuilt tools, all three stages, and subsequent incremental builds were exercised on the verified host. The test used exact local Git/package caches; live archive-download availability is not part of that result. Runtime smoke evidence is in [TESTING.md](TESTING.md).

For emulator testing, the optional SDL frontend needs its host runtime libraries. Use `ldd .tools/mgba-sdl/usr/games/mgba` to check them, or an installed mGBA 0.10.5. Test a separate copy of the verified ROM with a disposable save. Follow the current procedure in `TESTING.md`; a source audit is not a gameplay pass.

## Checks without a build environment

From a source-only checkout with full Git history and Python:

```sh
python3 scripts/audit_documentation.py
python3 scripts/audit_release.py
python3 scripts/generate_test_dashboard_data.py --check
python3 -m unittest discover -s tests -v
git diff --check
```

Ledger integration tests explicitly skip when upstream sources are absent. The remaining tests and commands above need no ROM, private BPS, compiler, or Supabase access. The full audit wrapper requires prepared upstreams. Dashboard administration is optional; see [TEST_DASHBOARD_SETUP.md](TEST_DASHBOARD_SETUP.md).

## Troubleshooting

| Symptom | Resolution |
|---|---|
| Missing compiler, PNG header, or FreeImage library | Recheck archive extraction, versions, venv, PATH, and library exports. Do not reuse an absolute symlink into another project. |
| Wrong upstream revision or patch context | Compare `git rev-parse HEAD` against the lock; preserve local work and recreate the affected checkout from pins/overlays in an isolated directory. |
| `PENDING` overlay | Run the overlay applicator without `--check`, then recheck. |
| Missing/unexpected build input | Restore the pinned input or review the manifest change using [ARCHITECTURE.md](ARCHITECTURE.md). Do not sort or regenerate the order blindly. |
| Stale ledger/header | Identify its generator, intentionally regenerate, inspect the diff, and rerun its check. |
| Stage hash or boot-layout mismatch | Stop. Compare pins, overlay state, ordering, tools, and the affected artifact; do not change locked hashes to hide the failure. |
| History/documentation audit failure in a shallow clone | Fetch complete project history before rerunning the audit. |
| Existing private ROM differs from the lock | Use the newly verified pipeline output and retain old observations under their original artifact hash. |

For a clean-build test, use another isolated checkout and provision it with these steps. Avoid recursive deletion or cleanup commands against a shared workspace containing user changes.
