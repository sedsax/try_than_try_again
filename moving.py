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

def list_neighborhoods_in_district(lines, province, district=""):
    p = turkish_upper(province)
    d = turkish_upper(district) if district else ""
    print(f"\n{p} - {d if d else 'Merkez'} için mahalleler:")
    for line in lines:
        if p in line and (d in line if d else "->" not in line):
            print(f"  - {line}")
    print()

def move_neighborhood(file_path):
    lines = read_lines(file_path)

    while True:
        print("\n--- MAHALLE TAŞIMA ---")
        # Eski adres bilgileri
        old_n = input("Taşınacak mahalle adı: ")
        old_p = input("Eski il: ")
        old_d = input("Eski ilçe/belde (isteğe bağlı): ")

        # Eski adresi bulmak için esnek arama: başı aynı olan satırı da kabul et
        old_n_up = turkish_upper(old_n)
        old_p_up = turkish_upper(old_p)
        old_d_up = turkish_upper(old_d) if old_d else ""
        found_line = None
        for line in lines:
            parts = line.split("->")
            left = parts[0].strip()
            if old_d_up:
                # İlçe/belde varsa tam eşleşme
                if left == f"{old_n_up} {old_p_up}":
                    if old_d_up in line:
                        found_line = line
                        break
            else:
                # İlçe/belde yoksa başı aynı olan satırı kabul et
                if left == f"{old_n_up} {old_p_up}":
                    found_line = line
                    break
        if not found_line:
            print("Girilen mahalle bulunamadı. Lütfen tekrar deneyin.")
            continue

        # Yeni adres bilgileri
        new_p = input("Yeni il: ")
        new_d = input("Yeni ilçe/belde (isteğe bağlı): ")
        new_c = input("Yeni merkez tipi (isteğe bağlı): ")

        new_address = format_address(old_n, new_p, new_d, new_c)

        lines.remove(found_line)
        lines.append(new_address)
        write_lines(file_path, lines)

        print("Mahalle başarıyla taşındı.")

        list_neighborhoods_in_district(lines, new_p, new_d)
        break

if __name__ == "__main__":
    move_neighborhood("neighborhoods.txt")
