from .utils import load_transactions, format_currency, clear, Colors, print_color
from .summary import summarize_transactions
import time
import json
import os
from dotenv import load_dotenv

load_dotenv() 

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

try:
    from google import genai
    if GEMINI_API_KEY:
        client = genai.Client(api_key=GEMINI_API_KEY)
    else:
        client = None 
except ImportError:
    client = None
except Exception:
    client = None

def call_gemini_api_simulasi(financial_data):
    
    data = json.loads(financial_data)
    total_in = data.get("total_income", 0)
    total_out = data.get("total_expense", 0)
    balance = total_in - total_out
    by_cat = data.get("expense_breakdown", {})
    
    time.sleep(1.5) 
    
    analysis = []
    
    analysis.append("\n**Kesimpulan Gemini AI (Simulasi):**")
    if balance > 0 and balance >= total_in * 0.2:
        analysis.append(f"🟢 Posisi Keuangan Sangat Baik: Anda berhasil menyimpan 20%+ dari pemasukan.")
    elif balance > 0:
        analysis.append(f"🟡 Posisi Keuangan Sehat: Saldo Anda positif ({format_currency(balance)}{Colors.ENDC}).")
    else:
        analysis.append(f"🔴 Peringatan Saldo: Saldo Anda negatif ({format_currency(balance)}{Colors.ENDC}). Butuh review segera.")
    
    analysis.append("Coba tambahkan lebih banyak data untuk analisis yang lebih mendalam saat API diaktifkan.")
    
    return "\n".join(analysis)


def get_ai_analysis(financial_data_json):
    
    data = json.loads(financial_data_json)
    
    if client:
        try:
            print_color("--- Memanggil Gemini API Nyata... ---", Colors.OKCYAN)
            
            prompt = f"""
            Analisis data keuangan berikut dalam bahasa Indonesia. Berikan ringkasan dan 2-3 saran spesifik. 
            Data: Total Pemasukan: {data['total_income']}, Total Pengeluaran: {data['total_expense']}, 
            Breakdown Pengeluaran: {json.dumps(data['expense_breakdown'])}.
            """
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[prompt]
            )
            return response.text
            
        except Exception as e:
            print_color(f"❌ Gemini API gagal: {e}. Menggunakan mode simulasi.", Colors.FAIL)
            pass
            
    return call_gemini_api_simulasi(financial_data_json)


def ai_financial_analysis():
    data = load_transactions()
    if not data:
        print_color("Belum ada data untuk dianalisis oleh AI.", Colors.WARNING)
        return

    clear()
    print_color("╔════════════════════════════════════════╗", Colors.HEADER)
    print_color("║          🤖 ANALISIS KEUANGAN AI       ║", Colors.HEADER)
    print_color("╚════════════════════════════════════════╝", Colors.HEADER)

    total_in, total_out, by_cat = summarize_transactions(data)

    financial_data = {
        "total_income": total_in,
        "total_expense": total_out,
        "expense_breakdown": by_cat
    }
    
    print(f"Pemasukan Total : {format_currency(total_in)}{Colors.ENDC}")
    print(f"Pengeluaran Total: {format_currency(total_out)}{Colors.ENDC}")
    print(f"Saldo Saat Ini  : {format_currency(total_in - total_out)}{Colors.ENDC}")
    
    print_color("\n--- AI sedang menganalisis data Anda... ini mungkin butuh waktu singkat. ---", Colors.OKCYAN)

    try:
        data_json = json.dumps(financial_data)
        ai_response = get_ai_analysis(data_json) 
        
        print_color("\n===== Hasil Analisis Gemini AI =====", Colors.OKBLUE)
        print(ai_response) 
        print_color("======================================", Colors.OKBLUE)
        
    except Exception as e:
        print_color(f"❌ Error saat menjalankan analisis: {e}", Colors.FAIL)
