#!/bin/bash

cwd=$(pwd)
mkdir -p $cwd/cache
export TFHUB_CACHE_DIR=$cwd/cache
echo "TFHUB_CACHE_DIR=$TFHUB_CACHE_DIR"
