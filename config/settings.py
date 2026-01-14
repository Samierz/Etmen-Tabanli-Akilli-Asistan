"""
Merkezi konfigürasyon modülü.
API key'leri yükler ve LLM/Tavily client'ları başlatır.
"""
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient

# Environment variables yükle
load_dotenv()

# API Key'leri al
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Gemini LLM (LangChain) - SADECE key varsa oluştur
llm = None
if GOOGLE_API_KEY:
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-2.5-flash-lite",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.2
    )

# Tavily Search Client - SADECE key varsa oluştur
tavily = None
if TAVILY_API_KEY:
    tavily = TavilyClient(api_key=TAVILY_API_KEY)
