"""
Author: Logan Wright
Date: October 17th, 2026
Description: Helper module to provide functions and imports to keep the main script legible.
"""

# Builtin imports
from pathlib import (
    Path
)
import re
import os
import sys
from argparse import (
    ArgumentParser
)
from json import (
    dumps,
    dump,
    loads,
    load
)

# Third-party imports
from dotenv import (
    load_dotenv
)
from requests import (
    Session
)
from urllib.parse import (
    quote,
    unquote
)

# Constants
XAI_BASE_URL = "https://api.x.ai/"
GROK_ENG_MODEL = "grok-build-0.1"
DEFAULT_AGENT_CONFIGS = {
    "model": GROK_ENG_MODEL,
    "temperature": 0.2, # between 0 and 2, low for deterministic responses
    "store": False, # set True if we want to reuse the prompt/response history
    "service_tier": "default", # | priority | fast
    #"reasoning": {
    #    "effort": "low" # low | medium | high | xhigh
    #},
    "stream": False # useful if we need to feed a real-time data stream
}

def get_api_session() -> Session:
    # Create a blank session
    s = Session()
    # Add/modify the appropriate authorization and json-expectation to the headers
    s.headers.update(
        {
            "Authorization": f"Bearer {os.environ.get('GROK_API_KEY')}",
            "Content-Type": "application/json"
        }
    )
    return s

def safely_load_env(env_file: str | None) -> None:
    # Check if env file is not None
    if env_file:
        # Then make sure the path is legit
        if not os.path.exists(env_file):
            return
        
        # Finally, load the env file
        load_dotenv(env_file)
    
    return

def ensure_api_key_given() -> bool:
    # Check if GROK_API_KEY is in the environment variable list
    return "GROK_API_KEY" in os.environ.keys()

def ensure_api_key_valid() -> bool:
    # Make a basic request to get a list of the available models with this API key - ensure the status code is 200
    res = get_api_session().get(XAI_BASE_URL + "v1/models")
    return res.status_code == 200