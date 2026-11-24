
"""
Tests for the Kometa YAML Reader.

These tests verify that YAML source files can be read safely
and converted into Python data structures.
"""

import tempfile
import yaml
from pathlib import Path

from django.test import SimpleTestCase

from catalogue_import.kometa.yaml_reader import load_yaml


class TestLoadYaml(SimpleTestCase):
    """
    Tests the load_yaml function.
    """

    def test_load_valid_yaml(self):
        """
        A valid YAML file should return the expected Python dictionary.
        """

        # Create a temporary directory for our test file.
        with tempfile.TemporaryDirectory() as temporary_directory:

            # Build the path for a temporary YAML file.
            yaml_path = Path(temporary_directory) / "test.yml"

            # Write a small YAML example into the file.
            yaml_path.write_text(
                "collections:\n"
                "  LGBTQ Films:\n"
                "    imdb_id:\n"
                "      - tt0112471\n",
                encoding="utf-8",
            )

            # Read the YAML file using our function.
            result = load_yaml(yaml_path)

            # Define the Python data we expect to receive.
            expected = {
                "collections": {
                    "LGBTQ Films": {
                        "imdb_id": ["tt0112471"]
                    }
                }
            }

            # Check that the returned data matches our expectation.
            self.assertEqual(result, expected)


    def test_load_missing_file(self):
        """
        A missing YAML file should raise FileNotFoundError.
        """

        # Create a temporary directory without creating a YAML file.
        with tempfile.TemporaryDirectory() as temporary_directory:

            # Define the path of a file that does not exist.
            yaml_path = Path(temporary_directory) / "missing.yml"

            # Check that attempting to read it raises the expected error.
            with self.assertRaises(FileNotFoundError):
                load_yaml(yaml_path)

    
    def test_load_invalid_yaml(self):
        """
        Invalid YAML should raise a yaml.YAMLError.
        """

        # Create a temporary directory for our test file.
        with tempfile.TemporaryDirectory() as temporary_directory:

            # Build the path for a temporary YAML file.
            yaml_path = Path(temporary_directory) / "invalid.yml"

            # Write deliberately malformed YAML into the file.
            yaml_path.write_text(
                "collections:\n"
                "  LGBTQ Films:\n"
                "    imdb_id:\n"
                "      - tt0112471\n"
                "     - tt0109045\n",
                encoding="utf-8",
            )

            # Check that the invalid YAML raises a parsing error.
            with self.assertRaises(yaml.YAMLError):
                load_yaml(yaml_path)

    def test_load_empty_yaml(self):
        """
        An empty YAML file should raise a clear ValueError.
        """

        # Create a temporary directory for our test file.
        with tempfile.TemporaryDirectory() as temporary_directory:

            # Build the path for an empty YAML file.
            yaml_path = Path(temporary_directory) / "empty.yml"

            # Create an empty file.
            yaml_path.write_text("", encoding="utf-8")

            # Check that loading an empty file raises ValueError.
            with self.assertRaises(ValueError):
                load_yaml(yaml_path)


    def test_load_duplicate_keys(self):
        """
        Duplicate YAML keys should raise a yaml.YAMLError.
        """

        # Create a temporary directory for our test file.
        with tempfile.TemporaryDirectory() as temporary_directory:

            # Build the path for a temporary YAML file.
            yaml_path = Path(temporary_directory) / "duplicate.yml"

            # Write YAML containing a duplicate key.
            yaml_path.write_text(
                "collections:\n"
                "  LGBTQ Films:\n"
                "    summary: First description\n"
                "    summary: Second description\n",
                encoding="utf-8",
            )

            # Duplicate keys should not be silently accepted.
            with self.assertRaises(yaml.YAMLError):
                load_yaml(yaml_path)