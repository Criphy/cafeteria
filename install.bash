#!/bin/bash
if [ "$(uname)" == "Linux" ]; then
  rm -rf LICENSE README.md
  pkg install python postgresql tsu unzip
  pip install -r requirements.txt
  curl -L -o Cafeteria_Scripts.zip 'https://drive.google.com/uc?export=download&id=1uOQ9RHqDXSuOqiexYOYOKCQIlyUVbR5N'
  unzip Cafeteria_Scripts.zip -d ./scripts
  chmod +x ./scripts/main.py
  CAFE="$(pwd)/scripts/main.py"
  echo "Anything is installed! GG."
  echo "Command to start the game - sudo python $CAFE"
else
  echo "Installer can't starts on this system."
fi