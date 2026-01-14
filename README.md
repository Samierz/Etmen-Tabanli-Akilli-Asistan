
# 🤖 Etmen Tabanlı Akıllı Asistan

Modüler mimari ile tasarlanmış, çok amaçlı yapay zeka asistanı. Gemini AI, Wikipedia ve Tavily Search entegrasyonları ile donatılmış agentic sistem.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![LangChain](https://img.shields.io/badge/LangChain-Latest-green.svg)

## ✨ Özellikler

- 🧠 **Akıllı Görev Analizi**: LLM tabanlı intent classification
- 📚 **Wikipedia Entegrasyonu**: Türkçe bilgi arama ve cache sistemi
- 🔍 **Web Araması**: Tavily AI ile güncel bilgi erişimi
- 🧮 **Hesap Makinesi**: Güvenli matematiksel hesaplamalar
- 💬 **Doğal Dil İşleme**: Konuşma geçmişi ile bağlamsal yanıtlar
- 📊 **Agent Flow Tracking**: Gerçek zamanlı sistem izleme

## 🏗️ Mimari

Proje **katmanlı mimari** prensipleriyle tasarlanmıştır:

```
┌─────────────────────────────────────────┐
│          Streamlit UI (app.py)          │
├─────────────────────────────────────────┤
│         Coordinator (Manager)           │
├─────────────────────────────────────────┤
│          Task Manager (Router)          │
├─────────────────────────────────────────┤
│    Wiki Worker │ Calc Worker │ Web Worker
└─────────────────────────────────────────┘
```

### Katmanlar

1. **Config Layer** (`config/`)
   - API key yönetimi
   - LLM ve Tavily client initialization

2. **Workers Layer** (`workers/`)
   - `WikiWorker`: Wikipedia API entegrasyonu
   - `CalculatorWorker`: Matematiksel işlemler
   - `WebSearchWorker`: Tavily search integration

3. **Managers Layer** (`managers/`)
   - `TaskManager`: Intent classification ve routing
   - `Coordinator`: Ana kontrol akışı

4. **UI Layer** (`app.py`)
   - Streamlit web arayüzü
   - Session state yönetimi

## 📦 Kurulum

### Gereksinimler

- Python 3.10+
- Google Gemini API Key
- Tavily API Key

### Adımlar

1. **Projeyi klonlayın**
```bash
git clone <repository-url>
cd Etmen_Projesi
```

2. **Virtual environment oluşturun**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Bağımlılıkları yükleyin**
```bash
pip install streamlit langchain-google-genai tavily-python wikipedia python-dotenv
```

4. **Environment değişkenlerini ayarlayın**

`.env` dosyası oluşturun:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

API key'lerinizi şu kaynaklardan alabilirsiniz:
- [Google AI Studio](https://aistudio.google.com/app/apikey) - Gemini API
- [Tavily](https://tavily.com/) - Search API

## 🚀 Kullanım

Uygulamayı başlatın:

```bash
streamlit run app.py
```

Tarayıcınızda `http://localhost:8501` adresine gidin.

### Kullanım Örnekleri

#### 💬 Sohbet
```
Kullanıcı: Merhaba, nasılsın?
Asistan: [Sohbet modu aktif]
```

#### 📚 Wikipedia Sorguları
```
Kullanıcı: İstanbul hakkında bilgi ver
Asistan: [Wiki Worker çalışır]
```

#### 🧮 Hesaplamalar
```
Kullanıcı: 25 çarpı 48 kaç eder?
Asistan: [Calculator Worker çalışır]
```

#### 🔍 Güncel Bilgi
```
Kullanıcı: Bugün dolar kuru nedir?
Asistan: [Web Search Worker çalışır]
```

## 📁 Proje Yapısı

```
Etmen_Projesi/
├── config/
│   ├── __init__.py          # Config modülü exports
│   └── settings.py          # API key ve client initialization
│
├── workers/
│   ├── __init__.py          # Workers exports
│   ├── wiki_worker.py       # Wikipedia worker
│   ├── calculator_worker.py # Hesap makinesi worker
│   └── web_search_worker.py # Web search worker
│
├── managers/
│   ├── __init__.py          # Managers exports
│   ├── task_manager.py      # Intent classification & routing
│   └── coordinator.py       # Ana koordinatör
│
├── app.py                   # Streamlit UI
├── .env                     # Environment variables (git'e eklenmez)
├── .gitignore              # Git ignore rules
└── README.md               # Bu dosya
```

## ⚙️ Konfigürasyon

### Model Ayarları

`config/settings.py` dosyasında model parametrelerini değiştirebilirsiniz:

```python
llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash-lite",  # Model seçimi
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2  # Yaratıcılık seviyesi (0-1)
)
```

### Desteklenen Modeller

- `gemini-2.5-flash-lite` (varsayılan - hızlı)
- `gemini-1.5-flash` (dengeli)
- `gemini-1.5-pro` (güçlü)

## 🔧 Geliştirme

### Worker Ekleme

Yeni bir worker eklemek için:

1. `workers/` klasöründe yeni dosya oluşturun
2. Worker sınıfını tanımlayın
3. `workers/__init__.py`'ye ekleyin
4. `TaskManager`'da routing logic ekleyin

Örnek:

```python
# workers/translator_worker.py
class TranslatorWorker:
    def translate(self, text, target_lang):
        # Translation logic
        pass
```

### Test Etme

Worker'ları bağımsız test edebilirsiniz:

```python
from workers import CalculatorWorker

calc = CalculatorWorker()
result = calc.calculate("25*48")
assert result == "1200"
```

## 🧪 Özellikler

### Cache Sistemi

- Wikipedia ve web search sonuçları cache'lenir
- Aynı sorgu tekrar aratılmaz (performans optimizasyonu)
- Session süresince geçerli

### Agent Flow Tracking

Sidebar'da her sorgunun sistem içinde nasıl işlendiğini görebilirsiniz:
1. Coordinator → Sorgu alındı
2. Task Manager → Intent belirlendi
3. Worker → İşlem yapıldı
4. LLM → Yanıt oluşturuldu

## 🐛 Sorun Giderme

### "503 UNAVAILABLE" hatası
```
Google API geçici olarak yoğun. Birkaç saniye bekleyip tekrar deneyin.
```

### "ModuleNotFoundError: streamlit"
```bash
pip install streamlit
```

### API Key bulunamadı
```
.env dosyasının proje kök dizininde olduğundan ve key'lerin doğru girildiğinden emin olun.
```

## 📊 Performans

- Cache hit rate: ~80% (tekrarlayan sorgularda)
- Ortalama yanıt süresi: 2-3 saniye
- Memory footprint: ~200MB

## 🔐 Güvenlik

- API key'ler `.env` dosyasında saklanır (git'e eklenmez)
- Hesap makinesi güvenli `eval()` kullanır
- Input validation tüm worker'larda aktif


