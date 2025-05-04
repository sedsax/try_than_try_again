import os
import unicodedata
import locale

def turkish_normalize(text):
    if not isinstance(text, str):
        return ''
    # Türkçe karakterleri ASCII'ye çevirip küçük harfe dönüştürür
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').casefold().strip()

def turkish_upper(text):
    if not isinstance(text, str):
        return ''
    # İngilizce anahtar kelimeler bozulmasın
    keywords = ["PROVINCE CENTER", "DISTRICT CENTER", "PROVINCE", "DISTRICT"]
    for kw in keywords:
        if kw.lower() in text.lower():
            # Sadece anahtar kelimeyi büyük harfe çevir, kalanını Türkçe büyüt
            parts = text.split()
            result = []
            for part in parts:
                if part.lower() in [k.lower() for k in keywords]:
                    result.append(part.upper())
                else:
                    p = part.replace('i', 'İ').replace('ı', 'I')
                    p = p.replace('ş', 'Ş').replace('ğ', 'Ğ').replace('ü', 'Ü').replace('ö', 'Ö').replace('ç', 'Ç')
                    result.append(p.upper())
            return ' '.join(result)
    # Anahtar kelime yoksa klasik Türkçe büyütme
    text = text.replace('i', 'İ').replace('ı', 'I')
    text = text.replace('ş', 'Ş').replace('ğ', 'Ğ').replace('ü', 'Ü').replace('ö', 'Ö').replace('ç', 'Ç')
    return text.upper()

def load_neighborhoods(file_path):
    """Dosyadan mahalle verilerini oku ve satır listesi olarak döndür."""
    neighborhoods = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            neighborhoods = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("Hata: neighborhoods.txt dosyası bulunamadı.")
    except Exception as e:
        print(f"Okuma hatası: {e}")
    return neighborhoods

def save_neighborhoods(file_path, neighborhoods):
    """Mahalle listesini dosyaya kaydet."""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            for item in neighborhoods:
                file.write(item + "\n")
    except Exception as e:
        print(f"Yazma hatası: {e}")

def parse_line(line):
    """
    Bir satırı (ör: 'ÜNİVERSİTE TRABZON -> ORTAHİSAR -> ORTAHİSAR-DISTRICT CENTER')
    mahalle, il, ilçe/belde/il merkezi olarak ayırır.
    """
    try:
        parts = line.split("->")
        left = parts[0].strip()
        right1 = parts[1].strip() if len(parts) > 1 else ""
        right2 = parts[2].strip() if len(parts) > 2 else ""
        # left: 'ÜNİVERSİTE TRABZON'
        # right1: 'ORTAHİSAR'
        # right2: 'ORTAHİSAR-DISTRICT CENTER'
        if " " in left:
            neighborhood, province = left.rsplit(" ", 1)
        else:
            neighborhood, province = left, ""
        return neighborhood.upper(), province.upper(), right1.upper(), right2.upper()
    except Exception:
        return "", "", "", ""

def add_neighborhood(file_path):
    """Kullanıcıdan mahalle, il, ilçe/belde/il merkezi alıp ekleme işlemini yapar."""
    neighborhoods = load_neighborhoods(file_path)
    if neighborhoods is None:
        return

    while True:
        neighborhood = input("Mahalle adı: ").strip()
        province = input("İl adı: ").strip()
        district_or_center = input("İlçe/Belde adı: ").strip()
        center_type = input("Bağlı olduğu merkez tipi (örn: 'ORTAHİSAR-DISTRICT CENTER', 'ADIYAMAN-PROVINCE CENTER', 'KOCAÖZ'): ").strip()

        # İl merkezine bağlı mahalle için özel durum
        is_province_center = (
            not district_or_center and center_type and
            turkish_normalize(center_type).endswith("province center")
        )

        # Aynı mahalle, il, ilçe/belde/il merkezi var mı kontrol et (normalize ederek)
        exists = False
        for line in neighborhoods:
            n, p, d, c = parse_line(line)
            # İl merkezine bağlı mahalle için iki formatı da kontrol et
            if is_province_center:
                # Format: MAHALLE İL -> İL-PROVINCE CENTER
                check_line = f"{turkish_upper(neighborhood)} {turkish_upper(province)} -> {turkish_upper(province)}-PROVINCE CENTER"
                if turkish_normalize(line) == turkish_normalize(check_line):
                    exists = True
                    break
            else:
                if (
                    turkish_normalize(n) == turkish_normalize(neighborhood) and
                    turkish_normalize(p) == turkish_normalize(province) and
                    turkish_normalize(d) == turkish_normalize(district_or_center) and
                    turkish_normalize(c) == turkish_normalize(center_type)
                ):
                    exists = True
                    break

        if exists:
            print("Bu mahalle zaten mevcut! Lütfen farklı bir mahalle girin.")
            continue

        # Format: MAHALLE İL -> İL-PROVINCE CENTER (il merkezine bağlı mahalle için)
        if is_province_center:
            new_line = f"{turkish_upper(neighborhood)} {turkish_upper(province)} -> {turkish_upper(province)}-PROVINCE CENTER"
        # Normal format (ilçe/belde/il merkezi doluysa)
        elif district_or_center and center_type:
            new_line = f"{turkish_upper(neighborhood)} {turkish_upper(province)} -> {turkish_upper(district_or_center)} -> {turkish_upper(center_type)}"
        # Sadece ilçe/belde/il merkezi varsa
        elif district_or_center:
            new_line = f"{turkish_upper(neighborhood)} {turkish_upper(province)} -> {turkish_upper(district_or_center)}"
        # Sadece merkez tipi varsa (istisnai durum)
        elif center_type:
            new_line = f"{turkish_upper(neighborhood)} {turkish_upper(province)} -> {turkish_upper(center_type)}"
        else:
            new_line = f"{turkish_upper(neighborhood)} {turkish_upper(province)}"

        # Satırın normalize hali mevcutsa ekleme
        if any(turkish_normalize(line) == turkish_normalize(new_line) for line in neighborhoods):
            print("Bu mahalle zaten mevcut! Lütfen farklı bir mahalle girin.")
            continue

        neighborhoods.append(new_line)
        save_neighborhoods(file_path, neighborhoods)
        print("Mahalle başarıyla eklendi.\n")
        list_neighborhoods(neighborhoods, province, district_or_center, center_type)
        break

def list_neighborhoods(neighborhoods, province, district_or_center, center_type):
    """Belirtilen il, ilçe/belde/il merkezi ve merkez tipindeki mahalleleri listeler."""
    print(f"\n{province} ili, {district_or_center} ({center_type}) bölgesindeki mahalleler:")
    found = False
    for line in neighborhoods:
        n, p, d, c = parse_line(line)
        if (turkish_normalize(p) == turkish_normalize(province) and
            turkish_normalize(d) == turkish_normalize(district_or_center) and
            turkish_normalize(c) == turkish_normalize(center_type)):
            print("-", n)
            found = True
    if not found:
        print("Kayıtlı mahalle bulunamadı.")

def main():
    file_path = "neighborhoods.txt"
    add_neighborhood(file_path)

if __name__ == "__main__":
    main()