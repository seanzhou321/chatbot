# fetch sample travel data from internet

import os
import shutil
import requests

from crm_chatbot.resource_loader import ResourceLoader, RESOURCE_ROOT
local_file = ResourceLoader.get_resource_path("travel2.sqlite")
# The backup lets us restart for each tutorial section
backup_file = ResourceLoader.get_resource_path("travel2.backup.sqlite")

db_url = "https://storage.googleapis.com/benchmarks-artifacts/travel-db/travel2.sqlite"
overwrite = False
if overwrite or not local_file.exists():
    print("fetching the local file.")
    response = requests.get(db_url)
    response.raise_for_status()  # Ensure the request was successful
    with open(local_file, "wb") as f:
        f.write(response.content)

if not backup_file.exists() :
    # Backup - we will use this to "reset" our DB in each section
    print("make a back up of the local file.")
    shutil.copy(local_file, backup_file)
