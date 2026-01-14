"""
Web Search Worker - Web'den güncel bilgi arayan işçi etmen.
Tavily AI Search kullanır.
"""
from config.settings import tavily

try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False


class WebSearchWorker:
    """Web'den güncel bilgi arayan işçi etmen - Tavily AI Search."""
    
    def __init__(self):
        self.cache = {}  # Basit cache sistemi
    
    def search(self, query):
        """Tavily AI Search kullanarak arama yapar."""
        
        # Cache kontrolü
        if query in self.cache:
            if HAS_STREAMLIT:
                st.toast(f"✅ Cache'ten getiriliyor: {query}")
            return self.cache[query]
        
        try:
            if HAS_STREAMLIT:
                st.toast(f"🔍 Tavily AI ile aranıyor: {query}")
            
            # Tavily search (max 5 sonuç, advanced depth ile daha güncel!)
            response = tavily.search(
                query=query,
                max_results=5,
                search_depth="advanced"
            )
            
            # Sonuçları formatla
            if not response or 'results' not in response or not response['results']:
                return "(Arama sonucu bulunamadı)"
            
            formatted_results = []
            for result in response['results']:
                title = result.get('title', '')
                content = result.get('content', '')
                url = result.get('url', '')
                
                if not title or not content:
                    continue
                
                # URL'den domain çıkar
                source = ""
                if url:
                    try:
                        from urllib.parse import urlparse
                        domain = urlparse(url).netloc.replace('www.', '')
                        source = f" (Kaynak: {domain})"
                    except:
                        pass
                
                formatted_results.append(f"• **{title}**{source}\n  {content}")
                
                if len(formatted_results) >= 5:
                    break
            
            if not formatted_results:
                return "(İşlenebilir sonuç bulunamadı)"
            
            result_text = "\n\n".join(formatted_results)
            
            # Cache'e kaydet
            self.cache[query] = result_text
            if HAS_STREAMLIT:
                st.toast(f"✅ Tavily araması tamamlandı: {len(formatted_results)} sonuç")
            
            return result_text
            
        except Exception as e:
            if HAS_STREAMLIT:
                st.toast(f"⚠️ Arama hatası: {str(e)[:50]}")
            return f"(Arama hatası: {str(e)[:100]})"
