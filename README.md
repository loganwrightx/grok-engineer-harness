# Grok Engineer Harness

This repository is meant to use the Grok API to bring Grok into as many engineering workflows as I can think of. Below, you will find the scope of the development tasks that I am allowing Grok to work with. I am keeping this open-source to present my ideas and allow more talented contributors to work with me. Grok Build is a similar project, but this is more expansive and intended to be purely open-source. Implementing hooks for other agents will be a future endeavor and will begin by forking this repository.

## Table of Contents

1. [Environment Requirements](#environment-requirements)
2. [Harness Definitions and Requirements](#harness-definitions-and-requirements)
    - [Software Development](#software-development)
    - [Mechanical Design and Simulation (CAD)](#mechanical-design-and-simulation-cad)
    - [3D Printing](#3d-printing)

# Environment Requirements

| Name | Description | Status |
| :--: | :---------- | :----: |
| Personal API key | The user shall be required to provide their own API key to access Grok | Implemented |
| Agent management | The user must be supplied a locally hosted webapp interface that allows them to inject prompts, see resource management, interrupt actions, approve actions, and allocate resources to/from agents | Not Implemented |
| Display panel for user from agent | The agent(s) must be supplied knowledge of what the user is being presented as work is done | Not Implemented |
| Mode selection | The user must be able to select a single operating mode for the agent(s) – dedicated/solo (engineers that work in isolation and present final results) _or_ peer (engineers that collaborate with the user) | Not Implemented |

# Harness Architecture

For maximal reusability, all harnesses must inherit from the parent class, `GrokHarness`. `GrokHarness` will provide a few member methods that must be supported by each child class:

1. `help() -> str`: Returns a detailed description of what the harness _does_ and how to use it. This function will be the only thing that can tell the agent(s) how to use the respective toolset. This must be maintained to give the agent(s) all necessary context to effectively use the provided toolset. All usage of these harnesses will depend on defining a specific action (i.e. GET, POST, DELETE, etc.) as well as a body to perform the action with; this is extremely similar to a REST API.
2. `execute(command: str, *args, **kwargs) -> Any`: Single calling point for the agent(s) to execute their desired actions. Again, similar to a REST API, the command option specifies what to do with the args/kwargs.

Additional functions created in these child classes must be utilized within the above 3 functions – the main event loop will _not_ make calls to any other special functions.

# Harness Definitions and Requirements

## Software Development

TODO

## Mechanical Design and Simulation (CAD)

TODO

## 3D Printing

TODO