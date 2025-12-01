#!/usr/bin/env python3
"""
Test script for the E-commerce AI Support System
Tests database connectivity, AI model connectivity, and end-to-end functionality
"""

import sys
import os
import sqlite3
from datetime import datetime

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

def test_database_connection():
    """Test BigQuery database connectivity and basic queries"""
    print("🔍 Testing BigQuery Database Connection...")
    
    try:
        from src.database.connection import db
        
        # Test basic connection
        print(f"✅ BigQuery client initialized for project: {db.project_id}")
        print(f"✅ Dataset: {db.dataset_id}")
        
        # Test customer query
        customer = db.get_customer_info("C0001")
        if customer:
            print(f"✅ Customer query successful. Sample customer: {customer['name']} (@{customer['username']})")
        else:
            print("❌ No customers found in database")
            return False
        
        # Test orders query
        orders = db.get_customer_orders("C0001", limit=3)
        if orders:
            print(f"✅ Orders query successful. Customer has {len(orders)} recent orders")
            for order in orders[:2]:  # Show first 2
                print(f"   - Order #{order['_id']}: {order['product'][:40]}... - {order['status']}")
        else:
            print("⚠️  No orders found for customer")
        
        return True
        
    except Exception as e:
        print(f"❌ BigQuery database test failed: {e}")
        print("   Make sure your BigQuery credentials are properly configured")
        return False

def test_ai_connectivity():
    """Test AI model connectivity"""
    print("\n🤖 Testing AI Model Connectivity...")
    
    try:
        from src.models.llm_manager import llm_manager
        
        # Test basic AI response
        test_query = "What is the status of my order?"
        is_order_related = llm_manager.is_order_related_query(test_query)
        print(f"✅ AI model responded. Query classification test: '{test_query}' -> Order-related: {is_order_related}")
        
        # Test response generation
        sample_customer = {"name": "John Doe", "email": "john@example.com", "_id": 1}
        sample_order = {
            "_id": 123,
            "product": "Wireless Headphones",
            "status": "shipped",
            "tracking_number": "TRK123456789",
            "order_date": "2024-01-15"
        }
        
        response = llm_manager.generate_response(
            customer_query="Where is my order?",
            customer_context=sample_customer,
            order_data=sample_order
        )
        print(f"✅ AI response generation successful")
        print(f"   Sample response: {response[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ AI connectivity test failed: {e}")
        print("   Make sure Ollama is running and the model is downloaded")
        return False

def test_customer_support_agent():
    """Test the main customer support agent"""
    print("\n🎯 Testing Customer Support Agent...")
    
    try:
        from src.agents.agent import sql_customer_agent as agent
        
        # Test with a real customer
        customer_id = "C0001"
        test_queries = [
            "Where is my last order?",
            "What's the status of my recent purchase?", 
            "What's the weather like today?"  # Should be rejected
        ]
        
        for query in test_queries:
            print(f"\n   Testing: '{query}'")
            result = agent.process_customer_query(query, customer_id)
            
            if result["success"]:
                query_type = result.get("query_type", "unknown")
                print(f"   ✅ Success - Type: {query_type}")
                print(f"   Response: {result['response'][:80]}...")
            else:
                print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Customer support agent test failed: {e}")
        return False

def test_database_content():
    """Test database content and structure"""
    print("\n📊 Testing Database Content...")
    
    try:
        from src.database.connection import db
        
        # Count customers
        customers = db.get_all_customers(limit=100)
        print(f"✅ Total customers: {len(customers)}")
        
        # Count orders for first few customers
        total_orders = 0
        customer_ids = ["C0001", "C0002", "C0003", "C0004", "C0005"]
        for customer_id in customer_ids:
            orders = db.get_customer_orders(customer_id, limit=100)
            total_orders += len(orders)
            if orders:
                print(f"   Customer {customer_id}: {len(orders)} orders")
        
        print(f"✅ Total orders (first 5 customers): {total_orders}")
        
        # Test different order statuses
        test_customer_id = "C0001"
        statuses = ['pending', 'processing', 'shipped', 'delivered']
        for status in statuses:
            orders = db.search_orders_by_status(test_customer_id, status)
            if orders:
                print(f"   Customer 1 has {len(orders)} {status} orders")
        
        return True
        
    except Exception as e:
        print(f"❌ Database content test failed: {e}")
        return False

def test_end_to_end():
    """Test complete end-to-end functionality"""
    print("\n🚀 Testing End-to-End Functionality...")
    
    try:
        from src.agents.agent import sql_customer_agent as agent
        
        # Get a customer with orders
        from src.database.connection import db
        customers = db.get_all_customers(limit=10)
        
        test_customer = None
        for customer in customers:
            orders = db.get_customer_orders(customer['_id'], limit=1)
            if orders:
                test_customer = customer
                break
        
        if not test_customer:
            print("❌ No customers with orders found for testing")
            return False
        
        print(f"✅ Testing with customer: {test_customer['name']} (ID: {test_customer['_id']})")
        
        # Test realistic scenarios
        scenarios = [
            "Where is my last order?",
            "Has my order been shipped?",
            "What did I order recently?",
            "Can you help me with my account password?"  # Should be rejected
        ]
        
        success_count = 0
        for scenario in scenarios:
            print(f"\n   Scenario: '{scenario}'")
            result = agent.process_customer_query(scenario, test_customer['_id'])
            
            if result["success"]:
                success_count += 1
                query_type = result.get("query_type", "unknown")
                print(f"   ✅ Response ({query_type}): {result['response'][:60]}...")
            else:
                print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
        
        print(f"\n✅ End-to-end test completed: {success_count}/{len(scenarios)} scenarios successful")
        return success_count == len(scenarios)
        
    except Exception as e:
        print(f"❌ End-to-end test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 E-commerce AI Support System - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Database Connection", test_database_connection),
        ("AI Connectivity", test_ai_connectivity),
        ("Database Content", test_database_content),
        ("Customer Support Agent", test_customer_support_agent),
        ("End-to-End Functionality", test_end_to_end)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for use.")
        print("\nTo start the application:")
        print("   python main.py")
        print("   or")
        print("   streamlit run src/ui/customer_chat.py")
    else:
        print("⚠️  Some tests failed. Please check the configuration.")
        print("\nCommon issues:")
        print("- Make sure Ollama is running: ollama serve")
        print("- Make sure the model is downloaded: ollama pull llama3.1:8b-instruct-q4_K_M")
        print("- Check if the database file exists: data/ecommerce_data.db")

if __name__ == "__main__":
    main() 