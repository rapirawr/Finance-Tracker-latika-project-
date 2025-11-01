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
    for e in expenses:
        amt = e.get("amount",0)
        cat = e.get("category","Lainnya")
        by_cat[cat] = by_cat.get(cat,0) + amt
        
    suggestions = []
    total = sum(by_cat.values())
    if total == 0:
        print_color("Pengeluaran nol, gak perlu saran.", Colors.OKGREEN)
        return
        
    top3 = sorted(by_cat.items(), key=lambda x:x[1], reverse=True)[:3]
    for cat, amt in top3:
        perc = (amt/total)*100
        formatted_save = f"{Colors.FAIL}{format_currency(int(amt * 0.2))}{Colors.ENDC}"
        if perc > 30:
            est_save = int(amt * 0.2)
            suggestions.append(f"{Colors.FAIL}Kamu banyak keluarin buat {Colors.BOLD}{cat}{Colors.ENDC}{Colors.FAIL} ({int(perc)}%). Coba kurangi 20% biar hemat {formatted_save}.")
        elif perc > 15:
            suggestions.append(f"{Colors.WARNING}{cat} makan porsi besar di pengeluaranmu ({int(perc)}%). Coba cek subscription atau kebiasaan belanja.{Colors.ENDC}")
            
    weekly = {}
    for e in expenses:
        amt = e.get("amount",0)
        dt = e.get("date")
        try:
            d = datetime.date.fromisoformat(dt)
            wk = d.isocalendar()[1] 
            weekly[wk] = weekly.get(wk,0) + amt
        except:
            pass
            
    valid_weeks = list(weekly.values())
    
    if len(valid_weeks) > 2:
        avg_week = statistics.mean(valid_weeks)
        if max(valid_weeks) > avg_week * 1.3:
            suggestions.append(f"{Colors.FAIL}Pengeluaran mingguan cenderung fluktuatif, ada minggu yang sangat tinggi. Coba review pengeluaran tiap minggu.{Colors.ENDC}")
    
    if not suggestions:
        suggestions.append(f"{Colors.OKGREEN}Keuanganmu kelihatan stabil. Tetap jaga budgeting!{Colors.ENDC}")
        
    print_color("===== Saran Penghematan =====", Colors.HEADER)
    for s in suggestions:
        print("- " + s)
    print("")