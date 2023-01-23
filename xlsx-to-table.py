# yes this is a python file

import subprocess
import pandas as pd
import os
from pathlib import Path

# formatnya presetName: [question_table_schema, ans_table_schema]
preset_schemas = {
    'countries' : (
        '''Country VARCHAR(128), Population INT''', 
        '''Country VARCHAR(128), Population INT'''
    ),
    'employees' : (
        '''FirstName VARCHAR(64), LastName VARCHAR(64),Salary INT,Department VARCHAR(128)''',
        '''FirstName VARCHAR(64), LastName VARCHAR(64),Salary INT,Department VARCHAR(128)'''
    ),
    'computer'  : (
        '''ComputerName VARCHAR(128), CostPerHour FLOAT(8), HoursToCompute FLOAT(8)''',
        '''ComputerName VARCHAR(128), TotalCost FLOAT(8)''',
    ),
}

#### VARIABLES ####

db_name = os.environ.get("db_name")
db_user = os.environ.get("db_user")
db_password = os.environ.get("db_password")
delim = os.environ.get("delimiter")

def main():
    # Get Input
    target_xlsx = input("-> path of target XLSX file: ")
    schema = ()
    print("presets available:", preset_schemas.keys())
    schema_name = input("-> preset schema (empty if none): ")
    if schema_name == "":
        schema[0] = input("-> question table schema: ")
        schema[1] = input("-> answer table schema: ")
    else:
        schema = preset_schemas[schema_name]
    DROP_FIRST = True
    
    # Confirmation
    print("CSV delimiter:", delim)
    print("Table schema:", schema)
    proceed = input("Do you want to continue? (Y/n): ")

    if proceed.lower() != "y":
        exit(0)
        
    # Setup Postgres CLI config
    psql_config = ""
    if db_password == "":
        psql_config = f"psql -U {db_user} -d {db_name} -c"
    else:
        psql_config = f"psql -U {db_user} -p {db_password} -d {db_name} -c"

    df_arr = pd.read_excel(target_xlsx, None)
    for sheet_name in df_arr:
        df = df_arr[sheet_name]
        df.dropna(axis=0, inplace=True)
        
        print(f"\n======== ======== {sheet_name} ======== ========")
        print(df)
        
        # drop the table
        if DROP_FIRST:
            print(subprocess.Popen(
                    f'{psql_config} "DROP TABLE {sheet_name};"', 
                    stdout=subprocess.PIPE, 
                    shell=True, 
                    universal_newlines=True
                ).stdout.read()
            )
        
        # select schema
        if "_ans" in sheet_name:
            curr_schema = schema[1]
        else:
            curr_schema = schema[0]
        
        # create the table
        print(subprocess.Popen(
                f'{psql_config} "CREATE TABLE {sheet_name} ({curr_schema});"', 
                stdout=subprocess.PIPE, 
                shell=True, 
                universal_newlines=True
            ).stdout.read()
        )
        
        # export sheet to temporary csv
        relative = Path(".")
        absolute = os.path.abspath(relative)  # absolute is a str object
        temp_csv_filename = f"temp/tmp_{sheet_name}"
        df.to_csv(f"{temp_csv_filename}.csv", sep=delim, index=False)
        
        # import csv into newly-created table
        print(subprocess.Popen(
                f'''{psql_config} "copy {sheet_name} from '{absolute}/{temp_csv_filename}.csv' delimiter '{delim}' csv header;"''', 
                stdout=subprocess.PIPE, 
                shell=True, 
                universal_newlines=True
            ).stdout.read()
        )
        
if __name__ == "__main__":
    main()