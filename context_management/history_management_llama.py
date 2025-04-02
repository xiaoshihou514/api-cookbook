import asyncio
import os
from dotenv import load_dotenv
from typing import List, Dict, Any
from openai import OpenAI
from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Event,
    Context,
)

# Load environment variables
load_dotenv()
API_KEY = os.getenv("SONAR_API_KEY")

# Custom events for our workflow
class QueryEvent(Event):
    query: str
    
class ProcessQueryEvent(Event):
    query: str
    conversation_history: List[Dict[str, str]]

class GenerateResponseEvent(Event):
    query: str
    conversation_history: List[Dict[str, str]]
    context: str

# Function to call Sonar API
def call_sonar_api(messages):
    client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
    )
    return response.choices[0].message.content

# Main workflow class
class SonarConversationWorkflow(Workflow):
    @step
    async def start(self, ctx: Context, ev: StartEvent) -> QueryEvent:
        # Entry point - extract the query
        return QueryEvent(query=ev.query)
    
    @step
    async def process_query(self, ctx: Context, ev: QueryEvent) -> ProcessQueryEvent:
        # Get conversation history from state or initialize new
        conversation_history = await ctx.get("conversation_history", default=[])
        
        # Add user query to history
        conversation_history.append({"role": "user", "content": ev.query})
        
        # Store updated history
        await ctx.set("conversation_history", conversation_history)
        
        return ProcessQueryEvent(
            query=ev.query, 
            conversation_history=conversation_history
        )
    
    @step
    async def retrieve_context(self, ctx: Context, ev: ProcessQueryEvent) -> GenerateResponseEvent:
        # Get or initialize entities state
        entities = await ctx.get("entities", default={})
        
        # Context generation from entities
        context_parts = []
        for entity_name, attributes in entities.items():
            attrs_str = ", ".join([f"{k}: {v}" for k, v in attributes.items()])
            context_parts.append(f"{entity_name}: {attrs_str}")
        
        context = "\n".join(context_parts) if context_parts else "No prior context available."
        
        return GenerateResponseEvent(
            query=ev.query,
            conversation_history=ev.conversation_history,
            context=context
        )
    
    @step
    async def generate_response(self, ctx: Context, ev: GenerateResponseEvent) -> StopEvent:
        # Prepare messages for API call
        system_message = {
            "role": "system", 
            "content": (
                "You are a helpful AI assistant that maintains context across multiple questions. "
                f"Current conversation context: {ev.context}"
            )
        }
        
        # Create full message history for the API call
        messages = [system_message] + ev.conversation_history
        
        # Call the Sonar API
        response = call_sonar_api(messages)
        
        # Extract entities from response (simplified version)
        if "president" in ev.query.lower():
            entities = await ctx.get("entities", default={})
            if "Donald Trump" in response:
                entities["US President"] = {
                    "name": "Donald Trump",
                    "position": "President of the United States"
                }
            await ctx.set("entities", entities)
        
        # Check for age-related info
        if "age" in ev.query.lower() and "US President" in await ctx.get("entities", {}):
            entities = await ctx.get("entities")
            if "78" in response or "seventy-eight" in response.lower():
                entities["US President"]["age"] = "78"
                await ctx.set("entities", entities)
        
        # Update conversation history
        conversation_history = ev.conversation_history.copy()
        conversation_history.append({"role": "assistant", "content": response})
        await ctx.set("conversation_history", conversation_history)
        
        return StopEvent(result={
            "response": response,
            "conversation_history": conversation_history,
            "updated_context": await ctx.get("entities", default={})
        })

# Function to process a single question
async def ask_question(workflow, query):
    result = await workflow.run(query=query)
    return result

# Interactive CLI chatbot function
async def run_chatbot():
    print("=" * 50)
    print("Welcome to the LlamaIndex Context-Aware Chatbot")
    print("Type 'quit', 'exit', or 'bye' to end the conversation")
    print("=" * 50)
    
    # Initialize workflow
    conversation_flow = SonarConversationWorkflow(timeout=30, verbose=False)
    
    while True:
        # Get user input
        user_input = input("\nYou: ")
        
        # Check for exit commands
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("\nGoodbye! Thanks for chatting.")
            break
        
        # Process user query
        try:
            print("\nBot: ", end="", flush=True)
            result = await ask_question(conversation_flow, user_input)
            
            # Print the response
            print(result["response"])
            
            # Optionally, uncomment to show the current context state
            # print("\nCurrent context:", result["updated_context"])
        except Exception as e:
            print(f"Error: {str(e)}")

# Run the async main function
if __name__ == "__main__":
    try:
        asyncio.run(run_chatbot())
    except KeyboardInterrupt:
        print("\nChatbot terminated by user.")