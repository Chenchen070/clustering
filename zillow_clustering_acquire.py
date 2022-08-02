import pandas as pd
import env

def get_connection(db, username=env.username, host=env.host, password=env.password):
    return f'mysql+pymysql://{username}:{password}@{host}/{db}'
    
sql_query = '''
SELECT * FROM properties_2017
JOIN predictions_2017 USING (parcelid)
WHERE transactiondate < '2018'
AND propertylandusetypeid = 261
AND longitude IS NOT NULL
AND latitude IS NOT NULL
'''

def get_zillow_data():
    df = pd.read_sql(sql_query, get_connection('zillow'))
    return df

def drop_duplicate_zillow(df):
    df = df.sort_values('transactiondate').drop_duplicates('parcelid',keep='last')
    return df

def summarize_zillow(df):
    
    print('SUMMARY REPORT')
    print('=====================================================\n\n')
    print('Dataframe head: ')
    print(df.head(3))
    print('=====================================================\n\n')
    print('Dataframe info: ')
    print(df.info())
    print('=====================================================\n\n')
    print('Dataframe Description: ')
    print(df.describe())
    
    num_cols = [col for col in df.columns if df[col].dtype != 'O']
    cat_cols = [col for col in df.columns if col not in num_cols]
    print('=====================================================')
    print('DataFrame value counts: ')
    for col in df.columns:
        if col in cat_cols:
            print(df[col].value_counts(), '\n')
        else:
            print(df[col].value_counts(bins=10, sort=False), '\n')