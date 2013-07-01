#!/bin/bash

# adds .gitignore files to all the empty directories below the current working directory
find . -type d -empty -exec touch {}/.gitignore \;
