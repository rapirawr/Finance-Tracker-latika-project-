from .utils import load_transactions, format_currency, clear, Colors, print_color
from .summary import summarize_transactions
import time
import json

from google import genai
client = genai.Client(api_key="AIzaSyAhjZxdt6MRM_pI0BPr_-BlO1ji3qZRv1U")
def call_gemini_api(prompt):
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[prompt]
    )
    return response.text

def call_gemini_api_placeholder(financial_data):
    
    data = json.loads(financial_data)
    total_in = data.get("total_income", 0)
    total_out = data.get("total_expense", 0)
    balance = total_in - total_out
    by_cat = data.get("expense_breakdown", {})
    
    time.sleep(2) 
    
    analysis = []
    
    if balance > 0 and balance >= total_in * 0.2:
        analysis.append(f"🟢 **Posisi Keuangan Sangat Baik:** Saldo Anda positif dan berhasil menyimpan lebih dari 20% dari total pemasukan. Ini adalah indikasi *budgeting* yang kuat.")
    elif balance > 0:
        analysis.append(f"🟡 **Posisi Keuangan Sehat:** Saldo Anda positif ({format_currency(balance)}{Colors.ENDC}). Terus pertahankan momentum ini.")
    else:
        analysis.append(f"🔴 **Peringatan Saldo:** Saldo Anda negatif ({format_currency(balance)}{Colors.ENDC}) atau mendekati nol. Ini perlu perhatian serius.")

    if by_cat:
        top_cat, top_amt = max(by_cat.items(), key=lambda item: item[1])
        total_expense = sum(by_cat.values())
        perc = (top_amt / total_expense) * 100
        
        analysis.append(f"\n**Fokus Pengeluaran:** Kategori **'{top_cat}'** adalah yang terbesar, menyumbang **{perc:.0f}%** dari total pengeluaran.")
        
        if perc > 40:
             analysis.append(f"💡 **Saran Khusus:** Persentase pengeluaran {top_cat} sangat tinggi. Prioritaskan mencari alternatif hemat atau batasi pengeluaran di kategori ini.")
        elif perc > 20:
             analysis.append(f"💡 **Saran Khusus:** Pengeluaran {top_cat} masih dominan. Cek ulang apakah ada pemborosan kecil harian di kategori ini.")
             

    return "\n".join(analysis)


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
        ai_response = call_gemini_api_placeholder(data_json) 
        
        print_color(ai_response, Colors.ENDC) 
        print_color("======================================", Colors.OKBLUE)
        
    except Exception as e:
        print_color(f"❌ Error saat memanggil AI: {e}", Colors.FAIL)