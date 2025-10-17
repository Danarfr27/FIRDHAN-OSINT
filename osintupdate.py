import urllib.parse
import webbrowser
import time
import sys

try:
    # selenium imports are optional; script works without them but auto-click won't
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except Exception:
    SELENIUM_AVAILABLE = False


def osint_search_by_name(name, open_social_tabs=True):
    """
    Mencari semua informasi terkait nama target di Google,
    termasuk kemungkinan akun sosial media dan link lainnya.

    Jika auto-click diaktifkan (melalui prompt), fungsi akan mencoba
    mengklik hasil pencarian teratas pada halaman pencarian Google
    menggunakan Selenium (jika tersedia).
    """
    query = urllib.parse.quote_plus(name)
    # Pencarian Google umum
    google_search = f"https://www.google.com/search?q={query}"

    # Pencarian kemungkinan akun sosial media
    social_sites = [
        "site:facebook.com",
        "site:instagram.com",
        "site:twitter.com",
        "site:linkedin.com",
        "site:tiktok.com",
        "site:youtube.com",
        "site:github.com",
        "site:medium.com",
        "site:pinterest.com"
    ]

    print("\n[+] Link pencarian Google untuk nama target:")
    print(google_search)
    webbrowser.open(google_search)

    if open_social_tabs:
        print("\n[+] Link pencarian akun sosial media di Google:")
        for site in social_sites:
            search_url = f"https://www.google.com/search?q={query}+{urllib.parse.quote_plus(site)}"
            print(search_url)
            # Buka tab baru untuk setiap pencarian sosial media
            webbrowser.open_new_tab(search_url)


def auto_click_top_result_with_selenium(url, timeout=15, headless=False):
    """
    Buka URL dengan Selenium dan klik hasil pencarian teratas (first organic result).

    - timeout: waktu menunggu (detik) untuk elemen hasil muncul
    - headless: jika True, browser dijalankan tanpa UI (klik mungkin tidak berefek pada tampilan)

    Mengembalikan True jika klik berhasil, False jika gagal.
    """
    if not SELENIUM_AVAILABLE:
        print("[!] Selenium atau webdriver_manager tidak ditemukan. Install dengan: pip install selenium webdriver-manager")
        return False

    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")

    # Buka Chrome dengan driver yang diunduh otomatis
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"[!] Gagal memulai Chrome WebDriver: {e}")
        return False

    try:
        driver.get(url)
        wait = WebDriverWait(driver, timeout)

        # Tunggu sampai setidaknya satu judul hasil pencarian (h3) muncul
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3")))

        # Cari semua h3 (judul hasil). Ambil parent <a> pertama yang bisa diklik.
        h3s = driver.find_elements(By.CSS_SELECTOR, "h3")
        for h in h3s:
            try:
                a = h.find_element(By.XPATH, "./ancestor::a[1]")
                # Pastikan elemen terlihat dan klik
                if a.is_displayed() and a.is_enabled():
                    a.click()
                    print("[+] Berhasil mengklik hasil teratas (Selenium).")
                    # beri waktu supaya tab/halaman tujuan terbuka
                    time.sleep(2)
                    return True
            except Exception:
                continue

        print("[!] Tidak menemukan elemen hasil yang dapat diklik.")
        return False
    finally:
        # Jangan langsung menutup browser agar pengguna bisa melihat hasil.
        # Namun jika headless, tutup karena tidak ada UI untuk dilihat.
        if headless:
            driver.quit()


if __name__ == "__main__":
    print("=== OSINT Search by Name ===")
    target = input("Masukkan nama target: ").strip()
    if not target:
        print("[!] Nama target kosong. Keluar.")
        sys.exit(1)

    # Tanyakan apakah ingin membuka tab sosial media juga
    open_social = input("Buka pencarian akun sosial media juga? (Y/n) ").strip().lower()
    open_social_tabs = (open_social != 'n')

    # Jalankan pencarian normal (membuka Google dan tab sosial media jika dipilih)
    osint_search_by_name(target, open_social_tabs=open_social_tabs)

    # Opsi auto-click: jika pengguna ingin, coba klik hasil teratas di tab Google pertama
    auto_click = input("Aktifkan auto-click hasil pencarian teratas? (y/N): ").strip().lower()
    if auto_click == 'y' or auto_click == 'yes':
        # Pilihan metode; untuk sekarang hanya selenium yang diimplementasikan
        method = input("Metode auto-click [selenium]: ").strip().lower() or 'selenium'
        # Delay singkat agar tab browser sempat terbuka
        delay = 2
        print(f"[i] Menunggu {delay}s sebelum mencoba auto-click...")
        time.sleep(delay)

        if method == 'selenium':
            google_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(target)}"
            success = auto_click_top_result_with_selenium(google_url)
            if not success:
                print("[!] Auto-click gagal menggunakan Selenium. Pastikan selenium dan webdriver-manager terinstal dan Chrome tersedia.")
        else:
            print("[!] Metode auto-click tidak dikenali. Hanya 'selenium' yang didukung saat ini.")
