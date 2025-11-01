from .utils import load_transactions, format_currency, Colors, print_color
import datetime, statistics

def show_habits():
    data = load_transactions()
    if not data:
        print_color("Belum ada data buat dianalisis.", Colors.WARNING)
        return
    expenses = [d for d in data if d.get("type")!="income"]
    if not expenses:
        print_color("Belum ada pengeluaran buat dianalisis.", Colors.WARNING)
        return
    by_cat = {}
    daily = {}
    for e in expenses:
        amt = e.get("amount",0)
        cat = e.get("category","Lainnya")
        by_cat[cat] = by_cat.get(cat,0) + amt
        d = e.get("date")
        daily[d] = daily.get(d,0) + amt
    top_cat, top_amt = max(by_cat.items(), key=lambda x: x[1])
    avg_daily = statistics.mean(daily.values()) if daily else 0
    
    print_color("===== Analisis Kebiasaan =====", Colors.HEADER)
    print(f"Kategori pengeluaran terbanyak : {Colors.BOLD}{Colors.FAIL}{top_cat}{Colors.ENDC} ({format_currency(top_amt)}{Colors.ENDC})")
    print(f"Rata-rata pengeluaran per-hari  : {format_currency(round(avg_daily))}{Colors.ENDC}")
    trend = detect_trend(sorted(daily.items()))
    
    trend_color = Colors.FAIL if trend == "Naik" else Colors.OKGREEN if trend == "Turun" else Colors.WARNING
    print(f"Tren terakhir                    : {trend_color}{Colors.BOLD}{trend}{Colors.ENDC}")
    med = statistics.median(daily.values()) if daily else 0
    print(f"Median pengeluaran per-hari     : {format_currency(round(med))}{Colors.ENDC}")
    print("")

def detect_trend(daily_items):
    if len(daily_items) < 3:
        return "Data kurang buat deteksi tren"
    vals = [v for _,v in daily_items]
    third_len = max(1,len(vals)//3)
    first = sum(vals[:third_len]) / third_len
    last = sum(vals[-third_len:]) / third_len
    if last > first * 1.15:
        return "Naik"
    if last < first * 0.85:
        return "Turun"
    return "Stabil"

def predict_end():
    data = load_transactions()
    total_in = sum(d.get("amount",0) for d in data if d.get("type")=="income")
    total_out = sum(d.get("amount",0) for d in data if d.get("type")!="income")
    today = datetime.date.today()
    first_of_month = today.replace(day=1)
    days_passed = (today - first_of_month).days + 1
    try:
        next_month = first_of_month.replace(month=first_of_month.month%12+1)
    except ValueError: 
        next_month = first_of_month.replace(year=first_of_month.year+1, month=1)
    days_in_month = (next_month - first_of_month).days
    
    avg_daily = (total_out / days_passed) if days_passed>0 else 0
    predicted_out = avg_daily * days_in_month
    balance = total_in - total_out
    predicted_balance = total_in - predicted_out
    
    balance_color = Colors.OKGREEN if balance >= 0 else Colors.FAIL
    predicted_color = Colors.OKGREEN if predicted_balance >= 0 else Colors.FAIL

    print_color("===== Prediksi Saldo Akhir Bulan =====", Colors.HEADER)
    print(f"Saldo sekarang                 : {balance_color}{format_currency(balance)}{Colors.ENDC}")
    print(f"Rata-rata pengeluaran/hari     : {format_currency(round(avg_daily))}{Colors.ENDC}")
    print(f"Perkiraan pengeluaran bulan ini: {format_currency(round(predicted_out))}{Colors.ENDC}")
    print(f"Perkiraan saldo akhir bulan      : {predicted_color}{Colors.BOLD}{format_currency(round(predicted_balance))}{Colors.ENDC}")
    print("")