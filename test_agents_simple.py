#!/usr/bin/env python
"""
Simple test to verify agents can be imported and API key is loaded
"""

print("🧪 Testing Agent Initialization...\n")

# Test 1: Check if config loads
print("1️⃣ Testing config/settings...")
try:
    from config.settings import POLLINATIONS_API_KEY, MODEL_NAME
    if POLLINATIONS_API_KEY:
        print(f"✅ Pollinations API Key loaded: {POLLINATIONS_API_KEY[:10]}...")
        print(f"✅ Model: {MODEL_NAME}")
    else:
        print("❌ Pollinations API Key is None!")
except Exception as e:
    print(f"❌ Error loading config: {e}")

# Test 2: Check LangChain imports
print("\n2️⃣ Testing LangChain imports...")
try:
    from langchain_openai import ChatOpenAI
    print("✅ langchain_openai.ChatOpenAI imported")
except Exception as e:
    print(f"❌ Error: {e}")

try:
    from langchain.prompts import ChatPromptTemplate
    print("✅ langchain.prompts imported")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Try to create a simple ChatOpenAI instance
print("\n3️⃣ Testing ChatOpenAI initialization...")
try:
    from langchain_openai import ChatOpenAI
    from config.settings import POLLINATIONS_API_KEY, MODEL_NAME
    
    llm = ChatOpenAI(
        api_key=POLLINATIONS_API_KEY,
        model=MODEL_NAME,
        temperature=0.7
    )
    print(f"✅ ChatOpenAI initialized successfully!")
    print(f"   Model: {llm.model_name}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 4: Check agent imports
print("\n4️⃣ Testing agent module imports...")
try:
    import langchain.agents
    print(f"✅ langchain.agents module loaded")
    print(f"   Available: {dir(langchain.agents)[:10]}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
print("🎯 DIAGNOSIS COMPLETE")
print("="*60)
