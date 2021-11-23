#!/bin/bash

clear


echo "This is a bash script for your bash script. This stuffed is layered like a onion or something."

echo "The purpose of this script is to walk you through some things. Cause walking can be hard."

echo "In order to run the API's CLI, you must create a virtual env to run it in alonside other tasks. The github repo you pulled this from has another bash script called: cli.sh "

echo "In order to run this bash script you must enter the following command in the terminal: source cli.sh"

echo "You can input yes to let this script do that for you, or you can be a independent person who don't need no script and input no"

read input

if [ "$input" = "yes" ]
then
        source cli.sh
else
        echo "Fine, bye."

fi







