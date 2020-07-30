# Lorenzetti Event Simulator

[![Build Status](https://travis-ci.org/jodafons/lorenzetti.svg?branch=master)](https://travis-ci.org/jodafons/lorenzetti)
[![DOI](https://zenodo.org/badge/248031762.svg)](https://zenodo.org/badge/latestdoi/248031762)

Since of most part of the `datasets` from HEP experiments are private or do not contain the calorimetry low level information (like cells), we create the `Lorenzetti` group. The Lorenzetti is a iniciative to build an easier framework to produce HEP events and reconstructed eletromagnetic calorimeter information for machine learning HEP studies. This framework is able to generate events with `Pythia8`, propagate these particles throut of a generic calorimeter using `Geant4`, reconstruct the calorimeter information for, emulate
the eletronic pulse for each cell and estimate the cell's energy using the optimal filter technic. The events generated by pythia and simulated by geant are store into a root `ntuple` information that contain the low level information (cells, pulse energy, shower shapes and more) for the simulated data.

## Implemented Features:

- Pile-up simulation (in-time and out-of-time) using the bunch crossing information, eletronic simulation (pulse generator) and the cell's energy estimation;
- Shower shapes reconstruction based on the ATLAS standard calorimeter shower shapes;
- Rings information based on the ATLAS ringer algorithm;
- Cells energy for the RoI;
- Two types of ntuple for machine learning studies.

## Getting Started:

There are two ways you can run Lorenzetti: using a `Docker container` (stronglly recommended) or `locally` on your machine.
The locally installation usually can be used for geometry construction since allow the user to launch the `Qt`graphic inteface.

### Running with Docker

If you take a look at the [Lorenzetti's DockerHub](https://hub.docker.com/r/lorenzetti/lorenzetti) you'll find two main images:

* lorenzett/lorenzett:latest
* lorenzett/lorenzett:cluster

We'll refer to the `latest` image as `base`, since `cluster` inherits from it. More details on how these images are generated [here](https://github.com/jodafons/lorenzetti/tree/master/docker), on the `docker/` directory.

Our base image is meant for users that want to do a custom run on Lorenzett. If you're a first-timer, you'll want the `lorenzett/lorenzett:cluster` image.

#### Using the *cluster* image

```
docker run -v <output-path>:/output lorenzett/lorenzett:cluster -f PythiaGenerator/gen_zee.py -e 10 -j 10 -p 40 -o zee.reco.root -r reco_trf.py --bc_id_start -24 --bc_id_end 7 --ntuple physics --volume /output --seed 0
```

For `<args>` information, see below:

```
parser.sh - Script for running Lorenzetti cluster through docker in an one-line script
 
Arguments:
-h, --help                show this message
-f, --filter              chooses which type of event you're interested (example: PythiaGenerator/gen_zee.py)
-e, --event               sets the desired number of events
-j, --numberOfJobs        sets the number of jobs to run in the pythia generation phase. Each job will be generate n events.
-p, --pileupAvg           sets the pileup average
-o, --output              sets the output filename
-r, --reco_script         sets the reco script (example: reco_trf.py)
--bc_id_start             sets bc_id_start
--bc_id_end               sets bc_id_end
--ntuple                  sets the ntuple schemma (raw or physics)
--volume                  The path where everything will be mount
--seed                    The seed (Uses zero as default clock system)
--enableMagneticField     Enable the magnetic field
 
All arguments are required
```

#### Using the *latest* image

```
docker run -it -v <your-mount>:/volume lorenzett/lorenzett /bin/bash
```

> **Note**: You shall mount as many volumes as you wish.

As soon as your bash opens, you need to run
```
source setup_envs.sh
```

This will setup everything you need for Lorenzett.

For **event generation**, this is the command you're looking for (example for Zee):
```bash
prun_job.py -c "generator/PythiaGenerator/share/gen_zee.py -i zee_config.cmnd --outputLevel 6 --seed 0 -evt <n_events> --pileupAvg <average-pileup> --bc_id_start -8 --bc_id_end 7" -o zee.root -mt <n_threads> -n <n_jobs>
```

> **Notes**
> - Files like `zee_config.cmnd` are located at `/code/lorenzetti/generator/PythiaGenerator/data/`
> - Using seed=0 means that you'll use your system clock as seed.
> - All scripts for event generation can be found [here](https://github.com/jodafons/lorenzetti/tree/master/generator/PythiaGenerator/share).


For **reconstruction**, after generate the events using the `gen_*.py` command, you must pass the output file as input to the reconstruction transformation. To run the reconstruction use this command:

```bash
scripts/reco_trf.py -i zee.root --outputLevel 6 -nt <n_jobs> -o reco_zee.root
```

### Running locally

#### Requirements

- Geant4 (opengl or qt4 is required for graphic interface, https://github.com/jodafons/geant4.git);
- ROOT (https://github.com/root-project/root.git);
- Pythia8 (https://github.com/jodafons/pythia.git);
- HEPMC (https://github.com/jodafons/hepmc.git);
- FastJet (https://github.com/jodafons/fastjet.git);
- Gaugi (pip3 install gaugi).



### Useful scripts:

You can convert the ROOT ntuple information into a `numpy` array using the `convert.py` script and the reconstruction ntuple output.

```
python3 scripts/convert.py -i zee.reco.root -o zee.reco.npz --nov -1
```

> *Notes:*
> - Only supported by the `physics` ntuple schemma.
> - All cells (in matrix format) will be available using this script.

## References:

- Athena framework: https://gitlab.cern.ch/atlas/athena


