import re

import numpy as np
from langchain_core.tools import tool
import requests

from crm_chatbot.resource_loader import ResourceLoader

overwrite = False
local_file = ResourceLoader.get_resource_path("swiss_faq.md")
if overwrite or not local_file.exists(): 
    response = requests.get(
        "https://storage.googleapis.com/benchmarks-artifacts/travel-db/swiss_faq.md"
    )
    response.raise_for_status()
    faq_text = response.text

    with open(local_file, "w", encoding="utf-8") as f:
        f.write(faq_text)
        print(f"{local_file}  is created.")