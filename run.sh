#!/bin/bash

../termux-apt-repo/termux-apt-repo -s /storage/android/cross-compile/termux-packages/debs/ -o . --sign-gpg
./make_index.py .
