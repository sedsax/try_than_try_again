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

if __name__ == "__main__":
    add_address("neighborhoods.txt")
