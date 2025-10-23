#!/bin/bash
if [[ $0 == $BASH_SOURCE ]]; then
    echo "This script should be sourced and never run directly!"
    exit 1
else
    if [[ -z ${ENV_ACTIVATED} ]]; then
        curr_dir=`pwd`
        script_dir=$(dirname $(readlink -f "$BASH_SOURCE"))
        cd ${script_dir}


        orig_ps1=${PS1}
        source .venv/bin/activate
        PS1="(project env) ${orig_ps1}"

        cd ${curr_dir}

        export ENV_ACTIVATED=1
        echo "Activated project environment!"
    else
        echo "Environment already activated; doing nothing..."
    fi
fi