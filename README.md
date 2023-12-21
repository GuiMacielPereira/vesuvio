# VESUIVO REPOSITORY

This repository contains:
- `mvesuvio` package containing the Optimized NCP analysis procedures, published nightly.
- Vesuvio calibration script

## mvesuvio package

### Install mamba

To use the `mvesuvio` package you will need to use the `conda` package manager (or preferably  `mamba`, a much faster implementation of `conda`).

This is also the recommended best practice way of using the mantid packages.

To download and install mamba:
- https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html

### Create and activate an environment

To create a conda environment for `mvesuvio`:
- `mamba env create -n <environment_name> -c mantid/label/nightly mvesuvio`

To activate the conda environment:
- `conda activate <environment_name>`

### Using mvesuvio via the command line

You can use `mvesuvio` via the command line. There are two commands available: `config` and `run`.

#### config

The `config` command has three optional arguments:
- `--set-cache` - Sets the location `mvesuvio` will set up the experiment directory.
- `--set-experiment` - Sets the current experiment. This creates a new directory in the experiment directory (if not existing) which contains an input file. `mvesuvio` caches and outputs workspaces here.
- `--set-ipfolder` - Sets the directory in which `mvesuvio` will look for instrument parameter files.

If any of these arguments are not provided a default location/experiment will be selected. These will be output on the running of `mvesuvo config`

Usage examples:
- `mvesuvio config --set-cache C:\Vesuvio --set-experiment example1 --set-ipfolder C:\IPFolder` - Set cache and IP folder, create a new experiment directory called `example1`.
- `mvesuvio config --set-experiment example2` - Creates a new experiment directory in `C:\Vesuvio` called `example2`.

#### run

The `run` command has one optional argument:
- `--yes` - If provided, this argument automatically inputs `Y` when prompted for user input.

Usage example:
- `mvesuvio run --yes` - Run the vesuvio analysis, automatically providing `Y` when prompted.
- `mvesuvio run`- Run the vesuvio analysis, will wait for user input when prompted.

### Using mvesuvio via workbench

You can also use `mvesuvio` via `mantidworkbench` if you desire a higher degree of interaction with the output workspaces.

To do this, install workbench into your existing vesuvio conda environment:
- `mamba install mantidworkbench`

Start workbench using the command line:
- `workbench`

In the workbench script editor you must first import mvesuvio:

- `import mvesuvio as mv`

After this you can set the config if desired, as above in the command line example. All arguments are optional.

- `mv.set_config(cache_directory='C:\Vesuvio', experiment_id='example3', ip_folder='C:\IPFolder')`

Following the setting of the config, you can use workbench to open and edit the analysis input file created in the relevant experiment directory.
Once the inputs have been ammended and the file saved, run the analysis:

- `mv.run(yes_to_all=True)`

## Outdated documentation (To Review):
### Currently in development, daily updates and corrections.

Three example scripts are provided, BaH2_500C, D_HMT and starch_80_RD, each detailing the initial conditions for each sample.

Start with script starch_80_RD, includes most complete comments.

How to use for a new sample:

    1. Copy one of the main scripts (for example starch_80_RD.py) and create a new .py file with the name of the desired sample and in the sample directory as D_HMT.py or starch_80_RD.py.

    2. Fill in the new script with the desired initial conditions.

    3. Run the script. The script will create a new directory for the sample under experiments/, and will try to use LoadVesuvio to store the workspaces locally for future runs. If LoadVesuvio fails, the user needs to copy the worksapces as .nxs files onto experiments/sample/input_ws/, using the same format as the example samples provided.

    4. After the workspaces are stored locally, any further data reduction will run using the local workspaces.

    5. Bootstrap option is still under development, but any data from running bootstrap is stored under experiments/sample/bootstrap_data/ or experiments/sample/jackknife_data

    6. Analysis of bootstrap data works only with stored data in directories mentioned in point 5, it does not run any bootstrap
