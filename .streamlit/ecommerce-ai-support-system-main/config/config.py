import os
from typing import Dict, Any
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "E-commerce AI Live Support"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-powered customer support with local LLM and RAG"
    
    # Database settings (BigQuery)
    BIGQUERY_PROJECT_ID: str
    BIGQUERY_DATASET_ID: str
    BIGQUERY_SERVICE_ACCOUNT_PATH: str
    
    # AI Model settings
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    DEFAULT_MODEL: str = "llama3.1:8b-instruct-q4_K_M"
    MODEL_TEMPERATURE: float = 0.1
    MAX_TOKENS: int = 2048
    
    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Allow extra fields to be ignored

# Global settings instance
settings = Settings()

# Database configuration for SQL Agent
DATABASE_CONFIG = {
    "project_id": settings.BIGQUERY_PROJECT_ID,
    "dataset_id": settings.BIGQUERY_DATASET_ID,
    "service_account_path": settings.BIGQUERY_SERVICE_ACCOUNT_PATH
}

# Prompt templates
SYSTEM_PROMPT = """You are an AI customer support assistant for an e-commerce company. 
You have access to a customer database with order history, product information, and customer details.

Key guidelines:
1. Be helpful, concise, and professional
2. Use the customer's data from the database to provide personalized responses
3. Never ask customers for information you can get from the database (email, order ID, etc.)
4. Focus on solving the customer's problem efficiently
5. If you need to query the database, generate precise SQL queries
6. Always verify information before providing it to the customer

Current customer context will be provided with each query."""

SQL_AGENT_PROMPT = """You are a SQL expert for a BigQuery e-commerce database. Generate precise BigQuery SQL queries to retrieve customer information.

Database schema (BigQuery):
- customers: _id (STRING), username (STRING), password (STRING), email (STRING), name (STRING), phone (STRING), address (STRING), created_date (STRING)
- orders: _id (STRING), customer_id (STRING), product (STRING), sku (STRING), price (FLOAT), quantity (INTEGER), order_date (STRING), status (STRING), status_detail (STRING), tracking_number (STRING), eta (STRING), updated_at (STRING)
- products: product_id (INTEGER), name (STRING), sku (STRING), description (STRING), category (STRING), price (NUMERIC), stock_quantity (INTEGER), brand (STRING), weight (NUMERIC), dimensions (STRING), color (STRING), material (STRING), rating (NUMERIC), review_count (INTEGER), is_active (BOOLEAN), created_date (TIMESTAMP), updated_date (TIMESTAMP)

Key relationships:
- orders.customer_id references customers._id
- Customer IDs are in format: C0001, C0002, etc.
- Order IDs are in format: O0001, O0002, etc.

Important BigQuery syntax notes:
- Use backticks for table references with project.dataset.table format
- Use STRING instead of TEXT data types
- Use FLOAT instead of REAL data types
- Always include relevant JOINs to get complete information
- Use the customer_id from the session context""" 
