
def clean_phrase(string: str):
    clean = string.replace(',', '')
    clean = clean.replace('.', '')
    clean = clean.replace('\n', '')
    clean = clean.replace('\r', '')
    clean = clean.lower()
    clean = clean.strip()
    return clean