# Secure Code Fixer - Proje Açıklaması

## 🎯 Proje Nedir?

**Secure Code Fixer**, Python kaynak kodlarındaki güvenlik açıklarını otomatik olarak tespit eden ve düzelten bir **statik kod analiz aracı**dır.

Basitçe: Yazdığın Python kodlarını tarar ve içinde güvenlik riski oluşturabilecek hataları bulur.

---

## 📥 Nereden Veri Alıyor?

Proje **hiçbir dış kaynaktan veri almıyor**. Tamamen **yerel** çalışır:

1. **Girdi:** Senin bilgisayarındaki Python dosyaları (.py uzantılı)
2. **İşlem:** Bu dosyaları satır satır okur ve analiz eder
3. **Çıktı:** Bulduğu güvenlik açıklarını rapor eder

### Örnek Kullanım:
```bash
# Tek bir dosyayı tara
python src/main.py dosyam.py

# Bir klasörü tara
python src/main.py proje_klasorum/
```

---

## 🔍 Hangi Veri Üzerinde Çalışıyor?

**Kaynak kod** üzerinde çalışıyor. Yani:

- ✅ `.py` uzantılı Python dosyaları
- ✅ Dosyanın içindeki kod satırları
- ✅ Değişken isimleri, fonksiyon çağrıları, string'ler

**Örnek:** Eğer kodunda şöyle bir satır varsa:
```python
password = "12345"
```

Program bunu okur ve "Hardcoded password" (kodda sabit şifre) olarak tespit eder.

---

## 🛡️ Neyi Tespit Ediyor?

### 1. **SQL Injection** (SQL Enjeksiyonu)
**Ne:** Veritabanı sorgularına kullanıcı girdisi eklendiğinde oluşan güvenlik açığı

**Örnek Vulnerable Kod:**
```python
user_id = input("ID gir: ")
query = f"SELECT * FROM users WHERE id = {user_id}"  # TEHLİKELİ!
cursor.execute(query)
```

**Neden Tehlikeli:** Kullanıcı `1 OR 1=1` yazarsa tüm veritabanını çekebilir.

**Program Bunu Nasıl Buluyor:** `f"SELECT..."` veya `"SELECT" + variable` gibi pattern'leri arar.

---

### 2. **XSS (Cross-Site Scripting)**
**Ne:** Kullanıcı girdisinin HTML'de güvenli olmayan şekilde gösterilmesi

**Örnek Vulnerable Kod:**
```python
username = request.get('username')
html = f"<h1>Hoşgeldin {username}</h1>"  # TEHLİKELİ!
```

**Neden Tehlikeli:** Kullanıcı `<script>alert('hack')</script>` yazarsa zararlı kod çalışır.

---

### 3. **Command Injection** (Komut Enjeksiyonu)
**Ne:** Kullanıcı girdisiyle sistem komutları çalıştırma

**Örnek Vulnerable Kod:**
```python
filename = input("Dosya adı: ")
os.system(f"rm {filename}")  # TEHLİKELİ!
```

**Neden Tehlikeli:** Kullanıcı `file.txt; rm -rf /` yazarsa tüm sistemi silebilir.

---

### 4. **Path Traversal** (Dizin Geçişi)
**Ne:** Kullanıcının izin verilmeyen dosyalara erişmesi

**Örnek Vulnerable Kod:**
```python
filename = request.get('file')
with open(f"/uploads/{filename}", 'r') as f:  # TEHLİKELİ!
    content = f.read()
```

**Neden Tehlikeli:** Kullanıcı `../../etc/passwd` yazarsa sistem dosyalarını okuyabilir.

---

### 5. **Hardcoded Secrets** (Kodda Sabit Şifreler)
**Ne:** Şifre, API key gibi hassas bilgilerin kodda yazılması

**Örnek Vulnerable Kod:**
```python
api_key = "sk_live_12345abcdef"  # TEHLİKELİ!
password = "admin123"  # TEHLİKELİ!
```

**Neden Tehlikeli:** Kod GitHub'a yüklenirse herkes şifreyi görür.

---

### 6. **Weak Cryptography** (Zayıf Şifreleme)
**Ne:** Kırılmış veya zayıf şifreleme algoritmalarının kullanımı

**Örnek Vulnerable Kod:**
```python
import hashlib
hashed = hashlib.md5(password.encode())  # TEHLİKELİ! MD5 kırılmış
```

**Neden Tehlikeli:** MD5 ve SHA1 artık güvenli değil, kolayca kırılabilir.

---

## ⚙️ Nasıl Çalışıyor? (Teknik Detay)

### Adım 1: Dosya Okuma
```python
with open('dosya.py', 'r') as f:
    kod = f.read()
```

### Adım 2: Pattern Matching (Desen Eşleştirme)
Regex (düzenli ifadeler) kullanarak tehlikeli pattern'leri arar:

```python
# Örnek: SQL Injection pattern'i
pattern = r'execute\s*\(\s*f["\'].*?\{.*?\}.*?["\']'
```

### Adım 3: Tespit ve Raporlama
Eşleşme bulunca:
- Satır numarasını kaydeder
- Tehlike seviyesini belirler (CRITICAL, HIGH, MEDIUM, LOW)
- Öneri sunar

### Adım 4: Rapor Oluşturma
3 farklı formatta rapor:
- **Console:** Terminal ekranında
- **JSON:** Makineler için (CI/CD entegrasyonu)
- **HTML:** İnsan okuyabilir, güzel görünümlü

---

## 🚀 Nasıl Çalıştırılır?

### Gereksinimler
- Python 3.6 veya üzeri
- Hiçbir ek kütüphane gerekmez (sadece Python standard library)

### Kurulum
```bash
# 1. Proje klasörüne git
cd secure-code-fixer

# 2. Hemen kullanmaya başla (kurulum gerekmez!)
```

### Kullanım Örnekleri

#### 1. Tek Dosya Tarama
```bash
python src/main.py tests/vulnerable_samples/vulnerable_code.py
```

**Çıktı:**
```
============================================================
[SECURE CODE FIXER]
Automated Security Vulnerability Detection & Fixing
============================================================

[*] Scanning: tests\vulnerable_samples\vulnerable_code.py
[*] Found 1 Python files to scan

  Scanning: vulnerable_code.py
    [!] Found 12 vulnerabilities

============================================================
SCAN SUMMARY
============================================================
Total vulnerabilities found: 12

By Severity:
  CRITICAL: 8
  HIGH: 4
============================================================
```

#### 2. Klasör Tarama
```bash
python src/main.py C:/projelerim/web_uygulamam/
```

Tüm `.py` dosyalarını tarar.

#### 3. Otomatik Düzeltme
```bash
python src/main.py dosyam.py --fix
```

Bulduğu açıkları otomatik düzeltmeye çalışır (güvenlik yorumları ekler).

#### 4. Özel Rapor Klasörü
```bash
python src/main.py dosyam.py --output raporlarim
```

Raporları `raporlarim/` klasörüne kaydeder.

---

## 📊 Raporlar

### 1. Console Raporu (Terminal)
```
File: vulnerable_code.py
   Found 12 vulnerabilities

   1. [CRITICAL] SQL_INJECTION - Line 23
      Severity: CRITICAL
      Description: SQL query uses string formatting
      Code: query = f"SELECT * FROM users WHERE id = {user_id}"
      Recommendation: Use parameterized queries
```

### 2. JSON Raporu
```json
{
  "total_vulnerabilities": 12,
  "vulnerabilities": [
    {
      "file": "vulnerable_code.py",
      "line": 23,
      "type": "SQL_INJECTION",
      "severity": "CRITICAL",
      "description": "SQL query uses string formatting",
      "recommendation": "Use parameterized queries"
    }
  ]
}
```

### 3. HTML Raporu
Tarayıcıda açılabilen, renkli ve interaktif rapor.

**Nasıl Görüntülenir:**
```bash
# Rapor oluşturulduktan sonra
start reports/vulnerability_report.html
```

---

## 🎓 Gerçek Dünya Örneği

### Senaryo: Bir web uygulaması geliştiriyorsun

**Kodun:**
```python
# login.py
import sqlite3

def login(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # HATALI KOD!
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    
    user = cursor.fetchone()
    return user is not None
```

**Secure Code Fixer Çalıştır:**
```bash
python src/main.py login.py
```

**Çıktı:**
```
[!] Found 1 vulnerability

1. [CRITICAL] SQL_INJECTION - Line 8
   Description: SQL query uses f-string with user input
   Code: query = f"SELECT * FROM users WHERE username='{username}'..."
   Recommendation: Use parameterized queries:
   cursor.execute("SELECT * FROM users WHERE username=? AND password=?", 
                  (username, password))
```

**Düzeltilmiş Kod:**
```python
# Güvenli versiyon
query = "SELECT * FROM users WHERE username=? AND password=?"
cursor.execute(query, (username, password))
```

---

## 💡 Neden Önemli?

1. **Güvenlik:** Kodundaki açıkları erken tespit eder
2. **Öğrenme:** Her açık için açıklama ve öneri verir
3. **Zaman Kazandırır:** Manuel kod incelemesi yapmana gerek kalmaz
4. **Profesyonel:** Gerçek şirketlerde kullanılan araçlara benzer

---

## 📁 Proje Yapısı

```
secure-code-fixer/
├── src/                          # Kaynak kodlar
│   ├── main.py                   # Ana program (buradan başla)
│   ├── scanner/                  # Tarayıcı modülleri
│   ├── detectors/                # Açık tespit modülleri
│   ├── fixers/                   # Otomatik düzeltme modülleri
│   └── reporters/                # Rapor oluşturucular
├── tests/                        # Test dosyaları
│   └── vulnerable_samples/       # Örnek vulnerable kodlar
├── reports/                      # Oluşturulan raporlar
└── README.md                     # Dokümantasyon
```

---

## 🎯 Özet

**Secure Code Fixer:**
- ✅ Python kodlarını tarar
- ✅ 6 tip güvenlik açığı tespit eder
- ✅ Detaylı raporlar oluşturur
- ✅ Tamamen yerel çalışır (internet gerekmez)
- ✅ Kullanımı çok kolay
- ✅ Hiçbir ek kütüphane gerektirmez

**Tek komutla çalıştır:**
```bash
python src/main.py dosyan.py
```

**Ve kodundaki güvenlik açıklarını gör!** 🛡️
