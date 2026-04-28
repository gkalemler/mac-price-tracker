#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email ayarları
SENDER_EMAIL = "gurkan.kalemler@gmail.com"
RECEIVER_EMAIL = "gurkan.kalemler@gmail.com"
APP_PASSWORD = "bsqvsaqilzwvjsyc"

# Hedef fiyat aralığı (USD)
MIN_PRICE = 300
MAX_PRICE = 600

# Model filtresi (M2, M4 veya boş bırak = hepsi)
ALLOWED_MODELS = ["M2", "M4"]

# RAM filtresi
ALLOWED_RAM = ["16GB", "24GB", "32GB"]

# SSD filtresi
ALLOWED_SSD = ["256GB", "512GB", "1TB", "2TB"]

def send_email(subject, body):
    """Email gönder"""
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Email gönderildi: {subject}")
        return True
    except Exception as e:
        print(f"❌ Email hatası: {e}")
        return False

def get_apple_refurbished():
    """Apple refurbished sayfasını kontrol et"""
    url = "https://www.apple.com/shop/refurbished/mac"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        mac_minis = []
        
        tiles = soup.find_all('div', class_='rf-refurb-producttile')
        
        for tile in tiles:
            try:
                title_tag = tile.find('h3', class_='rf-refurb-producttile-title')
                if not title_tag:
                    continue
                    
                title = title_tag.text.strip()
                
                if 'Mac mini' not in title:
                    continue
                
                price_tag = tile.find('div', class_='as-price-currentprice')
                if not price_tag:
                    continue
                
                price_text = price_tag.text.strip()
                price_text = price_text.replace('$', '').replace(',', '')
                price = int(float(price_text))
                
                link_tag = tile.find('a', href=True)
                link = 'https://www.apple.com' + link_tag['href'] if link_tag else url
                
                if price < MIN_PRICE or price > MAX_PRICE:
                    continue
                
                if ALLOWED_MODELS:
                    if not any(model in title for model in ALLOWED_MODELS):
                        continue
                
                if ALLOWED_RAM:
                    if not any(ram in title for ram in ALLOWED_RAM):
                        continue
                
                if ALLOWED_SSD:
                    if not any(ssd in title for ssd in ALLOWED_SSD):
                        continue
                
                mac_minis.append({
                    'title': title,
                    'price': price,
                    'link': link
                })
                
            except Exception as e:
                print(f"⚠️ Ürün parse hatası: {e}")
                continue
        
        return mac_minis
        
    except Exception as e:
        print(f"❌ Scrape hatası: {e}")
        return []

def main():
    # ✅ TEST EMAIL GÖNDER
    print("📧 Test email gönderiliyor...")
    test_body = """
    <html>
    <body>
    <h2>✅ MAC MINI TRACKER TEST EMAIL</h2>
    <p><strong>Sistem başarıyla çalışıyor!</strong></p>
    <p>Bu test email'idir. Tracker aktif ve her 5 dakikada çalışıyor.</p>
    <p>Uygun Mac Mini bulunduğunda email alacaksınız!</p>
    <hr>
    <p style="color: #666;">Fiyat aralığı: $300-$600</p>
    </body>
    </html>
    """
    send_email("✅ Mac Mini Tracker - Test Email", test_body)
    
    # Normal kontrol
    print("🔍 Apple refurbished Mac mini kontrol ediliyor...")
    
    macs = get_apple_refurbished()
    
    if macs:
        print(f"\n🎉 {len(macs)} ADET UYGUN MAC MINI BULUNDU!")
        
        email_body = f"""
        <html>
        <body>
        <h2>🎉 Apple Refurbished Mac Mini Bulundu!</h2>
        <p><strong>{len(macs)} adet uygun Mac mini!</strong></p>
        <hr>
        """
        
        for mac in macs:
            email_body += f"""
            <div style="margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 5px;">
                <h3 style="color: #007aff;">{mac['title']}</h3>
                <p><strong>Fiyat:</strong> ${mac['price']}</p>
                <p><a href="{mac['link']}" style="background: #007aff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">SATIN AL! 🏃‍♂️</a></p>
            </div>
            """
        
        email_body += "</body></html>"
        
        send_email(
            f"🎉 {len(macs)} Mac Mini - ${macs[0]['price']}",
            email_body
        )
        
        for mac in macs:
            print(f"\n💰 {mac['title']}")
            print(f"   Fiyat: ${mac['price']}")
            print(f"   Link: {mac['link']}")
    else:
        print("\n😔 Uygun Mac mini bulunamadı")
        print(f"   Fiyat aralığı: ${MIN_PRICE}-${MAX_PRICE}")

if __name__ == "__main__":
    # TEST EMAIL
    print("📧 Test email gönderiliyor...")
    test_body = """
    <html>
    <body>
    <h2>✅ MAC TRACKER TEST</h2>
    <p>Sistem çalışıyor!</p>
    </body>
    </html>
    """
    send_email("✅ Mac Tracker Test", test_body)
    
    # Normal
    main()

