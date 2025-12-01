#!/usr/bin/env python3
"""
Customer Chat Interface using SQL Agent for dynamic query generation
"""

import streamlit as st
import time
import logging
from datetime import datetime

# Import the new SQL-powered agent
from src.agents.agent import sql_customer_agent

logger = logging.getLogger(__name__)

def initialize_chat_interface():
    """Initialize the chat interface with SQL Agent"""
    st.set_page_config(
        page_title="E-commerce AI Support",
        page_icon="🛒",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for better UI
    st.markdown("""
    <style>
    h1{
        color: white;
    }
    .main-header {
        background: #000000;
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .user-message {
        background: #e3f2fd;
        padding: 0.8rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        border-left: 4px solid #2196f3;
    }
    
    .assistant-message {
        background: #f1f8e9;
        padding: 0.8rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        border-left: 4px solid #4caf50;
    }
    
    .sql-query-display {
        background: #fff3e0;
        padding: 0.8rem;
        border-radius: 8px;
        border: 1px solid #ff9800;
        font-family: monospace;
        font-size: 0.9em;
        margin: 0.5rem 0;
    }
    
    .info-panel {
        background: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #4caf50;
    }
    </style>
    """, unsafe_allow_html=True)

def display_header():
    """Display the main header"""
    st.markdown("""
    <div class="main-header">
        <h1>E-commerce AI Support System</h1>
        <p>Powered by LangChain SQL Agent - Dynamic Query Generation</p>
    </div>
    """, unsafe_allow_html=True)

def display_sidebar():
    """Display sidebar with system information"""
    with st.sidebar:
        st.markdown("### 🔧 System Information")
        
        # System status
        with st.expander("🟢 System Status", expanded=True):
            st.success("✅ SQL Agent Active")
            st.info("🔄 Dynamic Query Generation")
            st.info("🗄️ BigQuery Connected")
            
        # Architecture info
        with st.expander("🏗️ Architecture", expanded=False):
            st.markdown("""
            **Current Implementation:**
            - 🧠 LangChain SQL Agent
            - 🔍 Dynamic SQL Generation
            - 📊 BigQuery Database
            - 🤖 Ollama LLM (Llama 3.1)
            
            **Features:**
            - Natural language to SQL
            - Real-time query generation
            - Contextual conversations
            - Order & product queries
            """)
        
        # Sample queries
        with st.expander("💡 Sample Queries", expanded=False):
            st.markdown("""
            **Try these queries:**
            - "What's my last order?"
            - "Show me all my orders"
            - "Total cost of all orders?"
            - "Do I have shipped orders?"
            - "What products do you offer?"
            - "Thank you!"
            """)
        
        # Debug options
        with st.expander("🔍 Debug Options", expanded=False):
            show_sql = st.checkbox("Show Generated SQL", value=True)
            show_metadata = st.checkbox("Show Response Metadata", value=False)
            return show_sql, show_metadata
    
    return True, False  # Default values if sidebar doesn't return

def display_chat_interface():
    """Main chat interface using SQL Agent"""
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "customer_id" not in st.session_state:
        st.session_state.customer_id = "C0001"  # Default customer for demo
    
    # Get debug options
    show_sql, show_metadata = display_sidebar()
    
    # Customer selection
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 💬 Chat with AI Support")
    with col2:
        customer_id = st.selectbox(
            "Customer ID:",
            ["C0001", "C0002", "C0003", "C0004", "C0005", "C0006", "C0007", "C0008", "C0009", "C0010"],
            index=0,
            key="customer_selector"
        )
        if customer_id != st.session_state.customer_id:
            st.session_state.customer_id = customer_id
            st.session_state.messages = []
            sql_customer_agent.clear_conversation_history(customer_id)
            st.rerun()
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <strong>You:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="assistant-message">
                    <strong>AI Support:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
                
                # Show SQL query if enabled and available
                if show_sql and "sql_query" in message and message["sql_query"]:
                    st.markdown(f"""
                    <div class="sql-query-display">
                        <strong>🔍 Generated SQL:</strong><br>
                        <code>{message["sql_query"]}</code>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Show metadata if enabled
                if show_metadata and "metadata" in message:
                    with st.expander("📊 Response Metadata", expanded=False):
                        st.json(message["metadata"])
    
    # Chat input
    if prompt := st.chat_input("Ask about your orders or our products..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message immediately
        with chat_container:
            st.markdown(f"""
            <div class="user-message">
                <strong>You:</strong> {prompt}
            </div>
            """, unsafe_allow_html=True)
        
        # Process with SQL Agent
        with st.spinner("🤖 Processing your request..."):
            try:
                # Use SQL Agent to process the query
                result = sql_customer_agent.process_customer_query(
                    query=prompt,
                    customer_id=st.session_state.customer_id
                )
                
                if result["success"]:
                    response = result["response"]
                    
                    # Prepare message with metadata
                    assistant_message = {
                        "role": "assistant",
                        "content": response,
                        "sql_query": result.get("sql_query"),
                        "metadata": {
                            "query_type": result.get("query_type"),
                            "result_count": result.get("result_count", 0),
                            "timestamp": result.get("timestamp"),
                            "customer_info": result.get("customer_info", {})
                        }
                    }
                    
                    st.session_state.messages.append(assistant_message)
                    
                    # Display assistant response
                    with chat_container:
                        st.markdown(f"""
                        <div class="assistant-message">
                            <strong>AI Support:</strong> {response}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Show SQL query if enabled
                        if show_sql and result.get("sql_query"):
                            st.markdown(f"""
                            <div class="sql-query-display">
                                <strong>🔍 Generated SQL:</strong><br>
                                <code>{result["sql_query"]}</code>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Show metadata if enabled
                        if show_metadata:
                            with st.expander("📊 Response Metadata", expanded=False):
                                st.json(assistant_message["metadata"])
                    
                else:
                    error_response = result.get("response", "I'm experiencing technical difficulties. Please try again.")
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_response,
                        "metadata": {"error": result.get("error", "Unknown error")}
                    })
                    
                    with chat_container:
                        st.error(f"❌ {error_response}")
                
            except Exception as e:
                logger.error(f"Chat processing error: {e}")
                error_message = "I'm experiencing technical difficulties. Please try again or contact support."
                st.session_state.messages.append({"role": "assistant", "content": error_message})
                
                with chat_container:
                    st.error(f"❌ {error_message}")
        
        # Rerun to update the interface
        st.rerun()

def display_test_panel():
    """Display simple testing panel"""
    st.markdown("### 🧪 System Status")
    
    if st.button("🔍 Test System", type="primary"):
        with st.spinner("Testing system..."):
            try:
                from src.database.agent import sql_agent
                connection_ok = sql_agent.test_connection()
                
                if connection_ok:
                    st.success("✅ System operational!")
                    st.info("🗄️ Database connected")
                    st.info("🤖 SQL Agent ready")
                else:
                    st.error("❌ Database connection failed!")
                    
            except Exception as e:
                st.error(f"❌ System test failed: {e}")

def main():
    """Main function to run the SQL Agent chat interface"""
    try:
        # Initialize the interface
        initialize_chat_interface()
        
        # Display header
        display_header()
        
        # Create tabs
        tab1, tab2 = st.tabs(["💬 Chat", "🧪 Status"])
        
        with tab1:
            display_chat_interface()
        
        with tab2:
            display_test_panel()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.9em;">
            🚀 E-commerce AI Support System | Powered by LangChain SQL Agent | 
            Dynamic Query Generation with Ollama Llama 3.1
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error("❌ Application failed to start. Please check the logs.")
        st.exception(e)

if __name__ == "__main__":
    main() 