#!/usr/bin/env python3

import typer
from pathlib import Path
import re

attribute_pattern = r"\[[^\[\]]+\]" # for removing branch rate attributes from BEAST 2 trees
log_pattern = r"^(\d+)\t(-\d+\.\d+)\t" # for retrieving the sample number and log-likelihood from each line of the log

def trees_to_t(trees_file: Path, t_file: Path):
    """
    Given a BEAST 2 .trees file, converts its contents to a MrBayes .t file.
    """
    # First, set up some processing flags:
    reading_trees = False
    # Then open the input and output files and proceed for each line in the input file:
    with open(trees_file, "r") as in_file, open(t_file, "w") as out_file:
        for line in in_file:
            # If we're reading the NEXUS header line, then copy the header and add another line with a fake ID:
            if line.strip() == "#NEXUS":
                out_file.write("#NEXUS\n")
                out_file.write("[ID: 0123456789]\n")
                continue
            # If we are entering the trees block, then change the processing flag and copy the content of the current line:
            if line.strip() == "Begin trees;":
                out_file.write(line)
                reading_trees = True
                continue
            # If we're reading lines from the trees block, then copy the current line with minor modifications
            # and change the processing flag only if this line marks the end of the trees block:
            if reading_trees:
                sub_line = line.replace("STATE_", "rep.") # change the tree's name to match the MrBayes convention
                sub_line = re.sub(attribute_pattern, "", sub_line) # remove all bracketed attributes
                sub_line = sub_line.replace(":0.0;", ";") # remove the root branch length, as MrBayes does not use it
                out_file.write(sub_line)
                if line == "End;":
                    reading_trees = False
                continue
    return

def log_to_p(log_file: Path, p_file: Path):
    """
    Given a BEAST 2 .log file, converts its contents to a minimal MrBayes .p file
    (containing only the log-likelihoods of the samples).
    """
    # Open the input and output files and proceed for each line in the input file:
    with open(log_file, "r") as in_file, open(p_file, "w") as out_file:
        for line in in_file:
            # If the current line is commented out, then don't copy it:
            if line.startswith("#"):
                continue
            # Otherwise, if the current line does not match the pattern for logged values, it must represent the header row;
            # write a fake ID declaration and a truncated header row for just the sample and log-likelihood:
            if re.match(log_pattern, line) is None:
                out_file.write("[ID: 0123456789]\n")
                out_file.write("Gen\tLnL\n")
                continue
            # Otherwise, extract the sample number and log-likelihood from this line and write them:
            groups = re.match(log_pattern, line).groups()
            out_file.write("%s\t%s\n" % (groups[0], groups[1]))

def main(
        trees_file: Path = typer.Argument(
            ...,
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
            help="The .trees output from BEAST 2 to convert.",
        ), 
        log_file: Path = typer.Argument(
            ...,
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
            help="The .log output from BEAST 2 to convert.",
        ), 
        t_file: Path = typer.Argument(
            ...,
            file_okay=True,
            dir_okay=False,
            writable=True,
            readable=False,
            resolve_path=True,
            help="The .t MrBayes output file to write. Note that branch rates will be stripped from the BEAST 2 trees during the conversion.",
        ), 
        p_file: Path = typer.Argument(
            ...,
            file_okay=True,
            dir_okay=False,
            writable=True,
            readable=False,
            resolve_path=True,
            help="The .p MrBayes output file to write. Note that this file will be minimal, containing only the sample numbers and log likelihoods.",
        )
    ):
    trees_to_t(trees_file, t_file)
    log_to_p(log_file, p_file)
    exit(0)

if __name__ == "__main__":
    typer.run(main)