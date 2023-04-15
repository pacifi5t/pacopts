#! /bin/sh

SCRIPT_PATH="$(readlink -f "$0")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"

setup() {
  python3 -m venv "$SCRIPT_DIR/.venv"
  . "$SCRIPT_DIR/.venv/bin/activate"
  pip3 install --disable-pip-version-check -r "$SCRIPT_DIR/requirements.txt"
}

if [ ! -d "$SCRIPT_DIR/.venv" ]; then
  echo "Setting up virtual environment and installing dependencies..."
  setup > /dev/null
  echo "Done!\n"
fi

. "$SCRIPT_DIR/.venv/bin/activate"
python3 "$SCRIPT_DIR/pacopts.py"
