if [[ `uname` -eq "Darwin" ]]; then
    source ~/.bash_profile
else
    source ~/.bashrc
fi

source "$(dirname $(readlink -f "$BASH_SOURCE"))/../activate.sh"