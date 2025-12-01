#!/usr/bin/env python3
"""
Test script specifically for BigQuery-based E-commerce AI Support System
"""

import sys
import os
from datetime import datetime

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

def test_bigquery_connection():
    """Test BigQuery connection and basic queries"""
    print("🔍 Testing BigQuery Connection...")
    
    try:
        from src.database.connection import db
        
        print(f"✅ BigQuery Project: {db.project_id}")
        print(f"✅ Dataset: {db.dataset_id}")
        print(f"✅ Service Account: {db.service_account_path}")
        
        # Test customer query
        customer = db.get_customer_info("C0001")
        if customer:
            print(f"✅ Customer query successful")
            print(f"   Name: {customer['name']}")
            print(f"   Username: @{customer['username']}")
            print(f"   Email: {customer['email']}")
        else:
            print("❌ No customer C0001 found")
            return False
        
        # Test orders query
        orders = db.get_customer_orders("C0001", limit=3)
        if orders:
            print(f"✅ Orders query successful - Found {len(orders)} orders")
            for i, order in enumerate(orders[:2]):
                print(f"   {i+1}. Order #{order['_id']}: {order['product'][:30]}...")
                print(f"      Status: {order['status']} | Price: ${order['price']}")
        else:
            print("⚠️  No orders found for customer C0001")
        
        # Test all customers query
        all_customers = db.get_all_customers(limit=5)
        print(f"✅ Found {len(all_customers)} customers in database")
        
        return True
        
    except Exception as e:
        print(f"❌ BigQuery connection test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ai_model():
    """Test AI model with BigQuery data"""
    print("\n🤖 Testing AI Model with BigQuery Data...")
    
    try:
        from src.models.llm_manager import llm_manager
        
        # Test if model is available
        if not llm_manager.test_connection():
            print("❌ AI model not available. Make sure Ollama is running.")
            return False
        
        print("✅ AI model connection successful")
        
        # Test with real customer data
        from src.database.connection import db
        customer = db.get_customer_info("C0001")
        latest_order = db.get_customer_latest_order("C0001")
        
        if customer and latest_order:
            response = llm_manager.generate_response(
                customer_query="Where is my last order?",
                customer_context=customer,
                order_data=latest_order
            )
            print("✅ AI response generation successful")
            print(f"   Query: 'Where is my last order?'")
            print(f"   Response: {response[:100]}...")
        else:
            print("⚠️ Could not test AI with real data - no customer/order found")
        
        return True
        
    except Exception as e:
        print(f"❌ AI model test failed: {e}")
        return False

def test_customer_support_agent():
    """Test the complete customer support system"""
    print("\n🎯 Testing Customer Support Agent with BigQuery...")
    
    try:
        from src.agents.agent import sql_customer_agent as agent
        
        test_queries = [
            "Where is my last order?",
            "What's the status of my recent purchase?",
            "What did I order recently?"
        ]
        
        customer_id = "C0001"
        success_count = 0
        
        for query in test_queries:
            print(f"\n   Testing: '{query}'")
            result = agent.process_customer_query(query, customer_id)
            
            if result["success"]:
                success_count += 1
                print(f"   ✅ Success - Response: {result['response'][:60]}...")
            else:
                print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
        
        print(f"\n✅ Customer support test: {success_count}/{len(test_queries)} queries successful")
        return success_count == len(test_queries)
        
    except Exception as e:
        print(f"❌ Customer support agent test failed: {e}")
        return False

def test_ui_compatibility():
    """Test UI component compatibility with BigQuery"""
    print("\n🖥️ Testing UI Compatibility...")
    
    try:
        from src.database.connection import db
        
        # Test functions used by UI
        customers = db.get_sample_customers_for_ui(limit=5)
        if customers:
            print(f"✅ UI customer list: {len(customers)} customers available")
            sample_customer = customers[0]
            print(f"   Sample: {sample_customer['name']} (@{sample_customer['username']})")
            
            # Test orders for UI display
            orders = db.get_customer_orders(sample_customer['_id'], limit=3)
            print(f"✅ UI orders display: {len(orders)} orders for customer")
        else:
            print("❌ No customers available for UI")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ UI compatibility test failed: {e}")
        return False

def main():
    """Run all BigQuery system tests"""
    print("🧪 BigQuery E-commerce AI Support System - Test Suite")
    print("=" * 60)
    
    tests = [
        ("BigQuery Connection", test_bigquery_connection),
        ("AI Model Integration", test_ai_model),
        ("Customer Support Agent", test_customer_support_agent),
        ("UI Compatibility", test_ui_compatibility)
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
    print("\n" + "=" * 60)
    print("📋 BIGQUERY SYSTEM TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All BigQuery tests passed! System is ready for use.")
        print("\n🚀 To start the application:")
        print("   python main.py")
        print("   or")
        print("   streamlit run src/ui/customer_chat.py")
        print("\n☁️ Your data is now running on BigQuery:")
        print("   Project: ecommerce-ai-support-system")
        print("   Dataset: ecommerce_data")
    else:
        print("⚠️  Some tests failed. Please check the configuration.")
        print("\n🔧 Common issues:")
        print("- Make sure BigQuery service account key is at config/bq-key.json")
        print("- Verify BigQuery permissions and project access")
        print("- Make sure Ollama is running: ollama serve")
        print("- Check if the AI model is downloaded: ollama pull llama3.1:8b-instruct-q4_K_M")

if __name__ == "__main__":
    main() 