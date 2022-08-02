import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

def drop_duplicate_zillow(df):
    df = df.sort_values('transactiondate').drop_duplicates('parcelid',keep='last')
    return df

def nulls_by_col(df):
    num_missing = df.isnull().sum()
    rows = df.shape[0]
    prcnt_miss = num_missing / rows * 100
    cols_missing = pd.DataFrame({'num_rows_missing': num_missing, 'percent_rows_missing': prcnt_miss})
    return cols_missing.sort_values(by='num_rows_missing', ascending=False)

def nulls_by_row(df):
    num_missing = df.isnull().sum(axis=1)
    prcnt_miss = num_missing / df.shape[1] * 100
    rows_missing = pd.DataFrame({'num_cols_missing': num_missing, 'percent_cols_missing': prcnt_miss})
    rows_missing = df.merge(rows_missing,
                        left_index=True,
                        right_index=True)[['parcelid', 'num_cols_missing', 'percent_cols_missing']]
    return rows_missing.sort_values(by='num_cols_missing', ascending=False)

def remove_columns(df, cols_to_remove):
    df = df.drop(columns=cols_to_remove)
    return df

def handle_missing_values(df, prop_required_columns=0.6, prop_required_row=0.75):
    threshold = int(round(prop_required_columns * len(df.index), 0))
    df = df.dropna(axis=1, thresh=threshold)
    threshold = int(round(prop_required_row * len(df.columns), 0))
    df = df.dropna(axis=0, thresh=threshold)
    return df

def data_prep(df, cols_to_remove=[], prop_required_column=0.6, prop_required_row=0.75):
    df = remove_columns(df, cols_to_remove)
    df = handle_missing_values(df, prop_required_column, prop_required_row)
    return df

def split_data(df):
    train_validate, test = train_test_split(df,test_size=0.2, random_state=123)
    train, validate = train_test_split(train_validate,test_size=0.3, random_state=123)
    
    return train, validate, test

def value_counts(col):
    return col.value_counts()

def impute_missing_value_zillow(df):
    df['buildingqualitytypeid'] = df.buildingqualitytypeid.fillna(df.buildingqualitytypeid.mean())
    df['unitcnt'] = df.unitcnt.fillna(df.unitcnt.mode()[0])
    df['propertyzoningdesc'] = df.propertyzoningdesc.fillna(df.propertyzoningdesc.mode()[0])
    df['heatingorsystemtypeid'] = df.heatingorsystemtypeid.fillna(df.heatingorsystemtypeid.mode()[0])
    df.dropna(inplace=True)
    return df