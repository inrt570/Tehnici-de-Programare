import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    if path.startswith("/"):
        path = path[1:]
    return f"https://{host}/{path}"
    pass


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.startswith("https://")
    pass


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    import requests
    response = requests.get(url)
    pass


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
         if 'Content-Length' not in response.headers:
            response = requests.get(url, timeout=5)
            
        headers = response.headers
        
        return {
            "status": response.status_code,
            "content_type": headers.get('Content-Type', '').split(';')[0],
            "length": len(response.content) if response.request.method == 'GET' else int(headers.get('Content-Length', 0)),
            "server": headers.get('Server', 'unknown')
        }
        
    except requests.exceptions.Timeout:
        return {"status": None, "error": "Timeout (peste 5s)"}
    except requests.exceptions.ConnectionError:
        return {"status": None, "error": "Eroare conexiune / DNS"}
    except requests.exceptions.RequestException as e:
        return {"status": None, "error": str(e)}
    pass


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    ok = 0
    for url in SITES:
        info = check_site(url)
        if info["status"] is not None and info["status"] < 400:
            ok += 1
            print(f"[OK] {url} -> {info['status']} ({info['length']} bytes)")
    print(f"Rezumat: {ok}/{len(SITES)} site-uri funcționează")
    pass


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
     try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
    {
            "status": None, 
            "error": str(e).split(':')[-1].strip() 
        }
    
    present = []
    missing = []
  
    for header in SECURITY_HEADERS:
        if header in response.headers:
            present.append(header)
        else:
            missing.append(header)
            
    score = int((len(present) / len(SECURITY_HEADERS)) * 100)
    pass


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
for i in range(1, attempts + 1):
        try:
            r = requests.get(url, timeout=10)
            if r.status_code < 500:
                return {"status": r.status_code, "attempts": i}
        except requests.RequestException:
            pass
    return {"status": None, "attempts": attempts}
    pass


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""

    pass
