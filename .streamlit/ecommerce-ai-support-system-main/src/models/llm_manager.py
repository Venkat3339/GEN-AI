from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from typing import Dict, Any, Optional, List
import logging
import json

logger = logging.getLogger(__name__)

class CustomerSupportLLM:
    """Local LLM manager for customer support focused on order-related queries and product information"""
    
    def __init__(self, model_name: str = "llama3.1:8b-instruct-q4_K_M", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.llm = None
        self._initialize_llm()
        
    def _initialize_llm(self):
        """Initialize the Ollama LLM"""
        try:
            self.llm = OllamaLLM(
                model=self.model_name,
                base_url=self.base_url,
                temperature=0.1,  # Low temperature for consistent responses
                top_p=0.9,
                num_predict=2048
            )
            logger.info(f"Successfully initialized LLM: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise
    
    def test_connection(self) -> bool:
        """Test if the LLM is working"""
        try:
            response = self.llm.invoke("Hello, please respond with 'OK' if you can hear me.")
            return "OK" in response or "ok" in response.lower()
        except Exception as e:
            logger.error(f"LLM connection test failed: {e}")
            return False
    
    def generate_response(self, customer_query: str, customer_context: Dict[str, Any], 
                         order_data: Optional[Dict[str, Any]] = None, 
                         product_data: Optional[Dict[str, Any]] = None,
                         conversation_history: List[Dict[str, str]] = None,
                         is_greeting: bool = False) -> str:
        """
        Generate a customer support response for order-related queries and product information
        """
        
        customer_name = customer_context.get('name', 'Customer')
        
        # Handle greeting
        if is_greeting:
            return f"Hello {customer_name}! I'm here to help you with any questions about your orders or our products. How can I assist you today?"
        
        # Handle common courtesy responses
        courtesy_responses = self._handle_courtesy_responses(customer_query)
        if courtesy_responses:
            return courtesy_responses
        
        # Create conversation context
        conversation_context = ""
        if conversation_history:
            recent_messages = conversation_history[-6:]  # Last 6 messages for context
            conversation_context = "\n".join([
                f"{'Customer' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                for msg in recent_messages
            ])
        
        # Prepare data sections
        order_section = f"Order Data: {json.dumps(order_data, indent=2)}" if order_data else "No order data available"
        product_section = f"Product Data: {json.dumps(product_data, indent=2)}" if product_data else "No product data available"
        conversation_section = f"Recent Conversation:\n{conversation_context}\n" if conversation_context else ""
        
        # Determine if this is the start of conversation
        is_conversation_start = not conversation_history or len(conversation_history) <= 1
        
        # Create the system prompt
        system_prompt = f"""You are a helpful AI customer support assistant for an e-commerce company. 

IMPORTANT RULES:
1. You can help with ORDER-RELATED questions and PRODUCT INFORMATION queries
2. Always be polite, professional, and helpful
3. {"Use the customer's name (" + customer_name + ") in your greeting if this is the start of conversation, otherwise just answer directly" if is_conversation_start else "Do NOT greet the customer again - this is an ongoing conversation. Answer their question directly"}
4. NEVER include customer IDs (like C0001) or product SKUs (like 7412) in responses unless the customer specifically asks for them
5. NEVER include debug messages like "Query processed: order_related" in your responses
6. For order questions, provide specific information from the order data
7. For product questions, provide helpful information from the product catalog
8. If you cannot find specific information, politely explain what you couldn't find and offer to help differently
9. For non-order and non-product questions, politely redirect: "I can only assist with questions about your orders and our products. Please contact our general support for other inquiries."
10. When asked about product catalogs or "what do you offer", describe the available products enthusiastically
11. When asked about order history, provide the available order information from the data - NEVER claim the system can't retrieve order history if order data is provided
12. For general product queries, showcase our product range and encourage browsing
13. If multiple orders are provided in the data, list them clearly with their details

FORMATTING RULES:
14. Use clear, readable formatting without special characters that might break rendering
15. For calculations and prices, use simple format: "3 Water Bottles at $14.99 each = $44.97"
16. Avoid using asterisks (*) for emphasis - use plain text instead
17. Use bullet points with dashes (-) for lists, not special characters
18. For mathematical expressions, use clear language: "The subtotal for this order is $44.97"
19. Structure multiple orders clearly with line breaks and simple formatting
20. Keep monetary values in standard format: $XX.XX (no special formatting)

CONTEXTUAL RESPONSE HANDLING:
21. If the customer gives a short response like "yes", "no", "sure", "okay", look at the conversation history to understand what you previously offered
22. If you previously offered to show products/catalog and they say "yes", provide product information
23. If you previously offered order help and they say "yes", provide order assistance
24. If they say "no" to your offers, politely acknowledge and ask if there's anything else you can help with
25. Always maintain conversation flow by understanding the context of what was previously discussed

Customer Information:
- Name: {customer_name}
- Email: {customer_context.get('email', '')}

Available Data:
{order_section}
{product_section}

{conversation_section}

Current Customer Query: {customer_query}

IMPORTANT: If this is a short response like "yes", "no", "sure", etc., carefully analyze the conversation history above to understand what you previously offered or asked, then respond appropriately based on that context.

FORMATTING REMINDER: Use clean, simple text formatting. Avoid asterisks, special characters, or complex markdown that might break text rendering. Keep calculations clear and readable.

{"This is the start of your conversation with this customer. Greet them warmly and then answer their question." if is_conversation_start else "This is an ongoing conversation. Answer the customer's question directly without greeting them again."}

Provide a helpful, natural response without any debug information or internal IDs unless specifically requested."""

        try:
            response = self.llm.invoke(system_prompt)
            # Return the response directly without cleaning/formatting
            return response.strip()
        except Exception as e:
            logger.error(f"Failed to generate response: {e}")
            return f"I apologize {customer_name}, but I'm experiencing technical difficulties. Please try again in a moment or contact our support team directly."
    
    def _clean_response_formatting(self, response: str) -> str:
        """Clean up response formatting to prevent UI rendering issues"""
        import re
        
        # Remove problematic formatting that breaks UI
        response = re.sub(r'\*([^*]+)\*', r'\1', response)  # Remove *text*
        response = re.sub(r'\s+', ' ', response)  # Clean up multiple spaces
        response = response.replace('**', '').replace('__', '')  # Remove formatting artifacts
        
        # Remove unwanted + signs at the beginning of lines (common LLM formatting issue)
        response = re.sub(r'^\s*\+\s*', '- ', response, flags=re.MULTILINE)  # Replace + with -
        response = re.sub(r'\n\s*\+\s*', '\n- ', response)  # Replace + with - in lists
        
        # Clean up any remaining formatting issues
        response = response.replace('+ ', '- ')  # Any remaining + to -
        
        return response.strip()
    
    def _handle_courtesy_responses(self, query: str) -> Optional[str]:
        """Handle common courtesy expressions"""
        query_lower = query.lower().strip()
        
        # Thank you responses
        if any(phrase in query_lower for phrase in ["thank you", "thanks", "thank u", "thx"]):
            return "You're very welcome! I'm happy to help. Is there anything else I can assist you with regarding your orders or our products?"
        
        # Greeting responses
        if query_lower in ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]:
            return "Hello! I'm here to help you with any questions about your orders or our products. How can I assist you today?"
        
        # Goodbye responses
        if any(phrase in query_lower for phrase in ["bye", "goodbye", "see you", "have a good day"]):
            return "Thank you for contacting us! Have a wonderful day, and feel free to reach out if you need any help with your orders or product questions."
        
        return None
    
    def _handle_contextual_responses(self, query_lower: str, conversation_history: List[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
        """Handle short contextual responses like 'yes', 'no', 'sure' based on conversation history"""
        
        # Check if this is a short affirmative/negative response
        affirmative_responses = ["yes", "yeah", "yep", "sure", "ok", "okay", "alright", "please", "definitely", "absolutely"]
        negative_responses = ["no", "nope", "nah", "not really", "no thanks", "no thank you"]
        
        if query_lower in affirmative_responses or query_lower in negative_responses:
            # For contextual responses, let the model handle it with full conversation context
            # Don't try to classify as specific query types - let the model understand the context
            return {"type": "contextual", "needs_data": False, "is_contextual": True}
        
        return None
    

    
    def is_order_related_query(self, query: str) -> bool:
        """
        Simple check if query is order/product related (kept for compatibility)
        """
        query_lower = query.lower()
        order_keywords = ["order", "orders", "product", "products", "purchase", "shipping", "delivery"]
        return any(keyword in query_lower for keyword in order_keywords)

# Global LLM instance
llm_manager = CustomerSupportLLM() 