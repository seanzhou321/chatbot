from importlib import resources
from pathlib import Path
import sqlite3
import yaml
import pandas as pd
import typing

RESOURCE_ROOT = "crm_chatbot.resources"

class ResourceLoader:
    """
    Modern resource loading using importlib.resources.
    Supports Python 3.7+ with backward compatibility.
    """
    
    @staticmethod
    def read_text_resource(
        resource_name: str,
        package: str = RESOURCE_ROOT, 
    ) -> str:
        """
        Read a text resource file using importlib.resources.
        
        Args:
            package: Package name containing the resource (e.g., 'crm_chatbot.resources')
            resource_name: Name of the resource file
            
        Returns:
            Content of the text file as string
        """
        try:
            # Modern approach (Python 3.9+)
            with resources.files(package).joinpath(resource_name).open('r') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading resource file: {e}")
            # Fallback for older Python versions
            return resources.read_text(package, resource_name)

    @staticmethod
    def get_resource_path(
        resource_name: str,
        package: str = RESOURCE_ROOT, 
    ) -> Path:
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
    def load_yaml_config(
        config_name: str,
        package: str = RESOURCE_ROOT, 
    ) -> dict:
        """
        Load a YAML configuration file from resources.
        
        Args:
            package: Package name containing the resource
            config_name: Name of the YAML file
            
        Returns:
            Dictionary containing the YAML data
        """
        content = ResourceLoader.read_text_resource(config_name, package)
        return yaml.safe_load(content)

    @staticmethod
    def load_csv_data(
        csv_name: str,
        package: str = RESOURCE_ROOT, 
    ) -> pd.DataFrame:
        """
        Load a CSV file from resources into a pandas DataFrame.
        
        Args:
            package: Package name containing the resource
            csv_name: Name of the CSV file
            
        Returns:
            Pandas DataFrame containing the CSV data
        """
        path = ResourceLoader.get_resource_path(csv_name, package)
        return pd.read_csv(path)

    @staticmethod
    def load_sqlite_data(
        db_name: str, 
        query:str,
        package: str = RESOURCE_ROOT, 
    ) -> pd.DataFrame:
        """
        Load data from a SQLite database.
        
        Args:
            db_name (str): Name of the SQLite database file
            query (str): SQL query to execute
        
        Returns:
            pandas.DataFrame: Query results
        """

        db_path = ResourceLoader.get_resource_path(db_name, package)

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
    def list_resources(package: str = RESOURCE_ROOT) -> typing.List[str]:
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
    def resource_exists(
        resource_name: str,
        package: str = RESOURCE_ROOT, 
    ) -> bool:
        """
        Check if a resource exists in the package.
        
        Args:
            package: Package name containing the resource
            resource_name: Name of the resource to check
            
        Returns:
            True if resource exists, False otherwise
        """
        try:
            return resources.files(package).joinpath(resource_name).is_file()
        except FileNotFoundError:
            return False


# Example usage
def main():
    """Example usage of ResourceLoader."""
    
    loader = ResourceLoader()
    PACKAGE = "crm_chatbot.resources"
    TEMPLATE_PACKAGE = "crm_chatbot.resources.templates"

    # List available resources
    print("Available resources:")
    resources = loader.list_resources(PACKAGE)
    for resource in resources:
        print(f"- {resource}")

    # Read travel2 from SQLite data
    try:
        print("\n")
        db = loader.load_sqlite_data("travel2.sqlite", "select * from aircrafts_data LIMIT 3", PACKAGE)
        print("\nSTravel2 sqlite:", db.head())
    except Exception as e:
        print(f"Error loading SQL: {e}")


if __name__ == "__main__":
    main()