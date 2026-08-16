from pathlib import Path

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "pdfs"
OUTPUT_DIR.mkdir(exist_ok=True)

VARIANTS = [
    {
        "key": "boy",
        "url": "https://playywithme.github.io/game/boy/",
        "file": "play-with-me-boy-game-link.pdf",
        "soft": colors.HexColor("#eaf5ff"),
    },
    {
        "key": "girl",
        "url": "https://playywithme.github.io/game/girl/",
        "file": "play-with-me-girl-game-link.pdf",
        "soft": colors.HexColor("#fff0f6"),
    },
    {
        "key": "twins",
        "url": "https://playywithme.github.io/game/twins/",
        "file": "play-with-me-twins-game-link.pdf",
        "soft": colors.HexColor("#eff2ff"),
    },
]


def draw_qr(pdf, url, x, y, size):
    qr = QrCodeWidget(url)
    bounds = qr.getBounds()
    qr_width = bounds[2] - bounds[0]
    qr_height = bounds[3] - bounds[1]
    drawing = Drawing(size, size, transform=[size / qr_width, 0, 0, size / qr_height, 0, 0])
    drawing.add(qr)
    renderPDF.draw(drawing, pdf, x, y)
    pdf.linkURL(url, (x, y, x + size, y + size), relative=0, thickness=0)


def draw_button(pdf, url, x, y, width, height):
    pdf.setFillColor(colors.HexColor("#223126"))
    pdf.roundRect(x, y, width, height, 8, stroke=0, fill=1)
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(x + width / 2, y + 16, "Start the game")
    pdf.linkURL(url, (x, y, x + width, y + height), relative=0, thickness=0)


def draw_pdf(variant):
    output = OUTPUT_DIR / variant["file"]
    width, height = A5
    pdf = canvas.Canvas(str(output), pagesize=A5)

    pdf.setFillColor(colors.HexColor("#f7fbf3"))
    pdf.rect(0, 0, width, height, stroke=0, fill=1)

    pdf.setFillColor(variant["soft"])
    pdf.circle(78, height - 88, 74, stroke=0, fill=1)
    pdf.setFillColor(colors.HexColor("#fff6e8"))
    pdf.circle(width - 66, 82, 88, stroke=0, fill=1)

    margin = 34
    card_x = margin
    card_y = 42
    card_w = width - margin * 2
    card_h = height - 84
    pdf.setFillColor(colors.white)
    pdf.roundRect(card_x, card_y, card_w, card_h, 20, stroke=0, fill=1)
    pdf.setStrokeColor(colors.HexColor("#d6e6d2"))
    pdf.setLineWidth(1)
    pdf.roundRect(card_x, card_y, card_w, card_h, 20, stroke=1, fill=0)

    pdf.setFillColor(colors.HexColor("#7eac7e"))
    pdf.circle(width / 2, height - 112, 28, stroke=0, fill=1)
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(width / 2, height - 121, "+")

    pdf.setFillColor(colors.HexColor("#b58d42"))
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawCentredString(width / 2, height - 172, "A LITTLE GAME")

    pdf.setFillColor(colors.HexColor("#223126"))
    pdf.setFont("Helvetica-Bold", 34)
    pdf.drawCentredString(width / 2, height - 214, "Let's Play")

    pdf.setFillColor(colors.HexColor("#637268"))
    pdf.setFont("Helvetica", 12)
    for offset, line in enumerate([
        "Scan the QR code or tap the button below.",
        "Finish the puzzle to unlock a little surprise.",
    ]):
        pdf.drawCentredString(width / 2, height - 248 - offset * 17, line)

    qr_size = 122
    qr_x = (width - qr_size) / 2
    qr_y = height - 420
    pdf.setFillColor(colors.HexColor("#f7fbf3"))
    pdf.roundRect(qr_x - 14, qr_y - 14, qr_size + 28, qr_size + 28, 16, stroke=0, fill=1)
    draw_qr(pdf, variant["url"], qr_x, qr_y, qr_size)

    draw_button(pdf, variant["url"], width / 2 - 92, 100, 184, 44)

    pdf.setFillColor(colors.HexColor("#637268"))
    pdf.setFont("Helvetica", 8.5)
    pdf.drawCentredString(width / 2, 68, "A tiny challenge is waiting for you.")

    pdf.save()
    return output


def main():
    for variant in VARIANTS:
        print(draw_pdf(variant))


if __name__ == "__main__":
    main()
