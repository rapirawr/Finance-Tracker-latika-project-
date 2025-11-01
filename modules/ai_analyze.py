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
    client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None
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
    
    BOLD = Colors.BOLD
    GREEN = Colors.OKGREEN
    RED = Colors.FAIL
    ENDC = Colors.ENDC
    YELLOW = Colors.WARNING
    
    analysis.append(f"\n{BOLD}{GREEN}**RINGKASAN KEUANGAN (SIMULASI)**{ENDC}")
    
    if balance > 0 and balance >= total_in * 0.2:
        analysis.append(f"* {GREEN}🟢 Posisi Keuangan Sangat Baik:{ENDC} Anda berhasil menyimpan 20%+ dari pemasukan. Keren!{ENDC}")
    elif balance > 0:
        analysis.append(f"* {YELLOW}🟡 Posisi Keuangan Sehat:{ENDC} Saldo Anda positif ({format_currency(balance)}{ENDC}). Pertahankan!{ENDC}")
    else:
        analysis.append(f"* {RED}🔴 Peringatan Saldo:{ENDC} Saldo Anda negatif ({format_currency(balance)}{ENDC}). Butuh review segera. Jangan sampai over budget, bro!{ENDC}")
        
    analysis.append(f"\n{BOLD}{YELLOW}**SARAN GEMINI AI (SIMULASI)**{ENDC}")
    
    if by_cat:
        top_cat, top_amt = max(by_cat.items(), key=lambda x: x[1])
        analysis.append(f"* {RED}Cek Pengeluaran Terbesar:{ENDC} Fokus ke {top_cat}. Porsinya gede banget, coba cari alternatif yang lebih murah.{ENDC}")
    
    analysis.append(f"* {GREEN}Tips Umum:{ENDC} Coba alokasikan 50% untuk kebutuhan, 30% untuk keinginan, dan 20% untuk tabungan/investasi. Kalau ini udah oke, berarti kamu udah pro!{ENDC}")

    analysis.append(f"\n{BOLD}NOTE:{ENDC} Coba tambahkan lebih banyak data untuk analisis yang lebih mendalam saat API diaktifkan.")
    
    return "\n".join(analysis)


def get_ai_analysis(financial_data_json):
    
    data = json.loads(financial_data_json)
    
    ANSI_CODES_PROMPT = {
        "BOLD": "\\\\033[1m",
        "GREEN": "\\\\033[92m",
        "RED": "\\\\033[91m",
        "YELLOW": "\\\\033[93m",
        "RESET": "\\\\033[0m"
    }

    if client:
        try:
            print_color("--- Waiting Gemini API response... ---", Colors.OKCYAN)
            
            prompt = f"""
            Analisis data keuangan berikut dalam bahasa Indonesia. Berikan ringkasan dan 2-3 saran spesifik. Berbicara seperti anggota Gen Z. Sampaikan apa adanya; tanpa mempermanis respons. Inovatif dan berpikir di luar kebiasaan.

            **INSTRUKSI FORMAT KHUSUS:**
            1. **JANGAN** gunakan karakter Markdown seperti `**` untuk bold. Gantilah dengan kode ANSI **{ANSI_CODES_PROMPT['BOLD']}** di awal dan **{ANSI_CODES_PROMPT['RESET']}** di akhir teks yang ingin di-bold.
            2. Gunakan kode warna ANSI untuk penekanan: **{ANSI_CODES_PROMPT['GREEN']}** untuk hal positif/saldo baik, **{ANSI_CODES_PROMPT['RED']}** untuk peringatan/masalah besar, dan **{ANSI_CODES_PROMPT['YELLOW']}** untuk perhatian/perlu diulas.
            3. Pisahkan bagian Ringkasan dan Saran dengan Heading yang di-bold dan berwarna (misal: **{ANSI_CODES_PROMPT['BOLD']}{ANSI_CODES_PROMPT['GREEN']}**RINGKASAN KEUANGAN**{ANSI_CODES_PROMPT['RESET']}**).
            4. Rapikan respons dengan bullet point (`*`) agar mudah dibaca di terminal.

            **Data Keuangan:**
            Total Pemasukan: {format_currency(data['total_income'])}, 
            Total Pengeluaran: {format_currency(data['total_expense'])}, 
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
            
    # Fallback ke simulasi
    return call_gemini_api_simulasi(financial_data_json)


def run_ai_analysis():
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
    
    print(f"Pemasukan Total : {Colors.OKGREEN}{format_currency(total_in)}{Colors.ENDC}")
    print(f"Pengeluaran Total: {Colors.FAIL}{format_currency(total_out)}{Colors.ENDC}")
    
    saldo = total_in - total_out
    saldo_color = Colors.OKGREEN if saldo >= 0 else Colors.FAIL
    print(f"Saldo Saat Ini  : {saldo_color}{format_currency(saldo)}{Colors.ENDC}")
    
    print_color("\n--- AI sedang menganalisis data Anda... ini mungkin butuh waktu... ---", Colors.OKCYAN)

    try:
        data_json = json.dumps(financial_data)
        ai_response = get_ai_analysis(data_json) 
        
        formatted_response = ai_response.encode('utf-8').decode('unicode_escape')
        
        print_color("\n===== Hasil Analisis Gemini AI =====", Colors.OKBLUE)
        print(formatted_response)
        print_color("======================================", Colors.OKBLUE)
        
    except Exception as e:
        print_color(f"❌ Error saat menjalankan analisis: {e}", Colors.FAIL)