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
CATEGORIES_FILE = os.path.join(DATA_DIR, "categories.json")

def ensure_data_file():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
    if not os.path.exists(CATEGORIES_FILE):
        with open(CATEGORIES_FILE, "w") as f:
            json.dump([], f)

def load_transactions():
    if not os.path.exists(DATA_FILE):
        return []
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

def load_categories():
    if not os.path.exists(CATEGORIES_FILE):
        return []
    with open(CATEGORIES_FILE, "r") as f:
        try:
            data = json.load(f)
            if not isinstance(data, list):
                return []
            return data
        except:
            return []

def save_categories(data):
    unique_categories = list(set(data))
    with open(CATEGORIES_FILE, "w") as f:
        json.dump(unique_categories, f, indent=2)

def parse_date(s):
    if '/' in s or '-' in s:
        try:
            parts = s.split('/') if '/' in s else s.split('-')
            if len(parts) == 2:
                d, m = map(int, parts)
                y = datetime.date.today().year
                return datetime.date(y, m, d)
        except:
            pass
            
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
        
    sign = "-" if n < 0 else ""
    n = abs(n)
    
    if n.is_integer():
        return f"{sign}Rp{int(n):,}".replace(",", "TEMP").replace(".", ",").replace("TEMP", ".")
    return f"{sign}Rp{n:,.2f}".replace(",", "TEMP").replace(".", ",").replace("TEMP", ".")


def print_color(text, color):
    print(f"{color}{text}{Colors.ENDC}")