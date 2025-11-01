from .utils import load_transactions, save_transactions, parse_date, today_str, format_currency, clear, Colors, print_color
import time
import datetime

CATEGORIES = [
    "Makanan", "Transport", "Hiburan", "Tagihan", "Belanja", "Kesehatan", "Lainnya"
]

def add_tx():
    while True:
        clear()
        print_color("╔════════════════════════════╗", Colors.OKBLUE)
        print_color("║      TAMBAH TRANSAKSI      ║", Colors.OKBLUE)
        print_color("╚════════════════════════════╝", Colors.OKBLUE)
        print("1. Pemasukan " + Colors.OKGREEN + "(IN)" + Colors.ENDC)
        print("2. Pengeluaran " + Colors.FAIL + "(OUT)" + Colors.ENDC)
        tipe = input("Pilih jenis (1/2): ").strip()
        if tipe not in ["1", "2"]:
            print_color("⚠️  Input salah, coba lagi...", Colors.WARNING)
            time.sleep(1)
            continue
        tipe = "income" if tipe == "1" else "expense"
        break

    while True:
        clear()
        print_color("╔════════════════════════════╗", Colors.OKBLUE)
        print_color("║          NOMINAL           ║", Colors.OKBLUE)
        print_color("╚════════════════════════════╝", Colors.OKBLUE)
        nominal = input(f"Masukkan nominal (angka saja): {Colors.OKGREEN}Rp").strip().replace(".", "").replace(",", "")
        print(Colors.ENDC, end="") 
        try:
            nominal = int(nominal)
            if nominal <= 0:
                raise ValueError
            break
        except:
            print_color("⚠️  Nominal gak valid.", Colors.FAIL)
            time.sleep(1)

    while True:
        clear()
        print_color("╔════════════════════════════╗", Colors.OKBLUE)
        print_color("║        PILIH KATEGORI       ║", Colors.OKBLUE)
        print_color("╚════════════════════════════╝", Colors.OKBLUE)
        for i, c in enumerate(CATEGORIES, 1):
            print(f"{Colors.BOLD}{i}.{Colors.ENDC} {c}")
        print(f"{Colors.BOLD}0.{Colors.ENDC} Kategori lain")
        pilih = input("Pilih (0-7): ").strip()
        if pilih.isdigit():
            pilih = int(pilih)
            if pilih == 0:
                cat = input("Tulis kategori baru: ").strip().title() or "Lainnya"
                break
            elif 1 <= pilih <= len(CATEGORIES):
                cat = CATEGORIES[pilih - 1]
                break
        print_color("⚠️  Pilihan gak valid.", Colors.FAIL)
        time.sleep(1)

    while True:
        clear()
        print_color("╔════════════════════════════╗", Colors.OKBLUE)
        print_color("║           TANGGAL          ║", Colors.OKBLUE)
        print_color("╚════════════════════════════╝", Colors.OKBLUE)
        print(f"{Colors.BOLD}1.{Colors.ENDC} Hari ini ({today_str()})")
        print(f"{Colors.BOLD}2.{Colors.ENDC} Kemarin")
        print(f"{Colors.BOLD}3.{Colors.ENDC} Masukkan tanggal sendiri (contoh: 29/10 atau 2025-10-29)")
        pilih = input("Pilih (1/2/3): ").strip()

        if pilih == "1":
            dt = datetime.date.today()
            break
        elif pilih == "2":
            dt = datetime.date.today() - datetime.timedelta(days=1)
            break
        elif pilih == "3":
            tanggal = input("Masukkan tanggal: ").strip()
            try:
                # Memanfaatkan utilitas parse_date yang lebih robust
                parsed_dt = parse_date(tanggal)
                if parsed_dt:
                    dt = parsed_dt
                    break
                else:
                    raise ValueError
            except:
                print_color("⚠️  Format tanggal salah, coba lagi...", Colors.FAIL)
                time.sleep(1)
        else:
            print_color("⚠️  Pilihan gak valid.", Colors.FAIL)
            time.sleep(1)

    clear()
    print_color("╔════════════════════════════╗", Colors.OKBLUE)
    print_color("║           CATATAN          ║", Colors.OKBLUE)
    print_color("╚════════════════════════════╝", Colors.OKBLUE)
    note = input("Tulis catatan (opsional): ").strip()

    clear()
    print_color("╔════════════════════════════╗", Colors.HEADER)
    print_color("║         KONFIRMASI         ║", Colors.HEADER)
    print_color("╚════════════════════════════╝", Colors.HEADER)
    tipe_str = f"{Colors.OKGREEN}Pemasukan{Colors.ENDC}" if tipe == 'income' else f"{Colors.FAIL}Pengeluaran{Colors.ENDC}"
    print(f"Jenis       : {tipe_str}")
    print(f"Nominal     : {format_currency(nominal)}{Colors.ENDC}")
    print(f"Kategori    : {Colors.OKCYAN}{cat}{Colors.ENDC}")
    print(f"Tanggal     : {Colors.OKCYAN}{dt.isoformat()}{Colors.ENDC}")
    print(f"Catatan     : {note if note else '-'}")
    ok = input("\nSimpan transaksi? (y/n): ").strip().lower()
    if ok != "y":
        print_color("❌ Transaksi dibatalkan.", Colors.FAIL)
        time.sleep(1)
        return

    tx = {
        "type": tipe,
        "amount": nominal,
        "category": cat,
        "date": dt.isoformat(),
        "note": note
    }
    data = load_transactions()
    data.append(tx)
    save_transactions(data)
    print_color("\n✅ Transaksi berhasil disimpan!", Colors.OKGREEN)
    time.sleep(1.5)

def summarize_transactions(data):
    total_in = 0
    total_out = 0
    by_cat = {}
    for d in data:
        amt = d.get("amount", 0)
        cat = d.get("category", "Lainnya")
        if d.get("type") == "income":
            total_in += amt
        else:
            total_out += amt
            by_cat[cat] = by_cat.get(cat, 0) + amt
    return total_in, total_out, by_cat

def show_summary():
    data = load_transactions()
    total_in, total_out, by_cat = summarize_transactions(data)
    saldo = total_in - total_out
    clear()
    print_color("╔════════════════════════════════════════╗", Colors.HEADER)
    print_color("║            RINGKASAN KEUANGAN          ║", Colors.HEADER)
    print_color("╚════════════════════════════════════════╝", Colors.HEADER)
    print(f"Total Pemasukan  : {format_currency(total_in)}{Colors.ENDC}")
    print(f"Total Pengeluaran: {format_currency(total_out)}{Colors.ENDC}")
    
    saldo_color = Colors.OKGREEN if saldo >= 0 else Colors.FAIL
    print(f"Saldo Sekarang   : {saldo_color}{format_currency(saldo)}{Colors.ENDC}")
    print_color("──────────────────────────────────────────", Colors.OKBLUE)

    if by_cat:
        print(f"{Colors.BOLD}Breakdown Pengeluaran:{Colors.ENDC}")
        total = sum(by_cat.values())
        for k, v in sorted(by_cat.items(), key=lambda x: x[1], reverse=True):
            perc = (v / total) * 100 if total > 0 else 0
            bar = render_bar(perc)
            bar_color = Colors.FAIL if perc > 30 else Colors.WARNING if perc > 15 else Colors.OKGREEN
            print(f"{k:<12} | {bar_color}{bar}{Colors.ENDC} {int(perc):>3}%  {format_currency(v)}{Colors.ENDC}")
    else:
        print_color("Belum ada pengeluaran.", Colors.WARNING)

def list_tx():
    data = load_transactions()
    clear()
    print_color("╔════════════════════════════════════════╗", Colors.HEADER)
    print_color("║            DAFTAR TRANSAKSI            ║", Colors.HEADER)
    print_color("╚════════════════════════════════════════╝", Colors.HEADER)

    if not data:
        print_color("Belum ada transaksi yang tercatat.", Colors.WARNING)
        return

    sorted_data = sorted(data, key=lambda x: x.get("date"), reverse=True)

    header = f"{'No':<4} {'Tanggal':<12} {'Tipe':<10} {'Nominal':<15} {'Kategori':<15} Catatan"
    print_color(header, Colors.BOLD + Colors.OKBLUE)
    print_color("─" * 75, Colors.OKBLUE)

    for i, t in enumerate(sorted_data, 1):
        tanggal = Colors.OKCYAN + t.get("date", "-") + Colors.ENDC
        tipe = t.get("type")
        tipe_str = f"{Colors.OKGREEN}IN{Colors.ENDC}" if tipe == "income" else f"{Colors.FAIL}OUT{Colors.ENDC}"
        nominal = format_currency(t.get("amount", 0))
        kategori = t.get("category", "Lainnya")
        note = t.get("note", "")
        print(f"{i:<4} {tanggal:<23} {tipe_str:<19} {nominal:<29}{Colors.OKCYAN}{kategori:<15}{Colors.ENDC} {note}")

    print_color("─" * 75, Colors.OKBLUE)
    print(f"Total transaksi: {Colors.BOLD}{len(sorted_data)}{Colors.ENDC}")

def delete_last_tx():
    data = load_transactions()
    if not data:
        print_color("❌ Belum ada transaksi untuk dihapus.", Colors.FAIL)
        time.sleep(1.5)
        return

    clear()
    last_tx = data[-1]
    tipe_str = f"{Colors.OKGREEN}Pemasukan{Colors.ENDC}" if last_tx['type'] == 'income' else f"{Colors.FAIL}Pengeluaran{Colors.ENDC}"
    
    print_color("╔════════════════════════════╗", Colors.FAIL)
    print_color("║  KONFIRMASI HAPUS TERAKHIR ║", Colors.FAIL)
    print_color("╚════════════════════════════╝", Colors.FAIL)
    print(f"Transaksi terakhir yang akan dihapus:")
    print(f"Jenis       : {tipe_str}")
    print(f"Nominal     : {format_currency(last_tx['amount'])}{Colors.ENDC}")
    print(f"Kategori    : {Colors.OKCYAN}{last_tx['category']}{Colors.ENDC}")
    
    confirm = input("\nYakin hapus transaksi ini? (y/n): ").strip().lower()
    if confirm == 'y':
        data.pop()
        save_transactions(data)
        print_color("\n✅ Transaksi terakhir berhasil dihapus.", Colors.OKGREEN)
    else:
        print_color("\n❌ Penghapusan dibatalkan.", Colors.WARNING)
        
    time.sleep(1.5)

def render_bar(percentage, length=25):
    filled = int((percentage / 100) * length)
    return "█" * filled + "-" * (length - filled)