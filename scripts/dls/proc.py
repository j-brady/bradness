#!/usr/bin/env python3

"""Fit DLS data
   
    Usage:
        proc.py <data.csv> <conf.yml>

    Description:
        
        Script fits DLS data from Wyatt DynaProIII and outputs data as a csv file using pandas dataframes.

        The conf.yml file should contain the delimiter used to separate columns in the input data file


            delimiter: ','


        for example would mean you are using commas
"""
from pathlib import Path
import yaml
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from docopt import docopt

from dls.dls import DLS, stokes_einstein, viscosity, q

if __name__=="__main__":
    args = docopt(__doc__)
    data_path = args.get("<data.csv>")
    data_path = Path(data_path)
    params = yaml.load(open(args.get("<conf.yml>"),'r'))
    mod = DLS(mu_2=True)

    if params.get("delimiter"):
        delimiter = params.get("delimiter")
    else:
        delimiter = ","
    data = pd.read_csv(data_path, delimiter=delimiter)
    print(data)
    data = data.dropna(axis=1)
    print(data)

    columns = data.columns[1:-1]
    print(columns)

    data = data[data["Time (µs)"]>0.2]
    data["t"] = data["Time (µs)"] / 1e6

    cols = params.get("wells",columns)
    print(cols)
    params = ['D','D_err','B','B_err','beta','beta_err','mu_2', 'mu_2_err']#, 'Gamma', 'PD']

    fits = {param:[] for param in params}
    fits['col'] = []

    for col in cols:
        try:
            out = mod.g.fit(data[col],t=data['t'],params=mod.pars)
    #        plt.semilogx(data['t'],data[col],label=col)
    #        plt.semilogx(data['t'],out.best_fit,'k--')
            hashes = "####################################"
            print(f"{hashes}\n{col}\n{hashes}")
            print(out.fit_report())
            print(mod.pars)
            for k,v in out.params.items():
                fits[k].append(v.value)
                fits[k+"_err"].append(v.stderr)

            fits['col'].append(col)
        #    fits[col].append()
        except:
            print(f"""

            #########################################
            Skipping {col}
            #########################################
            
            """)

    print(fits)
    df = pd.DataFrame(fits)
    df["Gamma"] = df['D'] * q() ** 2.
    df["PD"] = df['mu_2'] / df['Gamma'] ** 2.
    df["Rh"] = stokes_einstein(df['D'], viscosity(298.15),298.15) 
    df["Rh_err"] = df["D_err"] * (df["Rh"] / df["D"]) 
    print(df)
    df.to_csv(f"{data_path.stem}_fits.csv",float_format="%.2e",index=False)
    #print(np.sqrt((30542962.5/(3.3e-11*q()**2)**2)))

#    plt.xlabel("s")
#    plt.legend()
#    plt.tight_layout()
#    plt.savefig(f"{data_path.stem}.svg")
#    plt.show()



