"""Turn files into (text, page) sections. Supports PDF, DOCX, TXT and MD."""
import math
import re
from pathlib import Path

SUPPORTED = {".pdf", ".docx", ".txt", ".md"}

# English letter frequencies (%), used to tell real text from scrambled text.
_FREQ = dict(zip("etaoinshrdlcumwfgypbvkjxqz",
                 [12.7, 9.1, 8.2, 7.5, 7.0, 6.7, 6.3, 6.1, 6.0, 4.3, 4.0, 2.8, 2.8, 2.4, 2.4, 2.2, 2.0,
                  2.0, 1.9, 1.5, 1.0, 0.8, 0.15, 0.15, 0.1, 0.07]))


def _englishness(text):
    """Average log-frequency of the letters: about -3.0 for English, much lower for gibberish."""
    letters = [c for c in text.lower() if "a" <= c <= "z"]
    if len(letters) < 4:
        return -9.0
    return sum(math.log(_FREQ[c] / 100) for c in letters) / len(letters)


def _shift(text):
    # Some PDFs (NCERT books among them) embed fonts whose glyph codes are 29 below ASCII:
    # "WKH" is "the" and \x03 is a space. Shift those codes back up.
    return "".join(chr(ord(c) + 29) if ord(c) <= 0x5D and c != " " else c for c in text)


def fix_shifted_font(text):
    """Decode lines that use the shifted font encoding; leave normal lines alone."""
    out = []
    for line in text.splitlines():
        shifted = _shift(line)
        out.append(shifted if _englishness(shifted) > _englishness(line) + 0.4 else line)
    return "\n".join(out)


def _clean(text):
    text = text.replace("\x00", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"-\n(?=[a-z])", "", text)  # re-join words hyphenated across lines
    return text.strip()


def load_pdf(path):
    from pypdf import PdfReader

    for i, page in enumerate(PdfReader(path).pages, start=1):
        text = _clean(fix_shifted_font(page.extract_text() or ""))
        if text:
            yield text, i


def load_docx(path):
    import docx

    doc = docx.Document(path)
    parts = [p.text for p in doc.paragraphs if p.text.strip()]
    for table in doc.tables:
        for row in table.rows:
            parts.append(" | ".join(cell.text.strip() for cell in row.cells))
    text = _clean("\n".join(parts))
    if text:
        yield text, None


def load_text(path):
    text = _clean(Path(path).read_text(encoding="utf-8", errors="replace"))
    if text:
        yield text, None


def load(path):
    """Yield (text, page_number_or_None) for one file."""
    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        yield from load_pdf(path)
    elif ext == ".docx":
        yield from load_docx(path)
    elif ext in (".txt", ".md"):
        yield from load_text(path)
