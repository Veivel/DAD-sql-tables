# yes this is a python file

import subprocess
import pandas as pd
import os
from pathlib import Path

#### VARIABLES ####

# target_xlsx = 'testcases/employees_all.xlsx'
target_xlsx = input("Path of target xlsx file: ")
delim = ';'
content = '''
FirstName VARCHAR(64),
LastName VARCHAR(64),
Salary INT,
Department VARCHAR(128)'''

###################

print("csv delimiter: ", delim)
print("table schema: ", content)
proceed = input("Do you want to continue? (Y/n) ")

if proceed.lower() != "y":
    exit(0)

df_arr = pd.read_excel(target_xlsx, None)
for sheet_name in df_arr:
    df = df_arr[sheet_name]
    
    print(f"\n======== ======== {sheet_name} ======== ========")
    print(df)
    
    # create the table
    print(subprocess.Popen(
            f'psql -d das_test_db -c "CREATE TABLE {sheet_name} ({content});"', 
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
            f'''psql -d das_test_db -c "copy {sheet_name} from '{absolute}/temp.csv' delimiter '{delim}' csv header;"''', 
            stdout=subprocess.PIPE, 
            shell=True, 
            universal_newlines=True
        ).stdout.read()
    )