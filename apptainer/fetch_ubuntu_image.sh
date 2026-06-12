#!/bin/sh -e

echo "pull a docker image of ubuntu and make an apptainer image"

apptainer pull docker://ubuntu:22.04
