from .utils import load_transactions, format_currency, Colors, print_color
import statistics, datetime

def show_suggestions():
    data = load_transactions()
    if not data:
        print_color("Belum ada data buat kasih saran.", Colors.WARNING)
        return
    expenses = [d for d in data if d.get("type")!="income"]
    if not expenses:
        print_color("Belum ada pengeluaran buat dianalisis.", Colors.WARNING)
        return
    by_cat = {}
    weekly = {}
    for e in expenses:
        amt = e.get("amount",0)
        cat = e.get("category","Lainnya")
        by_cat[cat] = by_cat.get(cat,0) + amt
        dt = e.get("date")
        wk = week_of_month(dt)
        weekly[wk] = weekly.get(wk,0) + amt
    suggestions = []
    total = sum(by_cat.values())
    if total == 0:
        print_color("Pengeluaran nol, gak perlu saran.", Colors.OKGREEN)
        return
        
    top3 = sorted(by_cat.items(), key=lambda x:x[1], reverse=True)[:3]
    for cat, amt in top3:
        perc = (amt/total)*100
        if perc > 30:
            est_save = int(amt * 0.2)
            suggestions.append(f"{Colors.FAIL}Kamu banyak keluarin buat {Colors.BOLD}{cat}{Colors.ENDC}{Colors.FAIL} ({int(perc)}%). Coba kurangi 20% biar hemat {format_currency(est_save)}{Colors.FAIL}.")
        elif perc > 15:
            suggestions.append(f"{Colors.WARNING}{cat} makan porsi besar di pengeluaranmu ({int(perc)}%). Coba cek subscription atau kebiasaan belanja.{Colors.ENDC}")
            
    valid_weeks = [v for k,v in weekly.items() if k != "wk0"]
    avg_week = statistics.mean(valid_weeks) if len(valid_weeks) > 1 else 0

    if avg_week > 0 and max(valid_weeks) > avg_week * 1.3:
        suggestions.append(f"{Colors.FAIL}Pengeluaran mingguan cenderung fluktuatif, ada minggu yang sangat tinggi. Coba review pengeluaran tiap minggu.{Colors.ENDC}")
        
    if not suggestions:
        suggestions.append(f"{Colors.OKGREEN}Keuanganmu kelihatan stabil. Tetap jaga budgeting!{Colors.ENDC}")
        
    print_color("===== Saran Penghematan =====", Colors.HEADER)
    for s in suggestions:
        print("- " + s)
    print("")

def week_of_month(date_str):
    try:
        d = datetime.date.fromisoformat(date_str)
    except:
        return "wk0" 
        
    first = d.replace(day=1)
    return (d.day + first.weekday())//7 + 1