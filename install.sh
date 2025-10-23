#!/bin/bash

set -e

curr_dir=`pwd`
script_dir=$(dirname $(readlink -f "${0}"))
cd ${script_dir}

if [[ ! -d .vscode ]]; then
    mkdir .vscode
    cp -r .vscode_support/.default_vscode/ .vscode/
else
    echo "Warning: .vscode folder already exists, skipping installation of default..."
    echo "Consider manually copying any desired default settings from .vscode_support/.default_vscode"
fi


rm -rf .venv/
python3.13 -m venv .venv
source .venv/bin/activate
#pip3.13 install -r requirements.txt

echo "Local development environment installed!"
echo '(To activate, run `source activate.sh`)'

cd ${curr_dir}