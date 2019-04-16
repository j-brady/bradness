#!/usr/bin/env python3

"""
This script allows extraction of dynamic light scattering data from csv files collected by a Wyatt DynaPro DLS plate reader. It is helpful when performing experiments on the same plate with other researchers and your data is interleaved. Using this script pulls out the data for the plate wells that you want and writes them to a new csv file for you to later fit.

The script takes a yaml file with the well names in the format [letter][number]_, i.e. well A1 would be listed as A1_.

The output file name also needs ot be provded in the yaml file.

"""

import pandas as pd
import yaml
import sys

# Read in DLS data
data = pd.read_csv(sys.argv[1])

# Get rid of first point from each column since this is anomalous
data = data[1:]

# Get list of wells from yaml file
parameters = yaml.load(open(sys.argv[2],'r'))
wells = parameters['Wells']

# Get list of well names with temperatures from the dataframe
trimmed_wells = []
for well in wells:
    trimmed_wells = trimmed_wells + [col for col in data.columns if well in col]

# Generate trimmed DLS dataset and concatenate with the experimental time from
# the original DLS dataset
trimmed_data = data[trimmed_wells]
trimmed_data = pd.concat([data[data.columns[0]], trimmed_data], axis=1)

# Write trimmed DLS data file to new spreadsheet file
trimmed_data.to_csv(parameters['Outname'])

    

