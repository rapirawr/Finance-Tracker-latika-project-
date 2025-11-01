<<<<<<< HEAD
from modules.utils import ensure_data_file, prompt, clear, pause, Colors, print_color
from modules.summary import add_tx, show_summary, list_tx, delete_last_tx
from modules.analyze import show_habits, predict_end
from modules.suggest import show_suggestions
from modules.ai_analyze import run_ai_analysis

ensure_data_file()

def menu():
    clear()
    print_color("=" * 40, Colors.HEADER)
    print_color(f"{'AI PERSONAL FINANCE TRACKER':^40}", Colors.HEADER)
    print_color("=" * 40, Colors.HEADER)
    print(f"{Colors.BOLD}1.{Colors.ENDC} Tambah transaksi")
    print(f"{Colors.BOLD}2.{Colors.ENDC} Lihat ringkasan keuangan")
    print(f"{Colors.BOLD}3.{Colors.ENDC} Analisis kebiasaan")
    print(f"{Colors.BOLD}4.{Colors.ENDC} Saran penghematan")
    print(f"{Colors.BOLD}5.{Colors.ENDC} Prediksi saldo akhir bulan")
    print(f"{Colors.BOLD}6.{Colors.ENDC} List semua transaksi")
    print(f"{Colors.BOLD}7.{Colors.ENDC} AI Analisis")
    print(f"{Colors.BOLD}8.{Colors.ENDC} Hapus transaksi terakhir {Colors.BOLD}{Colors.FAIL}(UNDO){Colors.ENDC}")
    print_color(f"{Colors.BOLD}9.{Colors.ENDC} Keluar{Colors.BOLD}", Colors.OKGREEN) 
    print_color("-" * 40, Colors.OKBLUE)

def main():
    while True:
        menu()
        choice = prompt("Pilih menu (1-9)") 
        if choice == "1":
            add_tx()
            pause()
        elif choice == "2":
            show_summary()
            pause()
        elif choice == "3":
            show_habits()
            pause()
        elif choice == "4":
            show_suggestions()
            pause()
        elif choice == "5":
            predict_end()
            pause()
        elif choice == "6":
            list_tx()
            pause()
        elif choice == "7":
            run_ai_analysis() 
            pause()
        elif choice == "8":
            delete_last_tx()
            pause()
        elif choice == "9":
            print_color("\nDadahhh 👋 Sampai jumpa lagi!", Colors.OKBLUE)
            break
        else:
            print_color("Pilih yg bener dong.", Colors.FAIL)
            pause()

if __name__ == "__main__":
=======
from modules.utils import ensure_data_file, prompt, clear, pause, Colors, print_color
from modules.summary import add_transaction, show_summary, list_transactions
from modules.analyze import analyze_habits, predict_month_end
from modules.suggest import generate_suggestions
from modules.ai_analyze import ai_financial_analysis

ensure_data_file()

def menu():
    clear()
    print_color("=" * 40, Colors.HEADER)
    print_color(f"{'AI PERSONAL FINANCE TRACKER':^40}", Colors.HEADER)
    print_color("=" * 40, Colors.HEADER)
    print(f"{Colors.BOLD}1.{Colors.ENDC} Tambah transaksi")
    print(f"{Colors.BOLD}2.{Colors.ENDC} Lihat ringkasan keuangan")
    print(f"{Colors.BOLD}3.{Colors.ENDC} Analisis kebiasaan")
    print(f"{Colors.BOLD}5.{Colors.ENDC} Prediksi saldo akhir bulan")
    print(f"{Colors.BOLD}6.{Colors.ENDC} List semua transaksi")
    print(f"{Colors.BOLD}7.{Colors.ENDC} AI Analisis")
    print_color(f"{Colors.BOLD}8.{Colors.ENDC} Keluar{Colors.BOLD}", Colors.OKGREEN) 
    print_color("-" * 40, Colors.OKBLUE)

def main():
    while True:
        menu()
        choice = prompt("Pilih menu (1-8)") 
        if choice == "1":
            add_transaction()
            pause()
        elif choice == "2":
            show_summary()
            pause()
        elif choice == "3":
            analyze_habits()
            pause()
        elif choice == "4":
            generate_suggestions()
            pause()
        elif choice == "5":
            predict_month_end()
            pause()
        elif choice == "6":
            list_transactions()
            pause()
        elif choice == "7":
            ai_financial_analysis() 
            pause()
        elif choice == "8":
            print_color("\nDadahhh 👋 Sampai jumpa lagi!", Colors.OKBLUE)
            break
        else:
            print_color("Pilih yg bener dong.", Colors.FAIL)
            pause()

if __name__ == "__main__":
>>>>>>> 026ebe67c4f166141c921e7f366ac7b6ce37ecbe
    main()