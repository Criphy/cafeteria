#!/bin/bash
if [ "$(uname)" == "linux" ]; then
  rm -rf LICENSE README.md
  pkg install python postgresql
  pip install -r requirements.txt
  rm -rf requirements.txt
  chmod +x main.py
  CAFETERIA="$(pwd)/scripts/main.py"
  echo "Anything is installed! GG."
  echo "Command to start the game - python $CAFETERIA"
else
  echo "Installer can't starts on this system."
fi