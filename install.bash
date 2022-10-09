#!/bin/bash
rm -rf LICENSE README.md
pkg install python postgresql
pip install -r requirements.txt
rm -rf requirements.txt
chmod +x main.py
CAFETERIA="$(pwd)/scripts/main.py"
echo "Anything is installed! GG."
echo "Command to start the game - python $CAFETERIA"