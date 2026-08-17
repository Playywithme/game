from pathlib import Path
import math
import shutil

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
WORK_ROOT = ROOT.parents[1]
REPO_OUTPUT_DIR = ROOT / "pdfs"
FINAL_OUTPUT_DIR = WORK_ROOT / "outputs" / "pdfs"
REPO_OUTPUT_DIR.mkdir(exist_ok=True)
FINAL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CREAM = colors.HexColor("#FBF7EC")
CREAM_DARK = colors.HexColor("#F3ECDB")
INK = colors.HexColor("#3B4A3C")
MUTED = colors.HexColor("#7C8A76")
SAGE = colors.HexColor("#A7C79E")
SAGE_DEEP = colors.HexColor("#6E9B77")
GOLD = colors.HexColor("#C7A24B")
LINE = colors.HexColor("#E3DAC4")
WHITE = colors.white

VARIANTS = [
    {
        "key": "boy",
        "url": "https://playywithme.github.io/game/boy/play/",
        "file": "play-with-me-boy-game-link.pdf",
    },
    {
        "key": "girl",
        "url": "https://playywithme.github.io/game/girl/",
        "file": "play-with-me-girl-game-link.pdf",
    },
    {
        "key": "twins",
        "url": "https://playywithme.github.io/game/twins/",
        "file": "play-with-me-twins-game-link.pdf",
    },
]


def lerp(a, b, t):
    return a + (b - a) * t


def blend(c1, c2, t):
    return colors.Color(
        lerp(c1.red, c2.red, t),
        lerp(c1.green, c2.green, t),
        lerp(c1.blue, c2.blue, t),
    )


def draw_soft_background(pdf, width, height):
    steps = 70
    for i in range(steps):
        t = i / (steps - 1)
        pdf.setFillColor(blend(CREAM, CREAM_DARK, t))
        pdf.rect(0, height * t, width, height / steps + 1, stroke=0, fill=1)

    pdf.setFillColor(colors.Color(SAGE.red, SAGE.green, SAGE.blue, alpha=0.18))
    pdf.circle(54, height - 70, 86, stroke=0, fill=1)
    pdf.setFillColor(colors.Color(GOLD.red, GOLD.green, GOLD.blue, alpha=0.12))
    pdf.circle(width - 45, height - 92, 78, stroke=0, fill=1)
    pdf.setFillColor(colors.Color(SAGE.red, SAGE.green, SAGE.blue, alpha=0.14))
    pdf.circle(width - 35, 92, 98, stroke=0, fill=1)


def draw_star(pdf, x, y, r, color, alpha=0.82):
    pts = []
    for i in range(8):
        angle = math.pi / 4 * i - math.pi / 2
        radius = r if i % 2 == 0 else r * 0.33
        pts.extend([x + math.cos(angle) * radius, y + math.sin(angle) * radius])
    pdf.setFillColor(colors.Color(color.red, color.green, color.blue, alpha=alpha))
    path = pdf.beginPath()
    path.moveTo(pts[0], pts[1])
    for p in range(2, len(pts), 2):
        path.lineTo(pts[p], pts[p + 1])
    path.close()
    pdf.drawPath(path, stroke=0, fill=1)


def draw_cloud(pdf, x, y, scale=1.0, alpha=0.66):
    pdf.setFillColor(colors.Color(WHITE.red, WHITE.green, WHITE.blue, alpha=alpha))
    pdf.ellipse(x - 34 * scale, y - 10 * scale, x + 34 * scale, y + 12 * scale, stroke=0, fill=1)
    pdf.circle(x - 18 * scale, y + 4 * scale, 14 * scale, stroke=0, fill=1)
    pdf.circle(x + 14 * scale, y + 6 * scale, 17 * scale, stroke=0, fill=1)


def draw_moon(pdf, x, y, scale=1.0):
    pdf.setFillColor(colors.Color(GOLD.red, GOLD.green, GOLD.blue, alpha=0.82))
    pdf.circle(x, y, 29 * scale, stroke=0, fill=1)
    pdf.setFillColor(CREAM)
    pdf.circle(x + 14 * scale, y + 8 * scale, 28 * scale, stroke=0, fill=1)
    pdf.setStrokeColor(colors.Color(INK.red, INK.green, INK.blue, alpha=0.5))
    pdf.setLineWidth(1.2)
    path = pdf.beginPath()
    path.moveTo(x + 1 * scale, y - 3 * scale)
    path.curveTo(x + 6 * scale, y - 8 * scale, x + 14 * scale, y - 8 * scale, x + 19 * scale, y - 3 * scale)
    pdf.drawPath(path, stroke=1, fill=0)


def draw_balloon(pdf, x, y, scale=1.0):
    pdf.setFillColor(colors.Color(CREAM.red, CREAM.green, CREAM.blue, alpha=0.82))
    pdf.ellipse(x - 30 * scale, y - 39 * scale, x + 30 * scale, y + 39 * scale, stroke=0, fill=1)
    pdf.setStrokeColor(colors.Color(SAGE_DEEP.red, SAGE_DEEP.green, SAGE_DEEP.blue, alpha=0.78))
    pdf.setLineWidth(1)
    pdf.ellipse(x - 30 * scale, y - 39 * scale, x + 30 * scale, y + 39 * scale, stroke=1, fill=0)
    for offset in (-15, 0, 15):
        path = pdf.beginPath()
        path.moveTo(x + offset * 0.15 * scale, y + 39 * scale)
        path.curveTo(x + offset * scale, y + 18 * scale, x + offset * scale, y - 18 * scale, x, y - 39 * scale)
        pdf.drawPath(path, stroke=1, fill=0)
    pdf.line(x - 28 * scale, y, x + 28 * scale, y)
    pdf.setFillColor(colors.Color(GOLD.red, GOLD.green, GOLD.blue, alpha=0.78))
    pdf.roundRect(x - 12 * scale, y - 59 * scale, 24 * scale, 14 * scale, 2 * scale, stroke=0, fill=1)
    pdf.setStrokeColor(colors.Color(SAGE_DEEP.red, SAGE_DEEP.green, SAGE_DEEP.blue, alpha=0.72))
    pdf.line(x - 19 * scale, y - 35 * scale, x - 8 * scale, y - 45 * scale)
    pdf.line(x + 19 * scale, y - 35 * scale, x + 8 * scale, y - 45 * scale)


def draw_sprig(pdf, x, y, rotation, scale=1.0, flip=1):
    pdf.saveState()
    pdf.translate(x, y)
    pdf.rotate(rotation)
    pdf.scale(scale * flip, scale)
    pdf.setStrokeColor(colors.Color(SAGE_DEEP.red, SAGE_DEEP.green, SAGE_DEEP.blue, alpha=0.55))
    pdf.setLineWidth(1.2)
    pdf.line(0, 0, 0, 82)
    for i in range(6):
        yy = 12 + i * 12
        r = 6.7 - i * 0.35
        pdf.setFillColor(colors.Color(SAGE.red, SAGE.green, SAGE.blue, alpha=0.78))
        pdf.ellipse(-16, yy - r / 2, -3, yy + r / 2, stroke=0, fill=1)
        pdf.setFillColor(colors.Color(SAGE_DEEP.red, SAGE_DEEP.green, SAGE_DEEP.blue, alpha=0.72))
        pdf.ellipse(3, yy - r / 2, 16, yy + r / 2, stroke=0, fill=1)
    pdf.restoreState()


def draw_qr(pdf, url, x, y, size):
    qr = QrCodeWidget(url)
    bounds = qr.getBounds()
    qr_width = bounds[2] - bounds[0]
    qr_height = bounds[3] - bounds[1]
    drawing = Drawing(size, size, transform=[size / qr_width, 0, 0, size / qr_height, 0, 0])
    drawing.add(qr)
    renderPDF.draw(drawing, pdf, x, y)


def draw_button(pdf, url, x, y, width, height):
    pdf.setFillColor(INK)
    pdf.roundRect(x, y, width, height, 9, stroke=0, fill=1)
    pdf.setFillColor(WHITE)
    pdf.setFont("Helvetica-Bold", 15)
    pdf.drawCentredString(x + width / 2, y + 15, "Start the game")
    # The button is the only clickable area in the PDF.
    pdf.linkURL(url, (x, y, x + width, y + height), relative=0, thickness=0)


def draw_pdf(variant):
    output = REPO_OUTPUT_DIR / variant["file"]
    width, height = A5
    pdf = canvas.Canvas(str(output), pagesize=A5)

    draw_soft_background(pdf, width, height)

    card_x = 26
    card_y = 28
    card_w = width - card_x * 2
    card_h = height - card_y * 2
    pdf.setFillColor(colors.Color(WHITE.red, WHITE.green, WHITE.blue, alpha=0.58))
    pdf.roundRect(card_x, card_y, card_w, card_h, 22, stroke=0, fill=1)
    pdf.setStrokeColor(colors.Color(GOLD.red, GOLD.green, GOLD.blue, alpha=0.48))
    pdf.setLineWidth(1)
    pdf.roundRect(card_x + 7, card_y + 7, card_w - 14, card_h - 14, 17, stroke=1, fill=0)

    draw_sprig(pdf, card_x + 25, height - 110, 160, 0.78, 1)
    draw_sprig(pdf, width - card_x - 25, height - 110, -160, 0.78, -1)
    draw_sprig(pdf, card_x + 34, card_y + 17, -18, 0.7, 1)
    draw_sprig(pdf, width - card_x - 34, card_y + 17, 18, 0.7, -1)

    draw_moon(pdf, width * 0.28, height - 132, 0.88)
    draw_balloon(pdf, width * 0.72, height - 126, 0.82)
    draw_cloud(pdf, width * 0.44, height - 144, 0.58)
    draw_cloud(pdf, width * 0.18, height - 246, 0.48, 0.46)
    draw_cloud(pdf, width * 0.82, height - 247, 0.42, 0.42)

    for x, y, r, color in [
        (92, height - 66, 4, GOLD),
        (145, height - 88, 3, SAGE_DEEP),
        (width - 106, height - 67, 3.5, GOLD),
        (width - 70, height - 214, 4, SAGE_DEEP),
        (80, 185, 3.8, GOLD),
        (width - 92, 175, 3.4, GOLD),
        (width / 2 + 76, height - 204, 3.2, SAGE_DEEP),
    ]:
        draw_star(pdf, x, y, r, color)

    pdf.setFillColor(GOLD)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawCentredString(width / 2, height - 248, "A LITTLE GAME")

    pdf.setFillColor(INK)
    pdf.setFont("Times-BoldItalic", 37)
    pdf.drawCentredString(width / 2, height - 292, "Let's Play")

    pdf.setStrokeColor(colors.Color(GOLD.red, GOLD.green, GOLD.blue, alpha=0.55))
    pdf.setLineWidth(0.75)
    divider_y = height - 305
    pdf.line(width / 2 - 50, divider_y, width / 2 - 10, divider_y)
    draw_star(pdf, width / 2, divider_y, 4.6, GOLD, 0.95)
    pdf.line(width / 2 + 10, divider_y, width / 2 + 50, divider_y)

    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 11.5)
    pdf.drawCentredString(width / 2, height - 331, "Finish the little puzzle to")
    pdf.drawCentredString(width / 2, height - 347, "unlock a sweet surprise.")

    qr_size = 96
    qr_x = (width - qr_size) / 2
    qr_y = 124
    pdf.setFillColor(colors.Color(WHITE.red, WHITE.green, WHITE.blue, alpha=0.82))
    pdf.roundRect(qr_x - 13, qr_y - 13, qr_size + 26, qr_size + 26, 14, stroke=0, fill=1)
    pdf.setStrokeColor(colors.Color(LINE.red, LINE.green, LINE.blue, alpha=0.8))
    pdf.roundRect(qr_x - 13, qr_y - 13, qr_size + 26, qr_size + 26, 14, stroke=1, fill=0)
    draw_qr(pdf, variant["url"], qr_x, qr_y, qr_size)

    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica-Bold", 7.5)
    pdf.drawCentredString(width / 2, qr_y - 26, "SCAN ME")

    draw_button(pdf, variant["url"], width / 2 - 86, 48, 172, 42)

    pdf.setFillColor(colors.Color(MUTED.red, MUTED.green, MUTED.blue, alpha=0.82))
    pdf.setFont("Helvetica", 7.5)
    pdf.drawCentredString(width / 2, 24, "MADE WITH LOVE")

    pdf.setTitle("Play With Me")
    pdf.setAuthor("Play With Me")
    pdf.setSubject("Puzzle game link")
    pdf.save()

    final_output = FINAL_OUTPUT_DIR / variant["file"]
    shutil.copyfile(output, final_output)
    return output, final_output


def main():
    for variant in VARIANTS:
        repo_output, final_output = draw_pdf(variant)
        print(repo_output)
        print(final_output)


if __name__ == "__main__":
    main()
