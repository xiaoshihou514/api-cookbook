# example_usage.py
from chat_with_persistence import initialize_chat_session, chat_with_persistence

def main():
    # Initialize a new chat session
    index = initialize_chat_session()
    
    # First query
    print("### Initial Query ###")
    response = chat_with_persistence("What's the current weather in London?", index)
    print(f"Assistant: {response}")
    
    # Follow-up query
    print("\n### Follow-Up Query ###")
    follow_up = chat_with_persistence("What about tomorrow's forecast?", index)
    print(f"Assistant: {follow_up}")
    
if __name__ == "__main__":
    main()

