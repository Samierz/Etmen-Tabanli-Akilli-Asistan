"""
Coordinator - Kullanıcıyla konuşan ana etmen.
"""
from langchain_core.messages import HumanMessage
from config.settings import llm
from .task_manager import TaskManager


class Coordinator:
    """Kullanıcıyla konuşan ana etmen."""
    
    def __init__(self):
        self.manager = TaskManager()
    
    def generate_response(self, user_input, conversation_history=""):
        """Kullanıcı girdisine yanıt oluşturur."""
        # Akış başlangıcı
        flow_steps = [{
            "agent": "🧠 COORDINATOR",
            "action": "Sorgu alındı",
            "detail": f"Kullanıcı sorusu: '{user_input[:50]}...'"
        }]
        
        # 1. Task Manager'a sor (konuşma geçmişiyle birlikte)
        manager_result = self.manager.decide_and_run(user_input, conversation_history)
        
        # Manager'dan gelen akış adımlarını ekle
        if isinstance(manager_result, tuple) and len(manager_result) >= 3:
            worker_type, worker_data, manager_flow = manager_result
            flow_steps.extend(manager_flow)
        else:
            # Eski format desteği
            worker_type = "UNKNOWN"
            worker_data = manager_result
            manager_flow = []
        
        # Agent takip bilgisi
        agent_type = None
        agent_details = ""
        
        # 2. Sonucu işle
        if worker_type == "CHAT_MODE":
            agent_type = "💬 CHAT"
            agent_details = "Sohbet modu - Direkt LLM yanıtı"
            flow_steps.append({
                "agent": "🤖 LLM (Gemini)",
                "action": "Sohbet yanıtı oluşturuluyor",
                "detail": "Konuşma geçmişi kullanılarak doğal dil yanıtı"
            })
            # Sohbet modu
            final_prompt = f"""
            Konuşma Geçmişi:
            {conversation_history}
            
            Kullanıcı: {user_input}
            
            Konuşma geçmişini dikkate alarak nazik bir şekilde cevap ver.
            """
        
        elif worker_type == "CALC":
            agent_type = "🧮 CALCULATOR"
            agent_details = "Matematiksel hesaplama yapıldı"
            # Hesaplama sonucu direkt döndür
            return (f"📊 Hesaplama Sonucu: {worker_data}", agent_type, agent_details, flow_steps)
        
        elif worker_type == "SEARCH":
            agent_type = "🔍 WEB SEARCH"
            agent_details = "Tavily üzerinden web araması yapıldı"
            flow_steps.append({
                "agent": "🤖 LLM (Gemini)",
                "action": "Web sonuçlarını özetliyor",
                "detail": "Ham veri özetleniyor"
            })
            # Web arama sonucunu LLM ile özetle
            final_prompt = f"""
            Kullanıcı sorusu: {user_input}
            Web araması sonuçları:
            {worker_data}
            
            Görevin: Bu web arama sonuçlarını kullanarak kullanıcıya özetlenmiş, Türkçe bir cevap ver.
            ÖNEMLİ: Kaynaklara atıfta bulun.
            """
        
        elif worker_type == "WIKI":
            agent_type = "📚 WIKIPEDIA"
            agent_details = "Wikipedia Türkçe'den bilgi alındı"
            flow_steps.append({
                "agent": "🤖 LLM (Gemini)",
                "action": "Wikipedia verisini işliyor",
                "detail": "Ham veri kullanıcı dostu yanıta dönüştürülüyor"
            })
            final_prompt = f"""
            Konuşma Geçmişi:
            {conversation_history}
            
            Kullanıcı sorusu: {user_input}
            Wikipedia'dan gelen ham veri: {worker_data}
            
            Görevin: Bu ham veriyi kullanarak kullanıcıya nazik, kibar ve Türkçe bir cevap ver.
            ÖNEMLİ: Konuşma geçmişini dikkate al, tutarlı ol.
            ÖNEMLİ KURAL: Cevabın minimum 5 cümle olsun. Çok da uzatma.
            ÖNEMLİ KURAL 2: Ne zaman, nerede gibi sorular gelirse konu başlığını anlatma, soruyu cevapla.
            """
        else:
            # Fallback
            agent_type = "❓ UNKNOWN"
            agent_details = "Bilinmeyen işlem"
            final_prompt = f"Kullanıcı: {user_input}"

        try:
            response = llm.invoke([HumanMessage(content=final_prompt)])
            return (response.content, agent_type, agent_details, flow_steps)
        except Exception as e:
            return (f"Üzgünüm, bir hata oluştu: {str(e)}", "❌ HATA", str(e), flow_steps)
