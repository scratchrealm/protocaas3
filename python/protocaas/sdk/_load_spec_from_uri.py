import requests
import os
import json
import tempfile

def _load_spec_from_uri(uri: str) -> dict:
    # Convert github blob URL to raw URL
    if (uri.startswith('https://github.com/')) and ('/blob/' in uri):
        raw_url = uri.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
    else:
        raw_url = uri

    # Download the content
    response = requests.get(raw_url)
    response.raise_for_status()
    content = response.text

    # Save to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json') as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name

    # Read the JSON content from the file
    with open(temp_file_path, 'r') as file:
        data = json.load(file)

    # Clean up the temporary file
    os.remove(temp_file_path)
    
    return data