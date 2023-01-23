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

db_name = "das_test_db"
db_user = "test"
db_password = "" # no need
delim = ';'

target_xlsx = input("-> path of target XLSX file: ")
schema = ""
schema_name = input("-> preset schema (empty if none):")
if schema_name == "":
    schema = input("-> raw table schema: ")
else:
    schema = preset_schemas[schema_name]
DROP_FIRST = True

###################

print("-> CSV delimiter: ", delim)
print("-> Table schema: ", schema)
proceed = input("Do you want to continue? (Y/n) ")

if proceed.lower() != "y":
    exit(0)
    
psql_config = f"psql -U {db_user} -d {db_name} -c"

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
            f'{psql_config} "CREATE TABLE {sheet_name} ({schema});"', 
            stdout=subprocess.PIPE, 
            shell=True, 
            universal_newlines=True
        ).stdout.read()
    )
    
    # export sheet to temporary csv
    relative = Path(".")
    absolute = os.path.abspath(relative)  # absolute is a str object
    temp_csv_filename = f"temp_{sheet_name}"
    df.to_csv(f"{temp_csv_filename}.csv", sep=delim, index=False)
    
    # import csv into newly-created table
    print(subprocess.Popen(
            f'''{psql_config} "copy {sheet_name} from '{absolute}/{temp_csv_filename}.csv' delimiter '{delim}' csv header;"''', 
            stdout=subprocess.PIPE, 
            shell=True, 
            universal_newlines=True
        ).stdout.read()
    )