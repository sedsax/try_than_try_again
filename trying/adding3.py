import os
import unicodedata

def turkish_normalize(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').casefold()

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
        neighborhood = input("Mahalle adı: ").strip().upper()
        province = input("İl adı: ").strip().upper()
        district_or_center = input("İlçe/Belde/İl Merkezi adı: ").strip().upper()
        center_type = input("Bağlı olduğu merkez tipi (örn: 'ORTAHİSAR-DISTRICT CENTER', 'ADIYAMAN-PROVINCE CENTER', 'KOCAÖZ'): ").strip().upper()

        # Aynı mahalle, il, ilçe/belde/il merkezi var mı kontrol et
        exists = False
        for line in neighborhoods:
            n, p, d, c = parse_line(line)
            if n == neighborhood and p == province and d == district_or_center and c == center_type:
                exists = True
                break

        if exists:
            print("Bu mahalle zaten mevcut! Lütfen farklı bir mahalle girin.")
            continue

        # Format: MAHALLE İL -> İLÇE/BELDE/İL MERKEZİ -> MERKEZ TİPİ
        if center_type:
            new_line = f"{neighborhood} {province} -> {district_or_center} -> {center_type}"
        else:
            new_line = f"{neighborhood} {province} -> {district_or_center}"
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
        if p == province and d == district_or_center and c == center_type:
            print("-", n)
            found = True
    if not found:
        print("Kayıtlı mahalle bulunamadı.")

def main():
    file_path = "neighborhoods.txt"
    add_neighborhood(file_path)

if __name__ == "__main__":
    main()