# setup script for bash.
SD=$(realpath $(dirname $BASH_SOURCE)/..)
export PYTHONPATH=$SD/crsq-heap/src:$SD/crsq-arithmetic/src:$SD/crsq-main/src:$SD/report2026/src
