import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import env
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

def get_connection(db, username=env.username, host=env.host, password=env.password):
    return f'mysql+pymysql://{username}:{password}@{host}/{db}'
    
sql_query = '''
SELECT * FROM mall_customers.customers;
'''
def get_mall_data():
    df = pd.read_sql(sql_query, get_connection('mall_customers'))
    return df

def split_data(df):
    train_validate, test = train_test_split(df,test_size=0.2, random_state=123)
    train, validate = train_test_split(train_validate,test_size=0.3, random_state=123)
    
    return train, validate, test

def get_dummy(df):
    mall_df_dummy = pd.get_dummies(df['gender'], drop_first=True)
    df = pd.concat([df, mall_df_dummy], axis=1)
    df = df.drop(columns='gender')
    return df

def scale_mall_data(df):
    mms = MinMaxScaler()
    mms.fit(df[['age','annual_income','spending_score']])
    df[['age','annual_income','spending_score']] =\
    mms.transform(df[['age','annual_income','spending_score']])  
    return df