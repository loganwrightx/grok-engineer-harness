"""
Author: Logan Wright
Date: October 17th, 2026
Description: Main program entry-point to run the Grok engineering harness suite. This program is the main interface to begin using Grok
via the API with all the available engineering harnesses. See the README.md file to track the feature list and status.
"""

# Import helper module
from helper import *

# Import custom webapp module
from webapp import *

# Import custom harness modules
from harness_modules import (
    coding,
    designing,
    manufacturing
)

def prompt_agent(session: Session, prompt: str) -> dict | list | None:
    # Send the prompt to the specified model
    res = session.post(
        XAI_BASE_URL + "v1/responses",
        json={
            "input": prompt,
            # Add in the default agent options as kwargs
            **DEFAULT_AGENT_CONFIGS
        }
    )
    print(dumps(res.json(), indent=4))
    # Make sure the response was received well
    if res.status_code == 200:
        return res.json()
    return None

def main():
    # Build a stanard parser
    parser = ArgumentParser(
        description="Grok Engineering Harness Suite"
    )
        
    # Request a .env file with the GROK_API_KEY variable, but move along if not given
    parser.add_argument(
        "--env",
        type=str,
        help="Environment file containing the GROK_API_KEY environment variable (default file is grok.env) - optional if GROK_API_KEY is set in current shell",
        required=False
    )
        
    # Parse args
    args = parser.parse_args()
        
    # Safely load the .env if given
    safely_load_env(args.env)
        
    # Make sure variable is set
    if not ensure_api_key_given():
        raise Exception("GROK_API_KEY not set! Double check your spelling in your env file name and contents.")
        
    # Make sure API is responsive with the given key
    if not ensure_api_key_valid():
        raise Exception("Grok API key is not valid! Please generate a new Grok API key and set it in the environment variable then try again.")

def register_queues_with_callbacks(prompt_queue: Queue, response_queue: Queue) -> None:
    return

def grok_main(prompt_queue: Queue, response_queue: Queue):
    # Make the single HTTP session to the Grok API
    session = get_api_session()
    
    # Send Grok a prompt to build a tree.py file for demo purposes
    #answer: str = prompt_agent(
    #    session,
    #    "Hey Grok, this is a test API call from my personal python script." \
    #        "Can you build me a simple single-file python 3.13 program that does the Linux `tree` command? You are restricted to use only builtin libraries and cannot directly use the `tree` command."
    #).get("output")[1].get("content")[0].get("text")
    
    # Find the file contents for the python script with re
    #file_content = ""
    #in_file = False
    #for line in answer.split('\n'):
    #    if line.startswith("```python"):
    #        in_file = True
    #    elif line.startswith("```") and in_file:
    #        in_file = False
    #    
    #    if in_file and not line.startswith("```"):
    #        file_content += line + "\n"
    
    # Then write the contents into the target file
    #with open("new_tree.py", "w") as f:
    #    f.write(file_content)
    
    session.close()

if __name__ == '__main__':
    # Run main first
    main()
    
    # Then, if main is successful, run the Grok thread in the background to service the webapp. Share data via 2 queues
    grok_prompt_queue: Queue[str] = Queue(maxsize=10)
    grok_response_queue: Queue[str] = Queue(maxsize=10)
    grok_thread = Thread(
        target=grok_main,
        kwargs={
            "prompt_queue": grok_prompt_queue,
            "response_queue": grok_response_queue
        }
    )
    grok_thread.start()
    
    # Register the queues with the callbacks for the webapp to use them correctly
    register_queues_with_callbacks(grok_prompt_queue, grok_response_queue)
    
    # Register the queues into the webapp
    webapp.register_queues(
        grok_prompt_queue,
        grok_response_queue
    )
    
    # Then register all the webapp callback functions to load the endpoints
    webapp.register_callbacks()
    
    # And finally, start the webapp
    webapp.start()