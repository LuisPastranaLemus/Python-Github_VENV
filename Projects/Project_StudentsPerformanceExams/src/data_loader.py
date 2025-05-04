# Data loader for Data Analysis

import pandas as pd
import os

def load_csv(path, sep=',', encoding='utf-8', header='infer', keep_default_na=False):
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"*** Error *** \nFile not found: {path}.")
        print("\nThis is your current", os.getcwd())
    
    df = pd.read_csv(path, sep=sep, encoding=encoding, header=header, keep_default_na=keep_default_na)
    
    return df

def load_excel(path, sheet_name=0):

    if not os.path.exists(path):
        raise FileNotFoundError(f"*** Error *** \nFile not found: {path}.")
        print("\nThis is your current", os.getcwd())

    df = pd.read_excel(path, sheet_name=sheet_name, header='infer', keep_default_na=False)
    return df

def load_list(list ):
    
    df = pd.DataFrame(list)
    
    return df 

def load_dict(dict ):
    
    df = pd.DataFrame.from_dict(dict, orient='columns')
    
    return df