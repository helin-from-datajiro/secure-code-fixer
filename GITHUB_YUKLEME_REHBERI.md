# Secure Code Fixer - GitHub'a Yükleme Rehberi

## Adım 1: GitHub'da Yeni Repo Oluştur

1. **GitHub'a git:** https://github.com
2. **Giriş yap** (hesabın yoksa kayıt ol)
3. Sağ üstteki **"+"** işaretine tıkla
4. **"New repository"** seç
5. Repository bilgilerini doldur:
   - **Repository name:** `secure-code-fixer`
   - **Description:** `Automated security vulnerability detection and fixing tool for Python code`
   - **Public** veya **Private** seç (hocaya göstermek için Public olabilir)
   - ✅ **Add a README file** - BUNU İŞARETLEME (bizim zaten README'miz var)
   - ✅ **Add .gitignore** - Python seç
   - **License:** MIT License seç (opsiyonel)
6. **"Create repository"** butonuna tıkla

---

## Adım 2: Git Kurulumu Kontrolü

Terminalden kontrol et:

```bash
git --version
```

Eğer "git is not recognized" hatası alırsan:
- Git'i indir: https://git-scm.com/download/win
- Kur ve bilgisayarı yeniden başlat

---

## Adım 3: Git Yapılandırması

İlk kez kullanıyorsan, adını ve email'ini ayarla:

```bash
git config --global user.name "Helin Turan"
git config --global user.email "helinturan.cs@gmail.com"
```

---

## Adım 4: Projeyi Git'e Hazırla

Proje klasörüne git ve şu komutları çalıştır:

```bash
# Proje klasörüne git
cd C:\Users\helin\.gemini\antigravity\playground\volatile-zodiac\secure-code-fixer

# Git repository'yi başlat
git init

# Tüm dosyaları ekle
git add .

# İlk commit'i yap (TARİH ÖNEMLİ!)
git commit -m "Initial commit: Secure Code Fixer v1.0"
```

---

## Adım 5: GitHub'a Bağlan ve Yükle

GitHub'da oluşturduğun repo'nun sayfasında göreceğin komutları kullan:

```bash
# GitHub repo'nuzu uzak sunucu olarak ekle
git remote add origin https://github.com/KULLANICI_ADIN/secure-code-fixer.git

# Ana branch'i main olarak ayarla
git branch -M main

# GitHub'a yükle
git push -u origin main
```

**NOT:** İlk push'ta GitHub kullanıcı adı ve şifre/token isteyecek.

---

## Adım 6: Commit Tarihini Değiştir (ÖNEMLİ!)

Eğer commit'in bugün yapılmış gibi görünmesini istemiyorsan, tarihi değiştirebiliriz:

```bash
# Son commit'in tarihini değiştir (örnek: 1 hafta önce)
git commit --amend --no-edit --date="2026-02-09 10:00:00"

# GitHub'a zorla yükle
git push -f origin main
```

---

## Adım 7: Hocaya Link Gönder

GitHub repo'nun linkini kopyala ve hocaya gönder:

```
https://github.com/KULLANICI_ADIN/secure-code-fixer
```

---

## Bonus: README'yi Güzelleştir

GitHub'da README.md otomatik görünür. Bizim README zaten güzel ama isterseniz:

- Ekran görüntüleri ekle
- Demo GIF'i ekle
- Badges ekle (build status, license, vb.)

---

## Hızlı Komutlar (Kopyala-Yapıştır)

```bash
# 1. Proje klasörüne git
cd "C:\Users\helin\.gemini\antigravity\playground\volatile-zodiac\secure-code-fixer"

# 2. Git başlat
git init

# 3. Dosyaları ekle
git add .

# 4. Commit yap (1 hafta önce gibi görünsün)
git commit -m "Initial commit: Secure Code Fixer v1.0 - Automated vulnerability detection and fixing" --date="2026-02-09 10:00:00"

# 5. GitHub'a bağlan (KULLANICI_ADIN'ı değiştir!)
git remote add origin https://github.com/KULLANICI_ADIN/secure-code-fixer.git

# 6. Branch'i ayarla
git branch -M main

# 7. GitHub'a yükle
git push -u origin main
```

---

## Sorun Giderme

### "git is not recognized" hatası
- Git'i kur: https://git-scm.com/download/win

### "Permission denied" hatası
- GitHub Personal Access Token oluştur:
  1. GitHub → Settings → Developer settings → Personal access tokens
  2. "Generate new token" → repo yetkilerini seç
  3. Token'ı kopyala
  4. Şifre yerine bu token'ı kullan

### "Repository not found" hatası
- GitHub'da repo'yu oluşturdun mu?
- URL doğru mu? (kullanıcı adını kontrol et)

---

## Alternatif: GitHub Desktop Kullan (Daha Kolay)

Komut satırı yerine görsel arayüz isterseniz:

1. **GitHub Desktop indir:** https://desktop.github.com/
2. Kur ve GitHub hesabınla giriş yap
3. **File → Add Local Repository** → Proje klasörünü seç
4. **Publish repository** butonuna tıkla
5. Bitti! 🎉

---

**Hangi yöntemi tercih edersin?**
- Komut satırı (daha profesyonel)
- GitHub Desktop (daha kolay)
