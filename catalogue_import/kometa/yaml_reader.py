from pathlib import Path

import yaml

class UniqueKeyLoader(yaml.SafeLoader):
    """
    Extends PyYAML's SafeLoader to add protection
    against duplicate mapping keys.
    """
 
    def construct_mapping(self, node, deep=False):
        """
        Convert a YAML mapping into a Python dictionary.

        Checks mapping keys so duplicate keys can be rejected.
        """   
        
        # Expand YAML merge keys before checking the mapping.
        self.flatten_mapping(node)
        
        # Create an empty dictionary to store the mapping.
        mapping = {}
        
        # Process each key-value pair in the YAML mapping.
        for key_node, value_node in node.value:
            # Convert the YAML key into a Python object.
            key = self.construct_object(key_node, deep=deep) 
            # Check that the key can be used in a dictionary.
            try:
                hash(key)
            except TypeError as error:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    "found an unhashable key",
                    key_node.start_mark,
                ) from error
                
            # Reject a key if it already exists in the dictionary.
            if key in mapping:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    f"found duplicate key {key!r}",
                    key_node.start_mark,
                )
                
            # Convert the YAML value into a Python object.
            value = self.construct_object(value_node, deep=deep)
            # Store the key and value in the dictionary.
            mapping[key] = value
            
        # Return the completed dictionary to PyYAML.
        return mapping
        

def load_yaml(file_path):
    """
    Load a YAML file and return its contents as Python data.

    Args:
        file_path: Path to the YAML source file.

    Returns:
        The parsed YAML contents as Python dictionaries,
        lists and other basic data types.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        yaml.YAMLError: If the YAML content is invalid.
        ValueError: If the YAML file is empty.
    """

    # Convert the supplied path into a Path object.
    file_path = Path(file_path)

    # Open the YAML file using UTF-8 text encoding.
    with file_path.open("r", encoding="utf-8") as yaml_file:

        # Safely parse the YAML into Python data.
        data = yaml.load(yaml_file, Loader=UniqueKeyLoader)

        # An empty YAML file produces None.
        # Reject it because the importer needs actual source data.
        if data is None:
            raise ValueError("The YAML file is empty.")

        # Return the parsed data for further processing.
        return data