import os
import tempfile
import subprocess
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


# SVG -> PNG without CairoSVG
def load_image(path):
    if not path.lower().endswith(".svg"):
        return Image.open(path).convert("RGBA")

    # Temporary PNG
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        png_path = tmp.name

    try:
        subprocess.run(
            [
                "magick",
                path,
                "-background", "none",
                "PNG32:" + png_path
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return Image.open(png_path).convert("RGBA").copy()

    finally:
        if os.path.exists(png_path):
            os.remove(png_path)


# Load images
img = Image.open("skidpad_mac_Mesa_de_trabajo_1.png").convert("RGBA")
ev = Image.open("ev.png").convert("RGBA")
cv = Image.open("cv.png").convert("RGBA")
cv = cv.resize((61, 61), Image.Resampling.LANCZOS)
ev = ev.resize((61, 61), Image.Resampling.LANCZOS)

df = pd.read_excel('MFU_FSS_2026_20260729_1031.xlsx')
lines = df.astype(str).values.tolist()
heads = lines[0]
lines = lines[1:]

clean_lines = {}
classics = False

for line in lines:
    if line[7] == "CLASSIC" and not classics:
        continue
    if line[7] == "CLASSIC" and classics:
        continue

    clean_lines[line[3]] = {
        key: value for key, value in zip(heads, line)
    }


def get_banner(line):
    width, height = 408, 61

    # Gradient
    color = line["Primary Colour"]

    if not color.startswith("#"):
        color = "#ffffff"

    rgb = tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))

    rectangle = Image.new("RGBA", (width, height), rgb)
    # rectangle = Image.new("RGBA", (width, height), (0, 0, 0, 0))rgb

    # for x in range(width):
    #     alpha = int(255 * (1 - x / (width - 1)))
    #     rectangle.paste((*rgb, alpha), (x, 0, x + 1, height))

    # Logo
    try:
        img_path = (
            f"images/logos_square/" f"{line['Square Logo (filename)']}")
        square_logo = load_image(img_path)
    except (FileNotFoundError, OSError, subprocess.CalledProcessError):
        square_logo = Image.new("RGBA", (height, height), (255, 255, 255, 255))

    # Remove transparent padding around the logo
    alpha = square_logo.getchannel("A")
    bbox = alpha.getbbox()

    if bbox:
        square_logo = square_logo.crop(bbox)

    logo_height = height
    logo_ratio = (square_logo.width / square_logo.height)
    logo_width = round(logo_height * logo_ratio)
    square_logo = square_logo.resize(
        (logo_width, logo_height), Image.Resampling.LANCZOS)
    rectangle.paste(square_logo, (0, 0), square_logo)

    text = line["Aka Name"]
    draw = ImageDraw.Draw(rectangle)

    text_left = 80
    text_right = width - 10
    available_width = (text_right - text_left)

    font_path = "Montserrat-SemiBoldItalic.ttf"
    font_size = 29

    # Automatically shrink text until it fits
    while font_size > 5:

        font = ImageFont.truetype(font_path, size=font_size)

        bbox = draw.textbbox((0, 0), text, font=font)

        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        if (text_width <= available_width and text_height <= height):
            break

        font_size -= 1

    # Center text inside fixed text area
    x = (text_left + (available_width - text_width) // 2 - bbox[0])
    y = ((height - text_height) // 2 - bbox[1])

    draw.text((x, y), text, font=font, fill="white")

    return rectangle


# Generate images
teams = []

for key in clean_lines:

    line = clean_lines[key]
    img = Image.open("skidpad_mac_Mesa_de_trabajo_1 copy.png").convert("RGBA")

    team = line["Aka Name"]
    number = line["#"]
    university = line["University"]

    # Team banner
    banner = get_banner(line)
    banner.save(f"../static/icons/team_parts/{number}.png", "PNG")

    img.paste(banner, (118, 29), banner)

    if ("ev" if "electric" in line["Powertrain"].lower() else "cv") == "cv":
        img.paste(cv, (0, 29), cv)
    else:
        img.paste(ev, (0, 29), ev)

    draw = ImageDraw.Draw(img)

    # Number
    font = ImageFont.truetype("Montserrat-SemiBoldItalic.ttf", size=29)

    x_min, x_max = 58, 117
    y_min, y_max = 29, 88
    bbox = draw.textbbox((0, 0), str(number), font=font)

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (x_min + (x_max - x_min - text_width) // 2 - bbox[0])
    y = (y_min + (y_max - y_min - text_height) // 2 - bbox[1])

    draw.text((x, y), str(number), font=font, fill="#232323")

    # University
    font = ImageFont.truetype("MYRIADPRO-REGULAR.OTF", size=19)

    x_min, x_max = 117, 519
    y_min, y_max = 0, 30

    bbox = draw.textbbox((0, 0), university, font=font)

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (x_min + (x_max - x_min - text_width) // 2 - bbox[0])
    y = (y_min + (y_max - y_min - text_height) // 2 - bbox[1])
    draw.text((x, y), university, font=font, fill="white")

    img.save(f"../static/images/current_team/{number}.png", "PNG")
    print(f"Saved image for team {number} - {team}")
