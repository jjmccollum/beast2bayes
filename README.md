# beast2bayes
Python utility for converting .trees and .log files from BEAST 2 to .t and .p files from MrBayes

## About
I developed this software to meet a rather specific need: I wanted to apply the `sprspace` software (https://github.com/cwhidden/sprspace) to a posterior distribution of trees sampled in BEAST 2, but the software only worked with outputs from MrBayes.
Since others have expressed the same concern in the `sprspace` repo's issues, and since similar situations could very well arise for other software, I put together a lightweight Python script that converts BEAST 2 .trees and .log outputs to .t and .p files.
The only dependencies of the script are typer, pathlib, and re, and of these, only typer should need to be installed through pip.
For now, the .log to .p conversion maps only two fields of interest, the sample number and its posterior log-likelihood.
The code could easily be adapted to include more (or all) columns from the log table, but the column names might have to be mapped to conventional names in .p files.

## Installation and Usage

To install, just clone this repository or download the `beast2bayes.py` script from the `beast2bayes` directory.

To use the script, simply specify the two BEAST files and their respective MrBayes counterparts as follows:

```bash
python beast2bayes.py beast.trees beast.log mrbayes.t mrbayes.p
```