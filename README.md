# report2026 - data and script archive for the 2026 report

For data and script files, see [scripts/report2026_data/README.md](scripts/report2026_data/README.md)

## Extracting the code repositories

The python code required by the scripts span across multiple repositories.
Extract the following repositories with release name "report2026" under a single directory.
This should be done outside the apptainer container.

- crsq-heap
- crsq-arithmetic
- crsq-main
- report2026

## Preparing an Apptainer container

The scripts require a GPU and cuda installation that is capable of running qiskit-aer-gpu.
The scripts were run on a PC with NVIDIA GeForce RTX4090 and CUDA version 12.4 installed.
The OS was Ubuntu 22.04 LTS. Apptainer was used to create a container to run the scripts.
The apptainer def file can be found in the folder apptainer. Apptainer, CUDA12.4, NVIDIA
driver must all be installed on the host OS.

```bash
$ cd apptainer
$ ./fetch_ubuntu_image.sh
$ apptainer build qiskit-gpu.sif qiskit-gpu.def
```

A shell inside the container can be started by
```bash
apptainer run --nv --cleanenv /your/path/to/qiskit-gpu.sif
```

## Setup for running the scripts.

The following should be done inside the container.

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
