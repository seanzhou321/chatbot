import gradio as gr

# Initialize conversation history
conversation_history = []

# Sample customer support chatbot function
def chatbot(user_input):
    global conversation_history
    response = ""
    options = []
    key_points = []

    # Simulate chatbot responses and actions
    if "issue" in user_input.lower():
        response = "Can you provide more details about the issue you're experiencing?"
    elif "refund" in user_input.lower():
        response = "I understand you're interested in a refund. Here are your options:"
        options = ["Full Refund", "Partial Refund", "Store Credit"]
    elif "confirm" in user_input.lower():
        response = "Thank you for confirming. Here are the key points discussed so far:"
        key_points = ["Customer reported an issue", "Refund options provided"]
    else:
        response = "Could you please elaborate on your request?"

    # Append user and bot messages to conversation history
    conversation_history.append(("you", user_input))
    
    # Construct bot response with options and key points, if available
    bot_message = response
    if options:
        bot_message += "\n\nOptions:\n" + "\n".join([f"- {option}" for option in options])
    if key_points:
        bot_message += "\n\nKey Points:\n" + "\n".join([f"- {point}" for point in key_points])
    
    conversation_history.append(("Bot", bot_message))

    # Format conversation history display
    display_history = ""
    for role, msg in conversation_history:
        if role == "you":
            display_history += f'<div style="text-align: right; color: gold; white-space: pre-wrap;"><b>{role}:</b> {msg}</div><br>'
        else:
            display_history += f'<div style="text-align: left; color: #9ACD32; white-space: pre-wrap;"><b>{role}:</b> {msg}</div><br>'


    return display_history

# Function to handle user input and update conversation history
def interact(user_input, history):
    new_history = chatbot(user_input)
    return "", new_history  # Clear user input after sending

# Gradio interface setup
with gr.Blocks(css="""
            .chatbox {height: 80vh; overflow-y: auto; background-color: #222222}
            .small-btn {padding: 5px 10px; font-size:12px; min-width:40px;max-width:80px;}
""") as app:
    gr.Markdown("### Customer Support Chatbot")
    
    # Conversation history display
    chat_history = gr.HTML(label="Conversation History", elem_classes="chatbox")

    with gr.Row():
        # User input and button
        user_input = gr.Textbox(
            label="Your Message", 
            placeholder="Type ysour message here...",
            submit_btn=True,
        )
        submit_btn = gr.Button("Send", elem_classes="small-btn")

    # Button action to send message
    submit_btn.click(interact, inputs=[user_input, chat_history], outputs=[user_input, chat_history])

    # bind the enter key to the submit action
    user_input.submit(interact, inputs=[user_input, chat_history], outputs=[user_input, chat_history])

# Launch the Gradio app
if __name__ == "__main__":
    app.launch()
