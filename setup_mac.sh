#!/usr/bin/env bash
# To install on Mac, you need a new version of llvm than the one shipped with MacOS
# so using brew you can run
#
# $ brew install llvm
#
# and then run this file with your usual arguments, e.g. './setup_mac.sh test'

export CC="/usr/local/opt/llvm/bin/clang"
export CFLAGS="-I/usr/local/opt/llvm/include"
export CPP="/usr/local/opt/llvm/bin/clang"
export CPPFLAGS="-I/usr/local/opt/llvm/include"
export LDFLAGS="-L/usr/local/opt/llvm/lib"

python setup.py $@