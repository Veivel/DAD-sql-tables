## Preparation

1. pull image of postgres:14.6
2. execute/open container (`docker exec -it <container name> <runtime>`)

## Usage

1. apt-get install git
2. git pull <repository>
3. apt-get install python3 python3-pandas
4. python3 xlsx-to-table.py

-----

## Basic Workflow

1. Create testcase tables in xlsx form
2. push (upload)
3. pull inside container running db (download)
4. run xlsx-to-table

