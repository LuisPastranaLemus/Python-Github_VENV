# Data cleaning for Data Analysis

import pandas as pd
import unicodedata
from pandas.api.types import is_integer_dtype, is_float_dtype, is_string_dtype
from tqdm import tqdm
import re
import numpy as np

# Function to assign <NA> value to missing values ​​in a DataFrame
def missing_values(df, exclude=None):
    
    if exclude is None:
        exclude = []
    
    null_values = ['', ' ', '-', 'N/A', 'n/a', 'NA', 'na', 'NaN', 'nan', 'NULL', 'null', 'None', None]
    
    for column in df.columns:
        
        if column in exclude:
            continue 
        
        df[column] = df[column].replace(null_values, pd.NA)
                
    return df

def normalize_columns_header(df):
    
    df.columns = df.columns.str.replace('/', '_')
    df.columns = df.columns.str.replace('-', '_')
    df.columns = df.columns.str.replace(r'__+', '_', regex=True)
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.strip()
    
    return df
    
# Function to standardize string values format(snake_case, lower, strip, removal of hyphens)
def normalize_string(df, exclude=None):
    
    if exclude is None:
        exclude = []
    
    def normalize_str(text):
        return unicodedata.normalize('NFKD', str(text)).encode('ASCII', 'ignore').decode('utf-8')
        
    for column in df.columns:
        
        if column in exclude:
            continue 
            
        if df[column].dtype == 'object':
            
            df[column] = df[column].astype(str).apply(normalize_str)
            df[column] = df[column].str.replace('/', '_')
            df[column] = df[column].str.replace('-', '_')
            df[column] = df[column].str.replace(r'__+', '_', regex=True)
            df[column] = df[column].str.replace(' ', '_')
            df[column] = df[column].str.lower()
            df[column] = df[column].str.strip()
                
    return df

# Function to remove explicit duplicates
def drop_explicit_duplicates(df):

    df = df.drop_duplicates().reset_index(drop=True)
    
    return df

# Function for replacing string numeric values with numeric values
def replace_string_numeric_values_numeric(df, include=None,exclude=None):
    
    if exclude is None:
        exclude = []
    
    if include is None:
        available_columns = [col for col in df.columns if col not in exclude]
    else:
        available_columns = [col for col in include if col not in exclude]
    
    for column in available_columns:
        
        if df[column].dtype == 'object':
                
            df[column] = df[column].str.replace(',', '', regex=False)   
            
        # Convert to numeric, forcing errors to NaN
        if df[column].str.isdigit().all():
                
            if np.array_equal(df[column], df[column].astype('int')):
                df[column] = pd.to_numeric(df[column], errors='coerce').astype('Int64')
                
        elif df[column].apply(lambda x: x.replace('.', '', 1).isdigit() if isinstance(x, str) else False).all():
                
            if np.array_equal(df[column], df[column].astype('float')):
                df[column] = pd.to_numeric(df[column], errors='coerce').astype('Float64')
            
    return df

# Function to fill missing numeric values with "0"
def replace_missing_numeric_values_zero(df, include=None, exclude=None):
    
    if exclude is None:
        exclude = []
    
    if include is None:
        available_columns = [col for col in df.columns if col not in exclude]
    else:
        available_columns = [col for col in include if col not in exclude]
    
    for column in available_columns:
        
        if is_integer_dtype(df[column]):
            
            df[column] = df[column].fillna(0)
        
        elif is_float_dtype(df[column]):
            
            df[column] = df[column].fillna(0.0)
            
    return df

# Function to fill missing numeric values with "mean"
def replace_missing_numeric_values_mean(df, include=None, exclude=None):
    
    if exclude is None:
        exclude = []
    
    if include is None:
        available_columns = [col for col in df.columns if col not in exclude]
    else:
        available_columns = [col for col in include if col not in exclude]
    
    for column in available_columns:
        
        if is_integer_dtype(df[column]):
            
            mean = round(df[column].mean())
            df[column] = df[column].fillna(mean)
        
        elif is_float_dtype(df[column]):
            
            mean = df[column].mean()
            df[column] = df[column].fillna(mean).apply(lambda x: float(f"{x:.2f}")) 
            
    return df

# Function to fill missing numeric values with "median"
def replace_missing_numeric_values_median(df, include=None, exclude=None):
    
    if exclude is None:
        exclude = []
    
    if include is None:
        available_columns = [col for col in df.columns if col not in exclude]
    else:
        available_columns = [col for col in include if col not in exclude]
    
    for column in available_columns:
        
        if is_integer_dtype(df[column]):
            
            median = round(df[column].median())
            df[column] = df[column].fillna(median)
        
        elif is_float_dtype(df[column]):
            
            median = df[column].median()
            df[column] = df[column].fillna(median).apply(lambda x: float(f"{x:.2f}")) 
            
    return df
               
# Function for replacing string missing values, default "unknown"
def replace_missing_string_values(df, include=None, exclude=None, mssng_value='unknown'):   
    
    if exclude is None:
        exclude = []

    if include is None:
        available_columns = [col for col in df.columns if col not in exclude]
    else:
        available_columns = [col for col in include if col not in exclude]
    
    for column in available_columns:     
    
        if df[column].dtype == 'object':
        
            df[column] = df[column].fillna(mssng_value)
    
    return df

# Function for replacing string date values to datetime values

def replace_string_datetime_values_datetime(df, include=None, exclude=None, frmt=None, time_zone='UTC'):
    
    if exclude is None:
        exclude = []
    
    if include is None:
        available_columns = [col for col in df.columns if col not in exclude]
    else:
        available_columns = [col for col in include if col not in exclude]
    
    for column in available_columns:
        
        df[column] = pd.to_datetime(df[column], format=frmt, errors='coerce')
        
        try:
            
            df[column] = df[column].dt.tz_localize(time_zone)
        
        except TypeError:
            
            df[column] = df[column].dt.tz_convert(time_zone)
    
    return df
 
 # Function for unique values
def detect_unique_values(df, include=None, exclude=None):
     
    unique_dictionary = {}
     
    if exclude is None:
        exclude = []
        
    if include is None:
        available_columns = [col for col in df.columns if col not in exclude]
    else:
        available_columns = [col for col in include if col not in exclude]
     
    for column in available_columns:
        
        unique_dictionary[column] = df[column].unique()
    
    return unique_dictionary
        
        
# Function for implicit duplicates
def detect_implicit_duplicates(df, include=None, exclude=None):
    
    if exclude is None:
        exclude = []
    
    if include is None:
        available_columns = [col for col in df.columns if col not in exclude]
    else:
        available_columns = [col for col in include if col not in exclude]
    
    for column in available_columns:
        
        if column in exclude:
            continue  
        
        if df[column].dtype != 'object':
            continue
        
        column_values = df[column]
        column_values = column_values[column_values != '']
        column_values = column_values[column_values.apply(lambda x: len(re.split(r"[ \-\_']", x)) == 1)]

        # 2. Get base unique values
        base_unique_values = column_values.unique().tolist()
        if not base_unique_values:
            continue

        print(f"\nColumn: '{column}'")

        # 3. Compare base unique values against all Column's values
        for base in tqdm(base_unique_values, desc=f"Searching implicit values for: '{column}'"):
            pattern = re.compile(re.escape(base), re.IGNORECASE)

            matches = [val for val in column_values if val != base and pattern.search(val)]

            if matches:
                print(f"  '{base}' → {matches}")
