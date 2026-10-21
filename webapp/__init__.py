"""
Author: Logan Wright
Date: October 17th, 2026
Description: This is the base file for the webapp module used to manage and service the Grok Engineer harnesses.
"""

# Builtin imports
from queue import Queue

# Dash imports
from dash import (
    Dash,
    html,
    callback,
    dcc,
    Input,
    Output
)

class WebApp:
    """Webapp wrapper for Dash object to fit the interface of this program"""
    def __init__(self) -> None:
        self._webapp = Dash()
        self._queues_registered: bool = False
        self._callbacks_registered: bool = False
        self._prompt_queue: Queue[str] | None = None
        self._response_queue: Queue[str] | None = None
    
    def configure_layout(self) -> None:
        """Initializes the webapp layout"""
        self._webapp.layout = [
            html.Header("Grok Engineering Suite"),
            html.Div(
                children=[
                    html.H1("Grok Engineering Suite")
                ]
            )
        ]
    
    def register_queues(self, prompt_queue: Queue[str], response_queue: Queue[str]) -> None:
        """Configures queues for inter-thread communication between the webapp task and the Grok API worker thread"""
        self._prompt_queue = prompt_queue
        self._response_queue = response_queue
        self._queues_registered = True
    
    # TODO: Add callback functions here like so with single underscored prefix...
    def _send_prompt(self, *args) -> str:
        return "Sent!"
    
    def register_callbacks(self) -> bool:
        """Registers the webapp callback functions with the queues"""
        if not self._queues_registered:
            # We must have the queues registered before initializing the callbacks
            return False
        
        # Register each callback one-by-one
        callback(
            Output("target-html-id", "property-of-that-html-object"),
            Input("trigger-html-id", "property-of-that-html-object")
        )(self._send_prompt)
        
        # Set the flag to true indicating that callbacks are alive
        self._callbacks_registered = True
        return True
    
    def start(self) -> bool:
        """Starts the webapp main event loop, but returns False early if preconditions are not yet met"""
        if not self._queues_registered or not self._callbacks_registered:
            return False
        
        # Start the webapp with debug mode on for now (saving the main program will auto-restart it to refresh)
        self._webapp.run(
            debug=True
        )
        
        # Return true to fit the return type
        return True

# Create a webapp instance
webapp = WebApp()