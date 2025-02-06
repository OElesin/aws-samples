from pathlib import Path
import json
import re
from concurrent.futures import ThreadPoolExecutor
from typing import List, Iterator
import logging

def flatten_json(data):
    """
    Flatten a nested JSON structure into top-level key-value pairs.
    
    This function handles nested dictionaries and special keys with prefixes like '__prefix' and '__text'.
    It also manages list-type values, particularly for fields like 'title' and 'content'.
    
    Args:
        data (dict): The nested JSON dictionary to flatten
    
    Returns:
        dict: A flattened dictionary with top-level key-value pairs
    """
    # Initialize an empty dictionary to store flattened results
    flattened = {}
    
    # Iterate through each key-value pair in the input dictionary
    for key, value in data.items():
        # Handle special nested structures with '__prefix' and '__text'
        if isinstance(value, dict) and '__prefix' in value and '__text' in value:
            # Combine prefix and value into a single key
            flattened[f"{key}__{value['__prefix']}"] = value['__text']
        
        # Handle list values, particularly complex nested lists
        elif isinstance(value, list):
            if key == 'title':
                # For 'title', handle potential nested dictionary with prefix
                if isinstance(value[0], dict):
                    flattened[f"{key}__{value[0]['__prefix']}"] = value[0]['__text']
                else:
                    flattened[key] = remove_html_tags(value[0])
            
            elif key == 'content':
                # For 'content', handle list of dictionaries with media information
                for i, content_item in enumerate(value):
                    # Flatten nested media information
                    for media_key, media_value in content_item.items():
                        if media_key.startswith('_'):
                            # Use a numbered key to preserve multiple content items
                            flattened[f"{key}_{i}_{media_key}"] = media_value
                        elif media_key == 'player':
                            # Handle nested player information
                            flattened[f"{key}_{i}_player_url"] = media_value.get('_url')
        
        # Handle simple key-value pairs
        elif isinstance(value, (str, int, float, bool)):
            flattened[key] = remove_html_tags(value)
        
        # Handle nested dictionaries with specific prefixes
        elif isinstance(value, dict):
            for nested_key, nested_value in value.items():
                if nested_key.startswith('__'):
                    # Special handling for prefixed keys
                    flattened[f"{key}{nested_key}"] = remove_html_tags(nested_value)
    
    return flattened


def flatten_hbr_json(json_obj, parent_key='', sep='_'):
    """
    Recursively flattens a JSON object.

    :param json_obj: The JSON object (dict or list) to flatten.
    :param parent_key: The base key for recursion.
    :param sep: Separator for nested keys.
    :return: A flattened dictionary.
    """
    items = []
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            if isinstance(value, (dict, list)):
                items.extend(flatten_hbr_json(value, new_key, sep=sep).items())
            else:
                items.append((new_key, remove_html_tags(value)))
    elif isinstance(json_obj, list):
        for i, value in enumerate(json_obj):
            new_key = f"{parent_key}{sep}{i}" if parent_key else str(i)
            if isinstance(value, (dict, list)):
                items.extend(flatten_hbr_json(value, new_key, sep=sep).items())
            else:
                items.append((new_key, value))
    return dict(items)


def remove_html_tags(text: str) -> str:
    """
    Remove HTML tags from text while preserving the text content.
    
    Args:
        text (str): Text containing HTML tags
        
    Returns:
        str: Clean text without HTML tags
        
    Examples:
        >>> remove_html_tags("<p>Hello <b>World!</b></p>")
        'Hello World!'
        >>> remove_html_tags(None)
        ''
    """
    # Handle None or empty string
    if not text:
        return ""
    # Method 1: Using regex (faster but less robust)
    clean_text = re.sub(r'<[^>]+>', '', text)
    # Remove extra whitespace
    clean_text = ' '.join(clean_text.split())
    return clean_text


def read_podcasts_json_file():
    """
    Read podcasts data from JSON file in data/podcasts.json.
    Returns:
        list: List of podcasts data.
    Raises:
        FileNotFoundError: If the JSON file is not found.
        ValueError: If the JSON file is empty or invalid.
    """
    base_path = Path(__file__).parent.parent
    file_path = base_path / "data" / "podcasts.json"
    try:
        with open(file_path, "r") as f:
            content = f.read().strip()
            if not content:
                raise ValueError("JSON file is empty")
            rss = json.loads(content).get("rss", [])
            podcasts = rss.get("channel", {}).get("item", [])
            if not isinstance(podcasts, list):
                raise ValueError("Invalid JSON format: expected a list of podcasts")
            return map(flatten_json, podcasts)
    except FileNotFoundError:
        raise FileNotFoundError("JSON file not found: data/podcasts.json")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {str(e)}")


def process_single_file(file_path: Path) -> Iterator:
    """
    Process a single JSON file and extract podcast data.
    
    Args:
        file_path: Path to the JSON file
    Returns:
        Iterator of flattened podcast items
    """
    try:
        with open(file_path, "r") as f:
            content = f.read().strip()
            if not content:
                logging.warning(f"Empty file: {file_path}")
                return iter([])
                
            data = json.loads(content)
            podcasts = data.get("rss", {}).get("channel", {}).get("item", [])
            
            if not isinstance(podcasts, list):
                logging.error(f"Invalid format in {file_path}: expected a list of podcasts")
                return iter([])
            
            if 'hbr' in file_path.name:
                return map(flatten_hbr_json, podcasts)
            elif 'mckinsey' in file_path.name:
                return map(flatten_json, podcasts)
    except (json.JSONDecodeError, ValueError) as e:
        logging.error(f"Error processing {file_path}: {str(e)}")
        return iter([])


def read_podcasts_json_files(directory: str = "data", pattern: str = "*.json") -> Iterator:
    """
    Read multiple podcast JSON files concurrently from the specified directory.
    
    Args:
        directory: Directory containing JSON files (default: "data")
        pattern: File pattern to match (default: "*.json")
    Returns:
        Iterator of all podcast data combined
    Raises:
        FileNotFoundError: If the directory is not found
    """
    base_path = Path(__file__).parent.parent
    data_dir = base_path / directory
    
    if not data_dir.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    json_files = list(data_dir.glob(pattern))
    if not json_files:
        raise FileNotFoundError(f"No JSON files found in {directory}")

    # Use ThreadPoolExecutor for concurrent file processing
    with ThreadPoolExecutor() as executor:
        # Process all files concurrently and chain the results
        results = executor.map(process_single_file, json_files)
        
        # Flatten the results from all files into a single iterator
        from itertools import chain
        return chain.from_iterable(results)        