import streamlit as st                          # Import Streamlit for building the web app
from transformers import pipeline                 # Import Hugging Face pipeline for easy model loading

# -----------------------------
# 1. Page configuration
# -----------------------------
st.set_page_config(                               # Configure basic page settings (title, icon)
    page_title="Local AI Chatbot",                # Title shown in browser tab
    page_icon="💬"                                # Small emoji icon shown in tab
)

st.title("💬 Streamlit Chatbot with Local AI Model (No API Key)")  # Main heading displayed in the app


# -----------------------------
# 2. Load a real AI model (no API key)
# -----------------------------
@st.cache_resource                                # Cache the model so it is loaded only once
def load_model():
    # Load a small text-generation model using Hugging Face transformers.
    # This is a REAL AI model (distilgpt2) running locally.
    # It will download once and then be reused from cache.
    generator = pipeline(                         # Create a text-generation pipeline
        "text-generation",                        # Task type: generate text
        model="microsoft/DialoGPT-medium",                       # Small GPT-2 variant, good for demos
        max_new_tokens=200                        # Maximum number of new tokens to generate
    )
    return generator                              # Return the configured pipeline object


generator = load_model()                          # Actually load (or retrieve cached) model


# -----------------------------
# 3. Prompt building and reply generation
# -----------------------------
def build_prompt_from_history(history, user_message):
    # Build a simple chat-style prompt string from previous messages + new user message.
    # history: list of {"role": "user"/"bot", "text": "..."}
    # user_message: latest user input string
    lines = []                                    # Start with an empty list of lines

    for msg in history:                           # Loop through all previous messages
        if msg["role"] == "user":                 # If the message was from user
            lines.append(f"User: {msg['text']}")  # Format as 'User: ...'
        else:                                     # Otherwise, it's from the bot
            lines.append(f"Bot: {msg['text']}")   # Format as 'Bot: ...'

    lines.append(f"User: {user_message}")         # Add the latest user message
    lines.append("Bot:")                          # Ask model to continue as the bot

    return "\n".join(lines)                      # Join all lines into a single prompt string


def generate_bot_reply(history, user_message, temperature=0.7):
    # Call the real AI model (distilgpt2) to generate a reply based on conversation history.
    prompt = build_prompt_from_history(history, user_message)  # Build prompt from history + latest user message

    outputs = generator(                         # Call the text-generation pipeline
        prompt,                                  # Prompt text to continue from
        do_sample=True,                          # Enable sampling for more diverse outputs
        temperature=temperature,                 # Controls randomness (higher = more creative)
        max_new_tokens=80,                       # Limit length of generated reply
        num_return_sequences=1                   # We only need one reply sequence
    )

    full_text = outputs[0]["generated_text"]     # Extract the generated text from the first (and only) result

    # Try to keep only the text after the last "Bot:" to avoid repeating the prompt
    if "Bot:" in full_text:                      # Check if "Bot:" appears in the generated text
        bot_part = full_text.split("Bot:")[-1].strip()  # Take the part after the last "Bot:"
    else:
        bot_part = full_text                     # If no "Bot:", use full text as fallback

    # Sometimes the model continues with extra "User:" or "Bot:", cut at those markers if present
    for stop_token in ["User:", "Bot:"]:         # Look for markers indicating new turns
        if stop_token in bot_part:
            bot_part = bot_part.split(stop_token)[0].strip()  # Keep only text before the marker

    # If nothing meaningful remains, provide a safe fallback reply
    if len(bot_part) == 0:
        bot_part = "Sorry, I couldn't think of a good answer this time. 😅"

    return bot_part                              # Return the cleaned-up bot reply


# -----------------------------
# 4. Session state initialization
# -----------------------------
if "messages" not in st.session_state:           # If this is the first time in this session
    st.session_state["messages"] = [             # Initialize chat history list
        {
            "role": "bot",                       # Mark as bot message
            "text": "Hi, I'm a local AI chatbot running without any API key. How can I help you today?"
        }
    ]

if "temperature" not in st.session_state:        # Store temperature in session_state as well
    st.session_state["temperature"] = 0.7        # Default creativity level


# -----------------------------
# 5. Sidebar: settings and actions
# -----------------------------
st.sidebar.header("⚙️ Model Settings")           # Sidebar heading
st.sidebar.write("These settings control how creative the AI is.")  # Helper text

temperature = st.sidebar.slider(                 # Slider widget for temperature
    "Temperature (higher = more creative)",      # Label shown to user
    min_value=0.1,                               # Minimum value of slider
    max_value=1.5,                               # Maximum value of slider
    value=st.session_state["temperature"],       # Initial value (from session state)
    step=0.1                                     # Step size when moving slider
)
st.session_state["temperature"] = temperature    # Save slider value back to session state

with st.sidebar.expander("ℹ️ About this demo"):  # Collapsible info box in sidebar
    st.write(
        "- Model: distilgpt2 (Hugging Face transformers)  \n"
        "- Runs locally, no API key  \n"
        "- Intended for learning Streamlit + AI integration"
    )

if st.sidebar.button("🧹 Clear Chat History"):   # Button to clear chat
    st.session_state["messages"] = [             # Reset messages to a single welcome message
        {
            "role": "bot",
            "text": "Chat cleared. Let's start again! 🧠"
        }
    ]    
    st.rerun()                      # Rerun to refresh UI immediately


# -----------------------------
# 6. Display the conversation
# -----------------------------
st.subheader("Conversation")                     # Subheading above chat area

for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(
            f"""
<div style=" padding:10px; border-radius:10px; margin-bottom:10px;">
<b>You:</b> {msg['text']}
</div>
""",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
<div style=" padding:10px; border-radius:10px; margin-bottom:10px;">
<b>Bot:</b> {msg['text']}
</div>
""",
            unsafe_allow_html=True
        )



# -----------------------------
# 7. Chat input form
# -----------------------------
with st.form("chat_form", clear_on_submit=True): # Create a form for message input
    user_input = st.text_input("Type your message", "")  # Text field for user message
    submitted = st.form_submit_button("Send")    # Submit button for the form

if submitted and user_input.strip() != "":       # Only handle submission if text is not empty
    st.session_state["messages"].append(         # Add user message to history
        {"role": "user", "text": user_input}
    )

    with st.spinner("Thinking..."):              # Show spinner while model is generating
        reply = generate_bot_reply(              # Call function to get bot reply
            history=st.session_state["messages"],
            user_message=user_input,
            temperature=st.session_state["temperature"],
        )

    st.session_state["messages"].append(         # Add bot reply to history
        {"role": "bot", "text": reply}
    )

    st.rerun()