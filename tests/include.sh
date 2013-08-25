#! /usr/bin/env sh

config=$1

[[ -z $1 ]] && \
	config="--config include.yaml"

python ../include.py ${config}

