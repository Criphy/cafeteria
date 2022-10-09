#!/bin/bash
SYSTEM="$(uname)"
if [ "$SYSTEM" == "Linux" ]; then
  rm -rf LICENSE README.md
  pkg install python postgresql
  pip install -r requirements.txt
  chmod +x ./scripts/main.py
  sudo export CAFE="$(pwd)/scripts/main.py"
  sudo export CAFEID="$(pwd)/scripts/id"
  echo "Anything is installed! GG."
  echo "Command to start the game - python \$CAFE"
else
  echo "Installer can't starts on this system."
fi