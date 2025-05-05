from flask import Flask, request, send_file, jsonify
from PIL import Image
import io
import webcolors

app = Flask(__name__, static_url_path='/', static_folder='web')

@app.route("/")
def index():
    return send_file("web/index.html")

def closest_color(rgb_tuple):
    min_colors = {}
    for hex_value, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(hex_value)
        rd = (r_c - rgb_tuple[0]) ** 2
        gd = (g_c - rgb_tuple[1]) ** 2
        bd = (b_c - rgb_tuple[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]

@app.route("/analyze", methods=["POST"])
def analyze():
    if 'image' not in request.files:
        return "Kein Bild hochgeladen", 400

    image = request.files['image']
    img = Image.open(image.stream).convert("RGB").resize((100, 100))
    colors = img.getcolors(10000)
    dominant = max(colors, key=lambda tup: tup[0])[1]

    color_name = closest_color(dominant)

    return jsonify({
        "dominant_color": dominant,
        "color_name": color_name
    })

@app.route("/colorbox")
def colorbox():
    r = int(request.args.get("r", 0))
    g = int(request.args.get("g", 0))
    b = int(request.args.get("b", 0))

    preview = Image.new("RGB", (300, 300), (r, g, b))
    buffer = io.BytesIO()
    preview.save(buffer, format="PNG")
    buffer.seek(0)
    return send_file(buffer, mimetype="image/png")
