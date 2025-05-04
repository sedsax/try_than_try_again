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

def list_neighborhoods_in_region(lines, province, district=""):
    p = turkish_upper(province)
    d = turkish_upper(district) if district else ""

    print("\nGüncel mahalle listesi:")
    for line in lines:
        if d and f"{p} -> {d}" in line:
            print(line)
        elif not d and p in line:
            print(line)

def update_neighborhood(file_path):
    lines = read_lines(file_path)

    while True:
        old_n = input("Güncellenecek Mahalle: ")
        p = input("İl: ")
        d = input("İlçe/Belde (isteğe bağlı): ")
        c = input("Merkez tipi (örn: DISTRICT CENTER): ")

        old_line = format_address(old_n, p, d, c)

        normalized_lines = list(map(normalize_line, lines))
        if normalize_line(old_line) in normalized_lines:
            index = normalized_lines.index(normalize_line(old_line))
            new_n = input("Yeni Mahalle Adı: ")
            new_line = format_address(new_n, p, d, c)

            lines[index] = new_line
            write_lines(file_path, lines)
            print(f"\nMahalle güncellendi:\n{old_line} -> {new_line}")
            list_neighborhoods_in_region(lines, p, d)
            break
        else:
            print("Adres bulunamadı. Lütfen bilgileri kontrol edin ve tekrar deneyin.\n")

if __name__ == "__main__":
    update_neighborhood("neighborhoods.txt")
