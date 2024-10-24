# setup.py
# to install 
# Install in development mode ```(venv) ...\chatbot> pip install -e .````
# Install as regular package ```(venv) ...\chatbot> pip install .````
# Install with additional dependencies  ```(venv) ...\chatbot> pip install -e .[dev, docs]````

# upgrade ```(venv) ...\chatbot> pip install -e . --upgrade````

from setuptools import setup, find_packages

setup(
    name="crm_chatbot",
    version="0.1.0",
    package_dir={"": "src"},
    python_requires=">=3.12.7",
    install_requires=[
        'ollama', 
        'pandas',
        'langgraph',
        'langchain',
    ],
    extras_require={
        'dev': [
            'pytest'
            'flake8'
            'black'
        ],
        'docs': [
            'sphinx'
        ]
    },
    packages=find_packages(where="src"),
    package_data={
        "tools":['data/travel2.sqlite'],
    },
    include_package_data=True,
)
