# yes this is a python file

import subprocess
import pandas as pd
import os
from pathlib import Path

preset_schemas = {
    'countries': '''Country VARCHAR(128), Population INT''',
    'employees': '''FirstName VARCHAR(64),LastName VARCHAR(64),Salary INT,Department VARCHAR(128)'''
}


#### VARIABLES ####

# target_xlsx = 'testcases/employees_all.xlsx'
user = input("\n-> PSQL role name: ")
target_xlsx = input("-> Path of target xlsx file: ")
delim = ';'
content = input("-> table schema (raw from backend, or preset if exist): ")
DROP_FIRST = True

###################

print("-> CSV delimiter: ", delim)
print("-> Table schema: ", content)
proceed = input("Do you want to continue? (Y/n) ")

if proceed.lower() != "y":
    exit(0)
    
psql_config = f"psql -U {user} -d das_test_db -c"

df_arr = pd.read_excel(target_xlsx, None)
for sheet_name in df_arr:
    df = df_arr[sheet_name]
    
    print(f"\n======== ======== {sheet_name} ======== ========")
    print(df)
    
    # drop the table ()
    if DROP_FIRST:
        print(subprocess.Popen(
                f'{psql_config} "DROP TABLE {sheet_name};"', 
                stdout=subprocess.PIPE, 
                shell=True, 
                universal_newlines=True
            ).stdout.read()
        )
    
    # create the table
    print(subprocess.Popen(
            f'{psql_config} "CREATE TABLE {sheet_name} ({content});"', 
            stdout=subprocess.PIPE, 
            shell=True, 
            universal_newlines=True
        ).stdout.read()
    )
    
    # export sheet to temporary csv
    relative = Path(".")
    absolute = os.path.abspath(relative)  # absolute is a str object
    df.to_csv(f"temp.csv", sep=delim, index=False)
    
    # import csv into newly-created table
    print(subprocess.Popen(
            f'''{psql_config} "copy {sheet_name} from '{absolute}/temp.csv' delimiter '{delim}' csv header;"''', 
            stdout=subprocess.PIPE, 
            shell=True, 
            universal_newlines=True
        ).stdout.read()
    )