import unicodedata

KEYWORDS = {"province", "district", "province center", "district center"}

def turkish_normalize(text):
    if not isinstance(text, str):
        return ''
    text = text.strip().lower()
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')

def turkish_upper(text):
    replacements = str.maketrans({
        'i': 'İ', 'ı': 'I',
        'ş': 'Ş', 'ğ': 'Ğ',
        'ü': 'Ü', 'ö': 'Ö',
        'ç': 'Ç'
    })
    parts = text.strip().split()
    result = []
    for word in parts:
        if turkish_normalize(word) in KEYWORDS:
            result.append(word.upper())
        else:
            result.append(word.translate(replacements).upper())
    return ' '.join(result)

def read_lines(file_path):
    try:
        with open(file_path, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def write_lines(file_path, lines):
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(f"{line}\n" for line in lines)

def normalize_line(line):
    return turkish_normalize(line)

def address_exists(address, all_lines):
    return normalize_line(address) in map(normalize_line, all_lines)

def format_address(neighborhood, province, district="", center_type=""):
    n = turkish_upper(neighborhood)
    p = turkish_upper(province)
    d = turkish_upper(district) if district else ""
    c = turkish_upper(center_type) if center_type else ""

    if c and not d:
        return f"{n} {p} -> {c}"
    elif d and c:
        return f"{n} {p} -> {d} -> {c}"
    elif d:
        return f"{n} {p} -> {d}"
    elif c:
        return f"{n} {p} -> {c}"
    else:
        return f"{n} {p}"

def list_neighborhoods(file_path, province, district=""):
    lines = read_lines(file_path)
    p_norm = turkish_normalize(province)
    d_norm = turkish_normalize(district)
    found = False

    for line in lines:
        if p_norm in turkish_normalize(line):
            if not district or d_norm in turkish_normalize(line):
                print(" -", line)
                found = True

    if not found:
        print("Kayıt bulunamadı.")

def add_address(file_path):
    lines = read_lines(file_path)

    n = input("Mahalle: ")
    p = input("İl: ")
    d = input("İlçe/Belde (isteğe bağlı): ")
    c = input("Merkez tipi (örn: DISTRICT CENTER): ")

    new_line = format_address(n, p, d, c)

    if address_exists(new_line, lines):
        print("Adres zaten mevcut.")
    else:
        lines.append(new_line)
        write_lines(file_path, lines)
        print("Adres eklendi.")

def delete_neighborhood(file_path):
    lines = read_lines(file_path)

    p = input("Silinecek il: ")
    d = input("Silinecek ilçe/belde: ")
    n = input("Silinecek mahalle adı: ")

    target = turkish_normalize(n)
    updated_lines = [line for line in lines if not (
        turkish_normalize(p) in turkish_normalize(line) and
        turkish_normalize(d) in turkish_normalize(line) and
        target == turkish_normalize(line.split()[0])
    )]

    if len(updated_lines) == len(lines):
        print("Belirtilen mahalle bulunamadı.")
    else:
        write_lines(file_path, updated_lines)
        print("Mahalle silindi.")
        print("\nGüncel mahalle listesi:")
        list_neighborhoods(file_path, p, d)

def update_neighborhood(file_path):
    lines = read_lines(file_path)

    p = input("İl: ")
    d = input("İlçe/Belde: ")
    old_n = input("Güncellenecek mahalle adı: ")

    target = turkish_normalize(old_n)
    found = False

    for i, line in enumerate(lines):
        if (
            turkish_normalize(p) in turkish_normalize(line)
            and turkish_normalize(d) in turkish_normalize(line)
            and target == turkish_normalize(line.split()[0])
        ):
            found = True
            new_n = input("Yeni mahalle adı: ")
            parts = line.split("->")
            parts[0] = format_address(new_n, p, d).split("->")[0]
            lines[i] = " -> ".join(parts)
            break

    if not found:
        print("Mahalle bulunamadı.")
    else:
        write_lines(file_path, lines)
        print("Mahalle güncellendi.")
        print("\nGüncel mahalle listesi:")
        list_neighborhoods(file_path, p, d)

def main():
    file_path = "neighborhoods.txt"

    while True:
        print("\n--- MAHALLE YÖNETİM SİSTEMİ ---")
        print("1. Mahalle Ekle")
        print("2. Mahalle Sil")
        print("3. Mahalle Güncelle")
        print("4. Çıkış")

        choice = input("Bir işlem seçiniz (1-4): ")

        if choice == "1":
            add_address(file_path)
        elif choice == "2":
            delete_neighborhood(file_path)
        elif choice == "3":
            update_neighborhood(file_path)
        elif choice == "4":
            print("Programdan çıkılıyor.")
            break
        else:
            print("Geçersiz seçim. Lütfen 1-4 arasında bir değer giriniz.")

if __name__ == "__main__":
    main()
