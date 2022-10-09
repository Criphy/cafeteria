#!/bin/bash
SYSTEM="$(uname)"
CAFEDIR="/cafeteria/scripts/main.py"
if [ "$SYSTEM" == "Linux" ]; then
  rm -rf LICENSE README.md
  pkg install python postgresql
  pip install -r requirements.txt
  rm -rf requirements.txt
  chmod +x main.py
  export CAFEDIR="$CAFEDIR"
  echo "Anything is installed! GG."
  echo "Command to start the game - python \$CAFEDIR"
  cd /
else
  echo "Installer can't starts on this system."
fi