# report2026 - data and script archive for the 2026 report

For data and script files, see [scripts/report2026_data/README.md](scripts/report2026_data/README.md)

## Setup for running the scripts.

The scripts require a GPU and cuda installation that is capable of running qiskit-aer-gpu.
The scripts were run on a PC with NVIDIA GeForce RTX4090 and CUDA version 12.4 installed.
The OS was Ubuntu 22.04 LTS.

The python code required by the scripts span across multiple repositories.
Extract the following repositories with release name "report2026" under a single directory.

- crsq-heap
- crsq-arithmetic
- crsq-main
- report2026

Create a virtual python environment and install the packages listed in report2026/requirements.txt.

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r report2026/requirements.txt
```

Setup PYTHONPATH using the following script.
```bash
$ cd report2026
$ source setup_pythonpath.sh
```

The scripts under report2026/scripts should now be runnable.
