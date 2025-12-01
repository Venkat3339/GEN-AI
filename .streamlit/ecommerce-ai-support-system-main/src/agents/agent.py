#!/usr/bin/env python3
"""
SQL-powered Customer Support Agent using LangChain SQL Agent
This replaces the pre-defined database method approach with dynamic SQL generation
"""

import sys
import os
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from src.database.agent import sql_agent
from src.models.llm_manager import llm_manager

logger = logging.getLogger(__name__)

class SQLCustomerSupportAgent:
    """
    Customer support agent that uses LangChain SQL Agent for dynamic query generation.
    This is the original RAG + SQL Agent architecture as intended for the capstone project.
    """
    
    def __init__(self):
        self.sql_agent = sql_agent
        self.llm = llm_manager
        self.conversation_histories = {}  # Store conversation history per customer
        
    def process_customer_query(self, query: str, customer_id: str, session_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process a customer query using SQL Agent for data retrieval and LLM for response generation
        
        Args:
            query: Customer's question
            customer_id: ID of the logged-in customer (string like 'C0001')
            session_data: Additional session information
            
        Returns:
            Dict containing response, sql_query, and metadata
        """
        try:
            # Get customer context using SQL Agent
            customer_info = self.sql_agent.get_customer_context(customer_id)
            if not customer_info:
                return {
                    "response": "I'm sorry, I couldn't find your customer information. Please contact support.",
                    "success": False,
                    "error": "Customer not found"
                }
            
            # Initialize conversation history if not exists
            is_new_conversation = customer_id not in self.conversation_histories
            if is_new_conversation:
                self.conversation_histories[customer_id] = []
                
                # Check if the first query is a simple greeting only
                query_lower = query.lower().strip()
                simple_greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
                
                if query_lower in simple_greetings:
                    # Send greeting for simple greeting queries only
                    customer_name = customer_info.get('name', 'Customer')
                    greeting_response = f"Hello {customer_name}! I'm here to help you with any questions about your orders or our products. How can I assist you today?"
                    
                    # Add to conversation history
                    self.conversation_histories[customer_id].append({
                        "role": "user",
                        "content": query,
                        "timestamp": datetime.now().isoformat()
                    })
                    self.conversation_histories[customer_id].append({
                        "role": "assistant",
                        "content": greeting_response,
                        "timestamp": datetime.now().isoformat()
                    })
                    return {
                        "response": greeting_response,
                        "success": True,
                        "query_type": "greeting",
                        "is_greeting": True
                    }
            
            # Add current query to conversation history
            self.conversation_histories[customer_id].append({
                "role": "user",
                "content": query,
                "timestamp": datetime.now().isoformat()
            })
            
            # Classify query type for handling
            query_classification = self._classify_query_type(query)
            
            # Handle different query types
            if query_classification["type"] == "courtesy":
                response = self._handle_courtesy_response(query)
                sql_query = None
                data_results = None
                
            elif query_classification["type"] == "contextual":
                # For contextual responses like "yes/no", let the model understand the full conversation context
                response = self.llm.generate_response(
                    customer_query=query,
                    customer_context=customer_info,
                    conversation_history=self.conversation_histories[customer_id]
                )
                sql_query = None
                data_results = None
                
            elif query_classification["type"] == "non_supported":
                response = "I can only assist with questions about your orders and our products. Please contact our general support for other inquiries."
                sql_query = None
                data_results = None
                
            else:
                # Use SQL Agent to generate and execute query
                sql_result = self.sql_agent.generate_and_execute_query(query, customer_id)
                
                if not sql_result["success"]:
                    response = "I'm having trouble accessing your information right now. Please try rephrasing your question or contact support."
                    sql_query = sql_result.get("query")
                    data_results = None
                else:
                    # Generate natural language response using the SQL results
                    response = self._generate_response_from_sql_results(
                        query=query,
                        customer_info=customer_info,
                        sql_results=sql_result["results"],
                        sql_query=sql_result["query"]
                    )
                    sql_query = sql_result["query"]
                    data_results = sql_result["results"]
            
            # Add response to conversation history
            self.conversation_histories[customer_id].append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().isoformat()
            })
            
            # Keep conversation history manageable (last 20 messages)
            if len(self.conversation_histories[customer_id]) > 20:
                self.conversation_histories[customer_id] = self.conversation_histories[customer_id][-20:]
            
            return {
                "response": response,
                "success": True,
                "customer_info": customer_info,
                "query_type": query_classification["type"],
                "sql_query": sql_query,
                "data_results": data_results,
                "result_count": len(data_results) if data_results else 0,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing customer query: {e}")
            return {
                "response": "I'm experiencing technical difficulties. Please try again or contact our support team.",
                "success": False,
                "error": str(e)
            }
    
    def _classify_query_type(self, query: str) -> Dict[str, Any]:
        """
        Simple query classification to determine if we need SQL Agent or can handle directly
        """
        query_lower = query.lower().strip()
        
        # Handle contextual short responses (yes, no, sure, etc.)
        affirmative_responses = ["yes", "yeah", "yep", "sure", "ok", "okay", "alright", "please", "definitely", "absolutely"]
        negative_responses = ["no", "nope", "nah", "not really", "no thanks", "no thank you"]
        
        if query_lower in affirmative_responses or query_lower in negative_responses:
            return {"type": "contextual", "needs_sql": False}
        
        # Handle courtesy responses
        if any(phrase in query_lower for phrase in ["thank you", "thanks", "thank u", "thx"]):
            return {"type": "courtesy", "needs_sql": False}
        
        if query_lower in ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]:
            return {"type": "courtesy", "needs_sql": False}
        
        if any(phrase in query_lower for phrase in ["bye", "goodbye", "see you", "have a good day"]):
            return {"type": "courtesy", "needs_sql": False}
        
        # Check for order/product-related keywords that need SQL
        data_keywords = [
            "order", "orders", "purchase", "bought", "delivery", "shipping", "shipped", 
            "track", "tracking", "status", "arrive", "arrival", "eta", "when will",
            "where is", "last order", "recent order", "latest order", "first order",
            "my order", "order history", "cancelled", "pending", "processing",
            "total cost", "total price", "total amount", "how much", "spend", "spent",
            "product", "products", "item", "items", "price", "cost", "available",
            "stock", "category", "brand", "description", "specifications", "specs",
            "what is", "tell me about", "information about", "details about",
            "offer", "sell", "selling", "catalog", "list", "top", "best", "popular"
        ]
        
        if any(keyword in query_lower for keyword in data_keywords):
            return {"type": "data_query", "needs_sql": True}
        
        # Non-supported query
        return {"type": "non_supported", "needs_sql": False}
    
    def _handle_courtesy_response(self, query: str) -> str:
        """Handle courtesy responses without SQL"""
        query_lower = query.lower().strip()
        
        if any(phrase in query_lower for phrase in ["thank you", "thanks", "thank u", "thx"]):
            return "You're very welcome! I'm happy to help. Is there anything else I can assist you with regarding your orders or our products?"
        
        if query_lower in ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]:
            return "Hello! I'm here to help you with any questions about your orders or our products. How can I assist you today?"
        
        if any(phrase in query_lower for phrase in ["bye", "goodbye", "see you", "have a good day"]):
            return "Thank you for contacting us! Have a wonderful day, and feel free to reach out if you need any help with your orders or product questions."
        
        return "How can I help you today?"
    
    def _generate_response_from_sql_results(self, query: str, customer_info: Dict[str, Any], 
                                          sql_results: List[Dict[str, Any]], sql_query: str) -> str:
        """
        Generate natural language response from SQL results using LLM
        """
        customer_name = customer_info.get('name', 'Customer')
        
        # Determine if this is the start of conversation
        is_conversation_start = len(self.conversation_histories.get(customer_info.get('_id', ''), [])) <= 2
        
        # Create conversation context
        conversation_context = ""
        if customer_info.get('_id') in self.conversation_histories:
            recent_messages = self.conversation_histories[customer_info.get('_id')][-6:]
            conversation_context = "\n".join([
                f"{'Customer' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                for msg in recent_messages
            ])
        
        # Create the system prompt for response generation
        system_prompt = f"""You are a helpful AI customer support assistant for an e-commerce company.

IMPORTANT RULES:
1. You can help with ORDER-RELATED questions and PRODUCT INFORMATION queries
2. Always be polite, professional, and helpful
3. {"Use the customer's name (" + customer_name + ") in your greeting if this is the start of conversation, otherwise just answer directly" if is_conversation_start else "Do NOT greet the customer again - this is an ongoing conversation. Answer their question directly"}
4. NEVER include customer IDs (like C0001) or internal IDs in responses unless specifically asked
5. NEVER mention SQL queries, database operations, or any technical system details in your responses
6. NEVER say phrases like "The SQL query executed earlier" or "according to our database query"
7. When presenting a list of items (e.g., products, orders), use a clear, readable format. Use Markdown lists (e.g., * Item 1) for better readability.
8. ONLY use information from the database results provided below. Do NOT make up or hallucinate any data.
9. If the database results are empty, say so clearly without mentioning technical details.

Customer Information:
- Name: {customer_info.get('name', 'N/A')}
- Email: {customer_info.get('email', 'N/A')}
- Member since: {customer_info.get('created_date', 'N/A')}

Database Results: {sql_results}

Customer Query: "{query}"

Recent conversation history (for context):
{conversation_context}

{"This is the start of your conversation with this customer. Greet them warmly and then answer their question using ONLY the database results above." if is_conversation_start else "This is an ongoing conversation. Answer the customer's question directly using ONLY the database results above without greeting them again."}

Generate a helpful, natural response based STRICTLY on the database results provided. Do not mention any technical details about how the information was retrieved."""

        try:
            response = self.llm.llm.invoke(system_prompt)
            # Return the response directly without cleaning/formatting
            return response.strip()
        except Exception as e:
            logger.error(f"Failed to generate response from SQL results: {e}")
            return f"I found some information for you, but I'm having trouble formatting the response. Please try again or contact support."
    
    def clear_conversation_history(self, customer_id: str):
        """Clear conversation history for a customer (useful for logout)"""
        if customer_id in self.conversation_histories:
            del self.conversation_histories[customer_id]
    
    def test_system(self, customer_id: str = "C0001") -> Dict[str, Any]:
        """
        Test the SQL Agent system with sample queries
        """
        test_queries = [
            "What's my last order?",
            "Show me all my orders",
            "What's the total cost of all my orders?",
            "Do I have any shipped orders?",
            "What products are available?",
            "Thank you!",
            "What's the weather like?"  # This should be rejected
        ]
        
        results = []
        # Clear history for clean test
        self.clear_conversation_history(customer_id)
        
        for query in test_queries:
            print(f"\n🤖 Testing SQL Agent query: '{query}'")
            result = self.process_customer_query(query, customer_id)
            results.append({
                "query": query,
                "response": result["response"],
                "success": result["success"],
                "query_type": result.get("query_type", "unknown"),
                "sql_query": result.get("sql_query"),
                "result_count": result.get("result_count", 0)
            })
            print(f"✅ SQL Query: {result.get('sql_query', 'None')}")
            print(f"✅ Response: {result['response'][:100]}...")
        
        return {
            "test_results": results,
            "total_queries": len(test_queries),
            "successful_queries": sum(1 for r in results if r["success"]),
            "sql_queries_generated": sum(1 for r in results if r.get("sql_query")),
            "data_queries": sum(1 for r in results if r.get("query_type") == "data_query")
        }

# Global SQL-powered agent instance
sql_customer_agent = SQLCustomerSupportAgent() 