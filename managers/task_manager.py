"""
Task Manager - Görevi analiz edip yönlendiren ve arama terimini bulan yönetici.
"""
from langchain_core.messages import HumanMessage, SystemMessage
from config.settings import llm
from workers import WikiWorker, CalculatorWorker, WebSearchWorker

try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False


class TaskManager:
    """Görevi analiz edip yönlendiren ve arama terimini bulan yönetici."""
    
    def __init__(self):
        self.wiki_worker = WikiWorker()
        self.calc_worker = CalculatorWorker()
        self.web_worker = WebSearchWorker()
    
    def decide_and_run(self, user_query, conversation_history=""):
        """Kullanıcı sorgusunu analiz eder ve ilgili worker'ı çalıştırır."""
        # Akış takibi için liste
        flow_steps = []
        
        # Adım 1: Task Manager karar veriyor
        flow_steps.append({
            "agent": "🔍 TASK MANAGER",
            "action": "Sorguyu analiz ediyor",
            "detail": "LLM ile kategori belirleniyor (WIKI/SEARCH/CALC/CHAT)"
        })
        
        system_instruction = f"""
        Sen bir Karar Mekanizmasısın.
        Kullanıcının girdisini analiz et ve hangi agent'ın çalışması gerektiğini belirle.
        
        Konuşma Geçmişi:
        {conversation_history}
        
        KATEGORİLER:
        1. CHAT → Sadece sohbet (Merhaba, nasılsın vb.)
        2. WIKI: [konu] → Wikipedia'dan bilgi (Tarih, coğrafya, kişi vb.)
        3. CALC: [ifade] → Matematik hesaplama (25*48, 100+50 vb.)
        4. SEARCH: [sorgu] → Güncel bilgi için web araması (hava durumu, dolar kuru, haberler vb.)
        
        KURALLAR:
        - Cevabın formatı: "KATEGORİ" veya "KATEGORİ: terim"
        - Matematik soruları → CALC
        - Güncel bilgi (bugün, şimdi, son haberler) → SEARCH
        - Genel bilgi (tarih, tanım, açıklama) → WIKI
        - Konuşma geçmişindeki BAĞLAMI dikkate al
        - **ÖNEMLİ**: WIKI kategorisi için sadece ANA KONU başlığını ver (tarihçesi, özellikleri gibi eklentiler ekleme!)
           
        Örnekler:
        - "nasılsın" → CHAT
        - "Türkiye nedir" → WIKI: Türkiye
        - "domatesin tarihçesini anlat" → WIKI: domates
        - "İstanbul'un tarihi hakkında bilgi ver" → WIKI: İstanbul
        - "25 çarpı 48 kaç eder" → CALC: 25*48
        - "Bugün hava nasıl" → SEARCH: bugün hava durumu
        - "Dolar kuru nedir" → SEARCH: dolar kuru
        - "Python dili nedir" → WIKI: Python (programlama dili)
        - [Geçmişte İstanbul soruldu] "nerede peki?" → WIKI: İstanbul
        """
        
        # LLM'e soruyoruz: Bu nedir ve aranacak kelime ne?
        response = llm.invoke([SystemMessage(content=system_instruction), HumanMessage(content=user_query)])
        decision = response.content.strip()
        
        # Güvenlik kontrolü: Çok uzun decision'ı kısalt
        if len(decision) > 100:
            if HAS_STREAMLIT:
                st.warning(f"⚠️ LLM çok uzun yanıt döndürdü ({len(decision)} karakter), kısaltılıyor...")
            decision = decision[:100]
        
        # Kategoriye göre ilgili worker'ı çağır
        if decision.startswith("WIKI:"):
            topic = decision.replace("WIKI:", "").strip()
            flow_steps.append({
                "agent": "📚 WIKI WORKER",
                "action": f"Wikipedia'da '{topic}' aranıyor",
                "detail": "TR Wikipedia API üzerinden bilgi çekiliyor"
            })
            if HAS_STREAMLIT:
                st.toast(f"📚 Wiki Worker: '{topic}' aranıyor...")
            result = self.wiki_worker.search(topic)
            return ("WIKI", result, flow_steps)
        
        elif decision.startswith("CALC:"):
            expression = decision.replace("CALC:", "").strip()
            flow_steps.append({
                "agent": "🧮 CALCULATOR WORKER",
                "action": f"'{expression}' hesaplanıyor",
                "detail": "Python eval() ile güvenli hesaplama"
            })
            if HAS_STREAMLIT:
                st.toast(f"🧮 Calculator Worker: '{expression}' hesaplanıyor...")
            result = self.calc_worker.calculate(expression)
            return ("CALC", result, flow_steps)
        
        elif decision.startswith("SEARCH:"):
            query = decision.replace("SEARCH:", "").strip()
            flow_steps.append({
                "agent": "🔍 WEB SEARCH WORKER",
                "action": f"'{query}' web'de aranıyor",
                "detail": "Tavily API ile güncel bilgi toplanıyor"
            })
            if HAS_STREAMLIT:
                st.toast(f"🔍 Web Search Worker: '{query}' aranıyor...")
            result = self.web_worker.search(query)
            return ("SEARCH", result, flow_steps)
        
        elif decision == "CHAT":
            flow_steps.append({
                "agent": "💬 CHAT MODE",
                "action": "Sohbet moduna geçiliyor",
                "detail": "Worker kullanılmadan direkt LLM'e gönderiliyor"
            })
            return ("CHAT_MODE", None, flow_steps)
        
        else:
            # Fallback: Eğer format belli değilse Wikipedia'da ara
            flow_steps.append({
                "agent": "📚 WIKI WORKER (Fallback)",
                "action": f"'{decision}' aranıyor",
                "detail": "Kategori belirlenemedi, Wikipedia'ya yönlendiriliyor"
            })
            if HAS_STREAMLIT:
                st.toast(f"📚 Wiki Worker (fallback): '{decision}' aranıyor...")
            result = self.wiki_worker.search(decision)
            return ("WIKI", result, flow_steps)
