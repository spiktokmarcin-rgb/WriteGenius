"""Entrypoint for `python -m writegenius`."""

import sys
from writegenius.cli import main

if __name__ == "__main__":
    sys.exit(main())
