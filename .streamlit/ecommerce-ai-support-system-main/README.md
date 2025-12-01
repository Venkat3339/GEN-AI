# E-commerce AI Support System

A local AI-powered customer support system for e-commerce platforms, built as a capstone project. The system uses local LLM models with LangChain SQL Agent architecture and Google BigQuery cloud database to provide order-specific customer support responses.

## 🚀 Features

- **Local AI Model**: Runs entirely on local hardware using Ollama and Llama 3.1 8B
- **Cloud Database**: Google BigQuery for scalable data storage and querying
- **Order-Only Focus**: Handles only order-related queries, rejecting general questions
- **Session Management**: Simulated customer login - AI never asks for customer details
- **Dynamic SQL Generation**: Real-time SQL query generation from natural language
- **Web Interface**: Modern Streamlit-based chat interface

## 📁 Project Structure

```
ecommerce-ai-support-system/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── TODO.md                 # Project steps
│
├── src/                   # Source code
│   ├── __init__.py
│   ├── agents/           # AI agents
│   │   ├── __init__.py
│   │   └── agent.py      # SQL-powered customer support agent
│   ├── database/         # Database utilities
│   │   ├── __init__.py
│   │   ├── connection.py # BigQuery connection
│   │   └── agent.py      # SQL agent for dynamic queries
│   ├── models/           # AI model management
│   │   ├── __init__.py
│   │   └── llm_manager.py
│   └── ui/               # User interface
│       ├── __init__.py
│       └── customer_chat.py
│
├── config/               # Configuration
│   ├── __init__.py
│   ├── config.py
│   └── bq-key.json       # BigQuery service account key
│
└── scripts/              # Utility scripts
    ├── test_system.py
    └── test_bigquery_system.py
```

## 🛡️ System Boundaries & Security

The AI system is designed to:
- ✅ Answer order-related questions
- ✅ Provide shipping information
- ✅ Show order status and tracking
- ❌ Reject non-order related queries
- ❌ Never ask for customer email, order ID, etc.

### 🔒 Security Features

**Multi-Layer SQL Injection Protection:**
- **Input Sanitization**: Removes dangerous SQL patterns and injection attempts
- **Query Validation**: Only SELECT and WITH statements allowed
- **Prompt Security**: LLM instructions prevent malicious SQL generation
- **Operation Blocking**: Prevents DROP, DELETE, UPDATE, INSERT, ALTER operations

**Attack Protection:**
- ✅ SQL Injection attempts → Blocked and logged
- ✅ Prompt Injection attacks → Sanitized and neutralized  
- ✅ Comment-based attacks → Comments stripped from input
- ✅ Resource exhaustion → Input length limits enforced
- ✅ Data modification → Only read operations permitted

**Security Compliance:**
- OWASP SQL injection prevention guidelines
- Defense-in-depth architecture
- Comprehensive security logging
- Graceful error handling without information leakage

### 🛡️ Comprehensive Security Implementation

**Layer 1: Input Sanitization**
- **Pattern Removal**: Strips dangerous SQL keywords and patterns from user input
- **Comment Elimination**: Removes SQL comments (`--`, `/* */`) that could hide malicious code
- **Length Limiting**: Prevents extremely long inputs that could cause resource exhaustion
- **Pattern Neutralization**: Removes semicolons, dangerous SQL operations, and injection patterns
- **Security Logging**: Logs all sanitization actions for security monitoring

**Layer 2: LLM Prompt Security**
- **Security Instructions**: Explicit rules in LLM prompts to generate only safe SELECT/WITH queries
- **Operation Restrictions**: Clear instructions to ignore dangerous operations in customer queries
- **Context Awareness**: Treats suspicious SQL-like commands as normal text searches
- **Safe Query Focus**: Emphasizes data retrieval only, never modification or deletion

**Layer 3: SQL Validation**
- **Statement Type Check**: Ensures queries start only with SELECT or WITH
- **Dangerous Keyword Detection**: Blocks queries containing DROP, DELETE, UPDATE, INSERT, etc.
- **Case-Insensitive Validation**: Catches dangerous operations regardless of case
- **Comprehensive Coverage**: Protects against all major SQL injection attack vectors

## 🏗️ Architecture

- **Frontend**: Streamlit web interface
- **Backend**: Python with LangChain SQL Agent
- **Database**: Google BigQuery cloud database
- **AI Model**: Llama 3.1 8B via Ollama
- **Session**: Streamlit session state

### System Architecture Diagram

```
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ Streamlit UI     │    │ Python Backend   │    │ Google BigQuery  │
│                  │    │                  │    │                  │
│ • Customer Login │◄──►│ • Session Mgmt   │◄──►│ • customers      │
│ • Chat Interface │    │ • Query Handler  │    │ • orders         │
│ • Order Display  │    │ • AI Integration │    │ • products       │
│ • Sample Queries │    │ • BQ Connector   │    │ • Cloud Scale    │
└──────────────────┘    └──────────────────┘    └──────────────────┘
                                  │
                                  ▼
                        ┌──────────────────┐
                        │ Ollama Server    │
                        │                  │
                        │ • Llama 3.1 8B   │
                        │ • Local Hosting  │
                        │ • 4K Context     │ 
                        │ • GPU Optimized  │
                        └──────────────────┘
                                  │
                                  ▼
                        ┌──────────────────┐
                        │ LangChain SQL    │
                        │ Agent            │
                        │                  │
                        │ • Query Classify │
                        │ • Dynamic SQL    │
                        │ • BigQuery SQL   │
                        │ • Response Gen   │
                        └──────────────────┘
```
Flow: Customer Login → Query Input → [Classification → Dynamic SQL Generation → BigQuery + AI] → Natural Response

**Key Architecture Features:**
- **Dynamic SQL Generation**: Natural language queries are converted to BigQuery SQL in real-time
- **Context-Aware Processing**: System maintains conversation context for multi-turn interactions
- **Security-First Design**: Multi-layer protection against SQL injection and prompt attacks
- **Scalable Database**: BigQuery provides enterprise-grade scalability and performance

## 📊 Database Schema

The system uses Google BigQuery with a standard e-commerce schema:

**Tables:**
- **customers**: Customer profiles and account information
- **orders**: Order records with product, status, and tracking data  
- **products**: Product catalog with details, ratings, and inventory

**Benefits of BigQuery:**
- Scalable cloud infrastructure
- Fast analytical queries
- No local database maintenance
- Enterprise-grade security
- Real-time data access

## 🎯 Usage Examples

Sample customer queries the system handles:
- "Where is my last order?"
- "What's the status of my recent purchase?"
- "When will my order arrive?"
- "What did I order recently?"

Non-order queries are politely rejected:
- "What's the weather today?" → "I can only assist with questions related to your orders."

## 🔧 Technical Stack

- **AI/ML**: LangChain, Ollama, Llama 3.1 8B
- **Database**: Google BigQuery
- **Backend**: Python, Pydantic
- **Frontend**: Streamlit
- **Authentication**: Session-based simulation
- **Deployment**: Local development environment

## 📄 License

This project is created for educational purposes as part of a Computer Science capstone project.