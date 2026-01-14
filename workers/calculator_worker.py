"""
Calculator Worker - Matematiksel hesaplamalar yapan işçi etmen.
"""
import re

try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False


class CalculatorWorker:
    """Matematiksel hesaplamalar yapan işçi etmen."""
    
    def calculate(self, expression):
        """Güvenli matematiksel hesaplama yapar."""
        try:
            # Güvenlik: Sadece sayılar ve matematiksel operatörlere izin ver
            # Tehlikeli karakterleri temizle
            if not re.match(r'^[\d\s\+\-\*\/\(\)\.\%\*\*]+$', expression):
                return "Hatalı matematiksel ifade. Sadece sayılar ve +, -, *, /, %, ** operatörlerine izin veriliyor."
            
            # Güvenli değerlendirme
            result = eval(expression, {"__builtins__": {}}, {})
            if HAS_STREAMLIT:
                st.toast(f"🧮 Hesaplama yapıldı: {expression} = {result}")
            return str(result)
            
        except ZeroDivisionError:
            return "Hata: Sıfıra bölme yapılamaz."
        except Exception as e:
            return f"Hesaplama hatası: {str(e)}"
