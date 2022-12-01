#!/bin/bash

echo "compiling photoStats"
g++ photoStats.cxx -o photoStats `root-config --cflags` `root-config --libs`
