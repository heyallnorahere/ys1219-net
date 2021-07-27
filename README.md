# ys1219-net

This is the source code for my website. To build, run:

```bash
PYTHON_COMMAND="{your python 3 command}"
$PYTHON_COMMAND scripts.py sync-deps
$PYTHON_COMMAND scripts.py configure
make -C build -j 8
```