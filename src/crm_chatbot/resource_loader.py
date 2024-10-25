

from importlib import resources
from pathlib import Path
import sqlite3
import yaml
import pandas as pd
import typing

class ResourceLoader:
    """
    Modern resource loading using importlib.resources.
    Supports Python 3.7+ with backward compatibility.
    """
    

    @staticmethod
    def get_resource_path(package: str, resource_name: str) -> Path:
        """
        Get the path to a resource file.
        
        Args:
            package: Package name containing the resource
            resource_name: Name of the resource file
            
        Returns:
            Path object pointing to the resource
        """
        try:
            # Modern approach (Python 3.9+)
            return resources.files(package).joinpath(resource_name)
        except Exception:
            # Fallback for older Python versions
            with resources.path(package, resource_name) as path:
                return path

    @staticmethod
    def load_yaml_config(package: str, config_name: str) -> dict:
        """
        Load a YAML configuration file from resources.
        
        Args:
            package: Package name containing the resource
            config_name: Name of the YAML file
            
        Returns:
            Dictionary containing the YAML data
        """
        content = ResourceLoader.read_text_resource(package, config_name)
        return yaml.safe_load(content)

    @staticmethod
    def load_csv_data(package: str, csv_name: str) -> pd.DataFrame:
        """
        Load a CSV file from resources into a pandas DataFrame.
        
        Args:
            package: Package name containing the resource
            csv_name: Name of the CSV file
            
        Returns:
            Pandas DataFrame containing the CSV data
        """
        path = ResourceLoader.get_resource_path(package, csv_name)
        return pd.read_csv(path)

    @staticmethod
    def load_sqlite_data(package: str, db_name: str, query:str) -> pd.DataFrame:
        """
        Load data from a SQLite database.
        
        Args:
            db_name (str): Name of the SQLite database file
            query (str): SQL query to execute
        
        Returns:
            pandas.DataFrame: Query results
        """

        db_path = ResourceLoader.get_resource_path(package, db_name)

        try:
            conn = sqlite3.connect(db_path)
            df = pd.read_sql_query(query, conn)
            conn.close()
            print(f"Successfully executed query, returned {len(df)} rows")
            return df
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        
    @staticmethod
    def list_resources(package: str) -> typing.List[str]:
        """
        List all resources in a package.
        
        Args:
            package: Package name to inspect
            
        Returns:
            List of resource names in the package
        """
        try:
            # Modern approach (Python 3.9+)
            return [
                resource.name
                for resource in resources.files(package).iterdir()
                if resource.is_file()
            ]
        except Exception:
            # Fallback for older Python versions
            return list(
                resources.files(package))

    @staticmethod
    def resource_exists(package: str, resource_name: str) -> bool:
        """
        Check if a resource exists in the package.
        
        Args:
            package: Package name containing the resource
            resource_name: Name of the resource to check
            
        Returns:
            True if resource exists, False otherwise
        """
        try:
            with resources.path(package, resource_name):
                return True
        except FileNotFoundError:
            return False


# Example usage
def main():
    """Example usage of ResourceLoader."""
    
    loader = ResourceLoader()
    PACKAGE = "sample_project.resources"
    TEMPLATE_PACKAGE = "sample_project.resources.templates"

    # List available resources
    print("Available resources:")
    resources = loader.list_resources(PACKAGE)
    for resource in resources:
        print(f"- {resource}")

    # Load YAML configuration
    try:
        config = loader.load_yaml_config(PACKAGE, "config.yaml")
        print("\nConfiguration loaded:", config)
    except Exception as e:
        print(f"Error loading config: {e}")

    # Load CSV data
    try:
        df = loader.load_csv_data(PACKAGE, "data.csv")
        print("\nData preview:\n", df.head())
    except Exception as e:
        print(f"Error loading CSV: {e}")

    # Read SQL queries
    try:
        queries = loader.read_text_resource(PACKAGE, "queries.sql")
        print("\nSQL Queries:", queries)
    except Exception as e:
        print(f"Error loading SQL: {e}")

    # Load email template
    try:
        template = loader.read_text_resource(TEMPLATE_PACKAGE, "email_template.html")
        print("\nEmail template:", template[:100])
    except Exception as e:
        print(f"Error loading template: {e}")

    # Check if resources exist
    resources_to_check = ["config.yaml", "nonexistent.txt"]
    for resource in resources_to_check:
        exists = loader.resource_exists(PACKAGE, resource)
        print(f"\nResource '{resource}' exists: {exists}")

    # Read travel2 from SQLite data
    try:
        print("\n")
        db = loader.load_sqlite_data(PACKAGE, "travel2.sqlite", "select * from aircrafts_data LIMIT 3")
        print("\nSTravel2 sqlite:", db.head())
    except Exception as e:
        print(f"Error loading SQL: {e}")


if __name__ == "__main__":
    main()