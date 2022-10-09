#!/bin/bash
rm -rf LICENSE README.md
pkg install python postgresql
pip install -r requirements.txt
rm -rf requirements.txt
mv ./scripts/main.py ./
chmod +x main.py
set CAFETERIA="$(pwd)/main.py"
echo "Anything is installed! GG."
echo "Command to start the game - python \$CAFETERIA"