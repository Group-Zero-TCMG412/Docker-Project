#!/bin/bash


echo "Heard ya wanna do some things... lets do some things!"

echo "Creating WMDs..."
python3 -m venv myvenv

echo "Priming warheads"
source myvenv/bin/activate

echo "Pushed the big red button!"
pip3 install --editable .

echo "Mission accomplished"









