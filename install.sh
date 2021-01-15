#!/bin/bash

uid=$(id -u)

if [ "$uid" -ne 0 ]
    then echo "Error: To install, please run as root (uid 0)."
    exit
fi

cp ./breach-parse.sh ./breach-parse
mv ./breach-parse /usr/local/bin/

echo "Installation complete. Usage: $ breach-parse"