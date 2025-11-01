<<<<<<< HEAD
import os, json, datetime, math

class Colors:
    HEADER = '\033[95m'  
    OKBLUE = '\033[94m'  
    OKCYAN = '\033[96m'  
    OKGREEN = '\033[92m' 
    WARNING = '\033[93m' 
    FAIL = '\033[91m'    
    ENDC = '\033[0m'     
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "transactions.json")

def ensure_data_file():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)

def load_transactions():
    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
            if not isinstance(data, list):
                return []
            return data
        except:
            return []

def save_transactions(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def parse_date(s):
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
        try:
            return datetime.datetime.strptime(s, fmt).date()
        except:
            pass
    return None

def today_str():
    return datetime.date.today().isoformat()

def prompt(msg):
    return input(f"{Colors.OKCYAN}{msg}{Colors.ENDC}: ").strip()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input(f"{Colors.OKCYAN}\nTekan Enter untuk lanjut...{Colors.ENDC}")

def format_currency(n):
    try:
        n = float(n)
    except:
        n = 0.0
    if n.is_integer():
        return f"{Colors.BOLD}{Colors.OKGREEN}Rp{int(n):,}{Colors.ENDC}".replace(",", ".")
    return f"{Colors.BOLD}{Colors.OKGREEN}Rp{n:,.2f}{Colors.ENDC}".replace(",", ".")

def print_color(text, color):
=======
import os, json, datetime, math

# Kode Warna ANSI
class Colors:
    HEADER = '\033[95m'  
    OKBLUE = '\033[94m'  
    OKCYAN = '\033[96m'  
    OKGREEN = '\033[92m' 
    WARNING = '\033[93m' 
    FAIL = '\033[91m'    
    ENDC = '\033[0m'     
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "transactions.json")

def ensure_data_file():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)

def load_transactions():
    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
            if not isinstance(data, list):
                return []
            return data
        except:
            return []

def save_transactions(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def parse_date(s):
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
        try:
            return datetime.datetime.strptime(s, fmt).date()
        except:
            pass
    return None

def today_str():
    return datetime.date.today().isoformat()

def prompt(msg):
    return input(f"{Colors.OKCYAN}{msg}{Colors.ENDC}: ").strip()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input(f"{Colors.OKCYAN}\nTekan Enter untuk lanjut...{Colors.ENDC}")

def format_currency(n):
    try:
        n = float(n)
    except:
        n = 0.0
    if n.is_integer():
        return f"{Colors.BOLD}{Colors.OKGREEN}Rp{int(n):,}{Colors.ENDC}".replace(",", ".")
    return f"{Colors.BOLD}{Colors.OKGREEN}Rp{n:,.2f}{Colors.ENDC}".replace(",", ".")

def print_color(text, color):
>>>>>>> 026ebe67c4f166141c921e7f366ac7b6ce37ecbe
    print(f"{color}{text}{Colors.ENDC}")