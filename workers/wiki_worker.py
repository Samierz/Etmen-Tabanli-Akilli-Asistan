"""
Wikipedia Worker - Wikipedia'dan bilgi çeken işçi etmen.
"""
import wikipedia

try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False


class WikiWorker:
    """Wikipedia'dan bilgi çeken işçi etmen."""
    
    def __init__(self):
        self.cache = {}  # Cache sistemi: {query: result}
    
    def search(self, query):
        """Wikipedia'da kelime arar ve özet döner."""
        # Cache kontrolü
        if query in self.cache:
            if HAS_STREAMLIT:
                st.toast(f"✅ Cache'ten getiriliyor: {query}")
            return self.cache[query]
        
        try:
            wikipedia.set_lang("tr")
            summary = wikipedia.summary(query, sentences=2)
            
            # Sonucu cache'e kaydet
            self.cache[query] = summary
            if HAS_STREAMLIT:
                st.toast(f"🌐 Wikipedia'dan yeni veri alındı: {query}")
            return summary 

        except wikipedia.exceptions.DisambiguationError as e:
            # Agentic davranış: İlk seçeneği otomatik ara
            first_option = e.options[0]
            return self.search(first_option) 

        except wikipedia.exceptions.PageError:
            return "Aradığınız konuyla ilgili Wikipedia sayfası bulunamadı."
