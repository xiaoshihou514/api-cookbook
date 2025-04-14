# Integrating Perplexity’s Sonar API with the OpenAI SDK

This guide demonstrates how to integrate Perplexity’s Sonar API into the OpenAI SDK using a custom asynchronous client. The example shows how to create an agent that leverages the custom LLM provider, set up function tools, and run a sample query. This is ideal if you want to extend or customize your integration of the Sonar API for various applications.

## Overview

This example involves:
	•	Creating an asynchronous OpenAI client configured with Perplexity’s Sonar API.
	•	Creating a custom model that uses this client.
	•	Configuring an agent with custom instructions and a function tool to fetch weather.
	•	Running a sample query to demonstrate integration.

## Prerequisites
	•	Python 3.7 or later.
	•	Required Python packages:
	•	`openai`
	•	`nest_asyncio`
	•	The custom agents package (ensure this is installed or available in your environment).

Install dependencies via `pip` if needed:

```bash
pip install openai nest_asyncio
```

## Environment Setup

Set the following environment variables or update the code with the appropriate values:
	•	`EXAMPLE_BASE_URL`: The base URL of the Perplexity API (default: https://api.perplexity.ai).
	•	`EXAMPLE_API_KEY`: Your API key for accessing the Sonar API.
	•	`EXAMPLE_MODEL_NAME`: The model name, defaulting to `sonar-pro`.

## Usage

Simply run the script to create the agent and test a sample query asking for the weather in Tokyo. The agent will execute the query using the custom Sonar API-powered model and a tool to fetch weather data.


## Running the Example
	1.	Set up Environment Variables:
Ensure `EXAMPLE_BASE_URL`, `EXAMPLE_API_KEY`, and `EXAMPLE_MODEL_NAME` are set, either in your shell or within the code.
	2.	Install Dependencies:
Make sure you have installed the required packages (`openai`, `nest_asyncio`, and `agents`).
	3.	Execute the Script:
Run the script using Python:

```bash
python your_script_name.py
```

## Conclusion

This example provides a hands-on guide for integrating Perplexity’s Sonar API with the OpenAI SDK. The approach involves creating a custom asynchronous client, setting up a model with our API, and using an agent to process queries with additional function tools. Customize this code as needed to fit your application’s requirements.

References
	•	[Perplexity Sonar API Documentation](https://docs.perplexity.ai/home)
	•	[OpenAI Agents SDK Documentation](https://github.com/openai/openai-agents-python/blob/main/examples/model_providers/custom_example_agent.py)
