# fetch sample travel data from internet

import os
import shutil
import requests

db_url = "https://storage.googleapis.com/benchmarks-artifacts/travel-db/travel2.sqlite"
local_file = "travel2.sqlite"
# The backup lets us restart for each tutorial section
backup_file = "travel2.backup.sqlite"
overwrite = False
if overwrite or not os.path.exists(local_file):
    print("fetching the local file.")
    response = requests.get(db_url)
    response.raise_for_status()  # Ensure the request was successful
    with open(local_file, "wb") as f:
        f.write(response.content)

if not os.path.exists(backup_file) :
    # Backup - we will use this to "reset" our DB in each section
    print("make a back up of the local file.")
    shutil.copy(local_file, backup_file)
