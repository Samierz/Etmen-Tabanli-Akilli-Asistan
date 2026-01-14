"""
Agentic AI Asistan - Ana Uygulama (Streamlit UI)
Modüler mimari: Config, Workers, Managers
"""
import streamlit as st
from datetime import datetime
from config.settings import llm, tavily, GOOGLE_API_KEY, TAVILY_API_KEY
from managers import Coordinator

# API Key Kontrolü
if not GOOGLE_API_KEY or not llm:
    st.error("❌ HATA: GOOGLE_API_KEY bulunamadı! Lütfen .env dosyanızı kontrol edin.")
    st.stop()

if not TAVILY_API_KEY or not tavily:
    st.error("❌ HATA: TAVILY_API_KEY bulunamadı! Lütfen .env dosyanızı kontrol edin.")
    st.stop()

# --- ARAYÜZ (Streamlit) ---

st.set_page_config(page_title="Agentic AI Asistan", page_icon="🤖")
st.title("🤖 Etmen Tabanlı Akıllı Asistan")
st.caption("Mimari: Coordinator -> Task Manager -> Worker")

# Hafıza (Session State)
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Merhaba! Ben akıllı asistanınım. Bir şey merak ediyorsan sorabilirsin."}]

# Coordinator'ı session state'te tut (performans için)
if "coordinator" not in st.session_state:
    st.session_state["coordinator"] = Coordinator()

# Agent akış geçmişi
if "agent_flow" not in st.session_state:
    st.session_state["agent_flow"] = []

# --- SIDEBAR: Agent İzleme Paneli ---
with st.sidebar:
    st.header("🔍 Agentic Akış İzleyici")
    st.caption("Her sorgunun sistem içinde nasıl işlendiğini görün")
    
    if st.session_state["agent_flow"]:
        st.divider()
        for i, flow_item in enumerate(reversed(st.session_state["agent_flow"][-3:]), 1):  # Son 3 sorgu
            query_num = len(st.session_state['agent_flow']) - i + 1
            with st.expander(f"🔎 Sorgu #{query_num}: {flow_item['query'][:30]}...", expanded=(i==1)):
                st.caption(f"🕐 {flow_item['timestamp']} | Son Agent: {flow_item['agent']}")
                st.markdown("---")
                
                # Akış adımlarını göster
                st.markdown("**📋 Akış Timeline:**")
                for step_num, step in enumerate(flow_item.get('flow_steps', []), 1):
                    st.markdown(f"""
                    **{step_num}.** {step['agent']}  
                    → *{step['action']}*  
                    <small style='color: gray;'>{step['detail']}</small>
                    """, unsafe_allow_html=True)
                    if step_num < len(flow_item.get('flow_steps', [])):
                        st.markdown("↓")
    else:
        st.info("💡 Henüz sorgu yok. Bir soru sorarak başlayın!")
    
    st.divider()
    st.subheader("🤖 Agent Mimarisi")
    st.markdown("""
    **Akış Şeması:**
    1. 🧠 **Coordinator**: Ana yönetici
    2. 🔍 **Task Manager**: Karar verici
    3. ⚙️ **Worker** (Wiki/Search/Calc): İşi yapan
    4. 🤖 **LLM**: Yanıt oluşturucu
    """)

# Eski mesajları ekrana bas
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Kullanıcıdan Girdi Al
if user_input := st.chat_input("Sorunuzu buraya yazın..."):
    # 1. Kullanıcı mesajını ekrana bas ve kaydet
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)
    
    # 2. Coordinator'ı session state'ten al
    coordinator = st.session_state["coordinator"]
    
    # 3. Konuşma geçmişini hazırla (son 3 soru-cevap = 6 mesaj)
    recent_messages = st.session_state.messages[-6:]  # Son 6 mesaj
    conversation_history = "\n".join([
        f"{msg['role'].upper()}: {msg['content'][:200]}..." if len(msg['content']) > 200 else f"{msg['role'].upper()}: {msg['content']}"
        for msg in recent_messages
    ])
    
    with st.spinner("Koordinatör düşünüyor..."):
        result = coordinator.generate_response(user_input, conversation_history)
        
        # Sonuç tuple mı yoksa string mi kontrol et
        if isinstance(result, tuple) and len(result) >= 4:
            ai_response, agent_type, agent_details, flow_steps = result
        elif isinstance(result, tuple) and len(result) == 3:
            # Eski format (flow_steps yok)
            ai_response, agent_type, agent_details = result
            flow_steps = []
        else:
            # Eski formatla uyumluluk için
            ai_response = result
            agent_type = "❓ BİLİNMEYEN"
            agent_details = "Agent bilgisi alınamadı"
            flow_steps = []
    
    # Agent akışını kaydet (flow_steps ile birlikte)
    from datetime import datetime
    st.session_state["agent_flow"].append({
        "query": user_input,
        "agent": agent_type,
        "details": agent_details,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "flow_steps": flow_steps  # Detaylı akış bilgisi
    })
    
    # 3. Cevabı ekrana bas ve kaydet
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    
    # Agent bilgisini göster
    st.chat_message("assistant").write(ai_response)
    with st.chat_message("assistant"):
        st.caption(f"🤖 **Son Agent:** {agent_type} | {agent_details}")
    
    # Sidebar'ı otomatik güncelle
    st.rerun()
