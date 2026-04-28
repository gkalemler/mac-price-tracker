#!/usr/bin/env python3
"""
Apple Mac Mini Refurbished Fiyat Takipçisi
Her 10 dakikada bir kontrol eder, fiyat düşünce email atar!
"""

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import json
from datetime import datetime

# AYARLAR - BUNLARI DEĞİŞTİR!
EMAIL_TO = "Gurkan.kalemler@gmail.com"  # Email adresin
EMAIL_FROM = "Gurkan.kalemler@gmail.com"  # Gmail adresi (aynı)
EMAIL_PASSWORD = "bsqvsaqilzwvjsyc"  # Gmail uygulama şifresi ✅

# Hedef fiyat aralığı (USD)
MIN_PRICE = 300
MAX_PRICE = 600

# Model filtresi (M2, M4 veya boş bırak = hepsi)
ALLOWED_MODELS = ["M2", "M4"]  # M2 ve M4 kabul et

# RAM filtresi
ALLOWED_RAM = ["16GB", "24GB", "32GB"]  # 16GB ve üstü

# SSD filtresi
ALLOWED_SSD = ["256GB", "512GB", "1TB", "2TB"]  # 256GB ve üstü

def get_apple_refurb():
    """Apple refurbished sayfasını kontrol et"""
    url = "https://www.apple.com/shop/refurbished/mac/mac-mini"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Mac Mini'leri bul
        products = []
        
        # Fiyat ve ürün bilgilerini çek
        items = soup.find_all('div', class_='as-producttile')
        
        for item in items:
            try:
                title = item.find('h3').text.strip()
                price_text = item.find('span', class_='as-price-currentprice').text.strip()
                price = float(price_text.replace('$', '').replace(',', ''))
                
                # Model, RAM ve SSD kontrolü
                model_ok = any(model in title for model in ALLOWED_MODELS)
                ram_ok = any(ram in title for ram in ALLOWED_RAM)
                ssd_ok = any(ssd in title for ssd in ALLOWED_SSD)
                
                # Fiyat aralığında mı?
                price_ok = MIN_PRICE <= price <= MAX_PRICE
                
                if model_ok and ram_ok and ssd_ok and price_ok:
                    products.append({
                        'title': title,
                        'price': price,
                        'url': 'https://www.apple.com' + item.find('a')['href'] if item.find('a') else url
                    })
            except:
                continue
        
        return products
    
    except Exception as e:
        print(f"❌ Hata: {e}")
        return []

def send_email(subject, body):
    """Email gönder"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'html'))
        
        # Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_FROM, EMAIL_TO, text)
        server.quit()
        
        print("✅ Email gönderildi!")
        return True
    
    except Exception as e:
        print(f"❌ Email hatası: {e}")
        return False

def check_prices():
    """Fiyatları kontrol et"""
    print(f"\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🔍 Apple kontrol ediliyor...")
    
    products = get_apple_refurb()
    
    if not products:
        print("❌ Ürün bulunamadı!")
        return
    
    print(f"✅ {len(products)} ürün bulundu!\n")
    
    # Fiyatları göster
    for p in products:
        print(f"📦 {p['title']}")
        print(f"💰 ${p['price']}")
        
        # Email gönder (her uygun üründe)
        print(f"✅ Fiyat aralığında! Email gönderiliyor...")
        
        # Email gönder
        subject = f"🎯 Mac Mini ${p['price']} - İYİ FİYAT!"
        body = f"""
        <h2>💰 Uygun Fiyat Bulundu!</h2>
        <h3>{p['title']}</h3>
        <p><strong>Fiyat:</strong> ${p['price']}</p>
        <p><strong>Fiyat Aralığı:</strong> ${MIN_PRICE} - ${MAX_PRICE}</p>
        <p><a href="{p['url']}" style="background:#007AFF;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;">SATIN AL</a></p>
        <p><small>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small></p>
        """
        
        send_email(subject, body)
        
        print("-" * 50)

def main():
    """Ana döngü"""
    print("🚀 Apple Mac Mini Fiyat Takipçisi Başladı!")
    print(f"🎯 Modeller: {', '.join(ALLOWED_MODELS)}")
    print(f"💾 RAM: {', '.join(ALLOWED_RAM)}")
    print(f"💿 SSD: {', '.join(ALLOWED_SSD)}")
    print(f"💰 Fiyat: ${MIN_PRICE} - ${MAX_PRICE}")
    print(f"📧 Email: {EMAIL_TO}")
    print(f"⏱️  Kontrol: Her 10 dakika\n")
    print("=" * 50)
    
    # İlk kontrol
    check_prices()
    
    # Her 10 dakikada bir kontrol et
    while True:
        time.sleep(600)  # 600 saniye = 10 dakika
        check_prices()

if __name__ == "__main__":
    main()
