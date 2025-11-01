from .utils import load_transactions, save_transactions, load_categories, save_categories, parse_date, today_str, format_currency, clear, Colors, print_color
import time
import datetime

DEFAULT_CATEGORIES = [
    "Makanan", "Transport", "Hiburan", "Tagihan", "Belanja", "Kesehatan", "Lainnya"
]

def get_all_categories():
    custom_categories = load_categories()
    all_categories = DEFAULT_CATEGORIES + [c for c in custom_categories if c not in DEFAULT_CATEGORIES]
    return all_categories

def add_tx():
    clear()
    print_color("╔════════════════════════════╗", Colors.OKBLUE)
    print_color("║      TAMBAH TRANSAKSI      ║", Colors.OKBLUE)
    print_color("╚════════════════════════════╝", Colors.OKBLUE)

    while True:
        print("Jenis:")
        print("1. Pemasukan " + Colors.OKGREEN + "(IN)" + Colors.ENDC)
        print("2. Pengeluaran " + Colors.FAIL + "(OUT)" + Colors.ENDC)
        tipe_input = input("Pilih jenis (1/2): ").strip()
        if tipe_input in ["1", "2"]:
            tipe = "income" if tipe_input == "1" else "expense"
            break
        print_color("⚠️  Input salah, coba lagi...", Colors.WARNING)

    while True:
        nominal_input = input(f"Masukkan nominal (angka saja): {Colors.OKGREEN}Rp").strip().replace(".", "").replace(",", "")
        print(Colors.ENDC, end="")
        try:
            nominal = int(nominal_input)
            if nominal <= 0:
                raise ValueError
            break
        except:
            print_color("⚠️  Nominal gak valid.", Colors.FAIL)

    all_categories = get_all_categories()
    categories_to_show = [c for c in all_categories if c != "Lainnya"]
    
    while True:
        print("\nPilih Kategori:")
        for i, c in enumerate(categories_to_show, 1):
            print(f"{Colors.BOLD}{i}.{Colors.ENDC} {c}")
        print(f"{Colors.BOLD}0.{Colors.ENDC} Kategori baru (Custom)")
        pilih = input(f"Pilih (0-{len(categories_to_show)}): ").strip()
        
        if pilih.isdigit():
            pilih = int(pilih)
            if pilih == 0:
                cat = input("Tulis kategori baru: ").strip().title()
                if not cat:
                    cat = "Lainnya"
                
                if cat not in all_categories:
                    custom_categories = load_categories()
                    custom_categories.append(cat)
                    save_categories(custom_categories)
                    print_color(f"✅ Kategori '{cat}' disimpan untuk penggunaan berikutnya.", Colors.OKGREEN)
                break
                
            elif 1 <= pilih <= len(categories_to_show):
                cat = categories_to_show[pilih - 1]
                break
        print_color("⚠️  Pilihan gak valid.", Colors.FAIL)

    dt = datetime.date.today()
    while True:
        print("\nPilih Tanggal:")
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
            parsed_dt = parse_date(tanggal)
            if parsed_dt:
                dt = parsed_dt
                break
            else:
                print_color("⚠️  Format tanggal salah, coba lagi...", Colors.FAIL)
        else:
            print_color("⚠️  Pilihan gak valid.", Colors.FAIL)

    note = input("\nTulis catatan (opsional): ").strip()

    clear()
    print_color("╔════════════════════════════╗", Colors.HEADER)
    print_color("║         KONFIRMASI         ║", Colors.HEADER)
    print_color("╚════════════════════════════╝", Colors.HEADER)
    tipe_str = f"{Colors.OKGREEN}Pemasukan{Colors.ENDC}" if tipe == 'income' else f"{Colors.FAIL}Pengeluaran{Colors.ENDC}"
    print(f"Jenis       : {tipe_str}")
    nominal_str = format_currency(nominal)
    nominal_color = Colors.OKGREEN if tipe == 'income' else Colors.FAIL
    print(f"Nominal     : {nominal_color}{Colors.BOLD}{nominal_str}{Colors.ENDC}")
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
    
    print(f"Total Pemasukan  : {Colors.OKGREEN}{format_currency(total_in)}{Colors.ENDC}")
    print(f"Total Pengeluaran: {Colors.FAIL}{format_currency(total_out)}{Colors.ENDC}")
    
    saldo_color = Colors.OKGREEN if saldo >= 0 else Colors.FAIL
    print(f"Saldo Sekarang   : {saldo_color}{Colors.BOLD}{format_currency(saldo)}{Colors.ENDC}")
    print_color("──────────────────────────────────────────", Colors.OKBLUE)

    if by_cat:
        print(f"{Colors.BOLD}Breakdown Pengeluaran:{Colors.ENDC}")
        total = sum(by_cat.values())
        for k, v in sorted(by_cat.items(), key=lambda x: x[1], reverse=True):
            perc = (v / total) * 100 if total > 0 else 0
            bar = render_bar(perc)
            bar_color = Colors.FAIL if perc > 30 else Colors.WARNING if perc > 15 else Colors.OKGREEN
            print(f"{k:<12} | {bar_color}{bar}{Colors.ENDC} {int(perc):>3}%  {Colors.FAIL}{format_currency(v)}{Colors.ENDC}")
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

    sorted_data = sorted([(i+1, t) for i, t in enumerate(data)], key=lambda x: x[1].get("date"), reverse=True)

    header = f"{'No':<4} {'Tanggal':<12} {'Tipe':<10} {'Nominal':<15} {'Kategori':<15} Catatan"
    print_color(header, Colors.BOLD + Colors.OKBLUE)
    print_color("─" * 75, Colors.OKBLUE)

    for i, (original_index, t) in enumerate(sorted_data, 1):
        tanggal = Colors.OKCYAN + t.get("date", "-") + Colors.ENDC
        tipe = t.get("type")
        tipe_str = f"{Colors.OKGREEN}IN{Colors.ENDC}" if tipe == "income" else f"{Colors.FAIL}OUT{Colors.ENDC}"
        
        nominal_str = format_currency(t.get("amount", 0))
        nominal_color = Colors.OKGREEN if tipe == "income" else Colors.FAIL
        
        kategori = t.get("category", "Lainnya")
        note = t.get("note", "")
        print(f"{original_index:<4} {tanggal:<23} {tipe_str:<19} {nominal_color}{nominal_str:<15}{Colors.ENDC} {Colors.OKCYAN}{kategori:<15}{Colors.ENDC} {note}")

    print_color("─" * 75, Colors.OKBLUE)
    print(f"Total transaksi: {Colors.BOLD}{len(data)}{Colors.ENDC}")
    
    while True:
        action = input("\nMasukkan No. transaksi untuk dihapus, atau 'b' untuk kembali: ").strip().lower()
        if action == 'b':
            return
        
        try:
            tx_num = int(action)
            if 1 <= tx_num <= len(data):
                delete_by_number(tx_num)
                return
            else:
                print_color("❌ Nomor transaksi tidak valid.", Colors.FAIL)
        except ValueError:
            print_color("❌ Input tidak valid.", Colors.FAIL)

def delete_by_number(index):
    data = load_transactions()
    clear()
    
    tx_to_delete = data[index - 1]
    tipe_str = f"{Colors.OKGREEN}Pemasukan{Colors.ENDC}" if tx_to_delete['type'] == 'income' else f"{Colors.FAIL}Pengeluaran{Colors.ENDC}"
    
    print_color("╔════════════════════════════╗", Colors.FAIL)
    print_color("║  KONFIRMASI HAPUS TRANSAKSI ║", Colors.FAIL)
    print_color("╚════════════════════════════╝", Colors.FAIL)
    print(f"Yakin HAPUS transaksi No. {Colors.BOLD}{index}{Colors.ENDC} ini?")
    print(f"Jenis       : {tipe_str}")
    print(f"Nominal     : {Colors.BOLD}{format_currency(tx_to_delete['amount'])}{Colors.ENDC}")
    print(f"Kategori    : {Colors.OKCYAN}{tx_to_delete['category']}{Colors.ENDC}")
    
    confirm = input("\nYakin hapus? (y/n): ").strip().lower()
    if confirm == 'y':
        data.pop(index - 1)
        save_transactions(data)
        print_color("\n✅ Transaksi berhasil dihapus.", Colors.OKGREEN)
    else:
        print_color("\n❌ Penghapusan dibatalkan.", Colors.WARNING)

def delete_last_tx():
    data = load_transactions()
    if not data:
        print_color("❌ Belum ada transaksi untuk dihapus.", Colors.FAIL)
        time.sleep(1.5)
        return

    clear()
    last_tx = data[-1]
    last_index = len(data)
    tipe_str = f"{Colors.OKGREEN}Pemasukan{Colors.ENDC}" if last_tx['type'] == 'income' else f"{Colors.FAIL}Pengeluaran{Colors.ENDC}"
    
    print_color("╔════════════════════════════╗", Colors.FAIL)
    print_color("║  KONFIRMASI HAPUS TERAKHIR ║", Colors.FAIL)
    print_color("╚════════════════════════════╝", Colors.FAIL)
    print(f"Transaksi terakhir (No. {last_index}) yang akan dihapus:")
    print(f"Jenis       : {tipe_str}")
    print(f"Nominal     : {Colors.BOLD}{format_currency(last_tx['amount'])}{Colors.ENDC}")
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