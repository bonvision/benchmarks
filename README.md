# BonVision Benchmarks

This repository contains various performance and latency benchmarks for the BonVision package. Stimulus generation, data acquisition, and analysis scripts used to benchmark BonVision against PsychoPy and PsychToolbox are provided.

## How to use

All data acquisition is done using the Harp behavior board, which can be obtained at:
https://www.cf-hw.org/harp/behavior

Drivers and runtime dependencies for the Harp stack can be found at:
https://bitbucket.org/fchampalimaud/downloads/downloads/

Scripts for closed loop latency and frame-rate measurements were developed using the [Bonsai](https://bonsai-rx.org/) visual programming language, and are executed independently of stimulus generation. A self-contained bootstrapper executable can be found in the **bonsai** folder in this repository. Running the executable should automatically reproduce the environment configuration used for data acquisition.

