import bpy, sys, os, math, json, argparse

# Parse args
parser = argparse.ArgumentParser()
parser.add_argument("text")
parser.add_argument("font_key")
parser.add_argument("output_path")
parser.add_argument("--custom_font_path", default=None)
parser.add_argument("--advanced_settings", default="None")

argv = sys.argv[sys.argv.index("--")+1:]
args, _ = parser.parse_known_args(argv)

text = args.text
font_key = args.font_key
output_png = args.output_path
custom_font_path = args.custom_font_path

adv_settings = None
if args.advanced_settings != "None":
    try:
        adv_settings = json.loads(args.advanced_settings)
    except Exception as e:
        print("Failed to parse advanced settings:", e)

bpy.ops.wm.read_factory_settings(use_empty=True)

FONT_MAP = {
    "A4SPEED-Bold":           "Font/A4SPEED-Bold.ttf",
    "Arial":                  "Font/Arial.ttf",
    "BebasNeue-Regular":      "Font/BebasNeue-Regular.ttf",
    "Bold Drop":              "Font/Bold Drop.ttf",
    "Bubblegum":              "Font/Bubblegum.ttf",
    "BurbankBigCondensed-Black": "Font/BurbankBigCondensed-Black.otf",
    "Creamy Soup":            "Font/Creamy Soup.otf",
    "Designer":               "Font/Designer.otf",
    "Heavitas":               "Font/Heavitas.ttf",
    "Kind Daily":             "Font/Kind Daily.ttf",
    "LEMONMILK-Bold":         "Font/LEMONMILK-Bold.otf",
    "Minecrafter.Alt":        "Font/Minecrafter.Alt.ttf",
    "OpenSans-Bold":          "Font/OpenSans-Bold.ttf",
    "PackyGreat":             "Font/PackyGreat.ttf",
    "paladins":               "Font/paladins.ttf",
    "Pricedown Bl":           "Font/Pricedown Bl.otf",
    "Roboto-Regular":         "Font/Roboto-Regular.ttf",
    "Square Game":            "Font/Square Game.otf",
    "Super Greatly":          "Font/Super Greatly.ttf",
    "SuperMario256":          "Font/SuperMario256.ttf",
    "Supersonic Rocketship":  "Font/Supersonic Rocketship.ttf",
    "THEBOLDFONT":            "Font/THEBOLDFONT.ttf",
    "Starjedi":               "Font/Starjedi.ttf",
    "Starjhol":               "Font/Starjhol.ttf",
    "Starjout":               "Font/Starjout.ttf",
}

FONT_SETTINGS = {
    "A4SPEED-Bold":           (1, 0.074, 1, 2, 0.04, None),
    "Arial":                  (1, 0.074, 1, 2, 0.04, None),
    "BebasNeue-Regular":      (1, 0.074, 1, 2, 0.04, None),
    "Bold Drop":              (2, 0.069, 1, 1, 0.074, None),
    "Bubblegum":              (4, 0.069, 4, 2, 0.074, None),
    "BurbankBigCondensed-Black": (7, 0.069, 5, 1, 0.074, None),
    "Creamy Soup":            (5, 0.069, 3, 1, 0.074, None),
    "Designer":               (6, 0.069, 3, 1, 0.074, None),
    "Heavitas":               (6, 0.069, 5, 2, 0.074, None),
    "Kind Daily":             (2, 0.069, 1, 1, 0.074, 0.040),
    "LEMONMILK-Bold":         (7, 0.069, 6, 1, 0.074, 0.029),
    "Minecrafter.Alt":        (1, 0.069, 1, 1, 0.074, 0.039),
    "OpenSans-Bold":          (5, 0.069, 4, 1, 0.074, 0.029),
    "PackyGreat":             (4, 0.069, 3, 1, 0.074, 0.032),
    "paladins":               (1, 0.069, 1, 1, 0.074, 0.032),
    "Pricedown Bl":           (4, 0.069, 3, 1, 0.074, 0.032),
    "Roboto-Regular":         (4, 0.069, 3, 1, 0.074, 0.021),
    "Square Game":            (7, 0.069, 5, 1, 0.074, 0.030),
    "Super Greatly":          (3, 0.069, 2, 1, 0.074, 0.030),
    "SuperMario256":          (1, 0.069, 1, 1, 0.074, 0.030),
    "Supersonic Rocketship":  (5, 0.069, 6, 1, 0.074, 0.030),
    "THEBOLDFONT":            (4, 0.069, 3, 1, 0.074, 0.030),
    "Starjedi":               (5, 0.069, 4, 1, 0.074, 0.029),
    "Starjhol":               (5, 0.069, 4, 1, 0.074, 0.029),
    "Starjout":               (5, 0.069, 4, 1, 0.074, 0.029),
}

if font_key == "CUSTOM" and custom_font_path:
    font_file = custom_font_path
    settings = (7, 0.069, 5, 1, 0.074, 0.030)
else:
    font_file = os.path.join(os.path.dirname(__file__), FONT_MAP.get(font_key, "Font/BurbankBigCondensed-Black.otf"))
    settings = FONT_SETTINGS.get(font_key, (7, 0.069, 5, 1, 0.074, 0.030))

enable_border = True
if adv_settings:
    settings = (
        int(adv_settings.get("curveRes", settings[0])),
        float(adv_settings.get("curveExtrude", settings[1])),
        int(adv_settings.get("borderRes", settings[2])),
        int(adv_settings.get("borderBevelRes", settings[3])),
        float(adv_settings.get("borderExtrude", settings[4])),
        float(adv_settings.get("borderBevelDepth", settings[5]))
    )
    if "enableBorder" in adv_settings and str(adv_settings["enableBorder"]).lower() in ('false', '0', 'f'):
        enable_border = False

if not os.path.exists(font_file):
    raise FileNotFoundError(font_file)
font = bpy.data.fonts.load(font_file)

# ── Build exact same geometry as generate_text.py ──────────────────────────
curve = bpy.data.curves.new(type="FONT", name="TextCurve")
curve.body            = text
curve.font            = font
curve.resolution_u    = settings[0]
curve.extrude         = settings[1]
curve.bevel_depth     = 0
curve.bevel_resolution= 0

main_obj = bpy.data.objects.new("MainText", curve)
bpy.context.collection.objects.link(main_obj)
main_obj.rotation_euler = (1.5708, 0, 0)

objs_to_convert = [main_obj]
if enable_border:
    border_curve = curve.copy()
    border_curve.body            = text
    border_curve.font            = font
    border_curve.resolution_u    = settings[2]
    border_curve.bevel_resolution= settings[3]
    border_curve.extrude         = settings[4]
    border_curve.bevel_depth     = settings[5] if settings[5] is not None else 0.024
    
    border_obj = bpy.data.objects.new("BorderText", border_curve)
    bpy.context.collection.objects.link(border_obj)
    border_obj.rotation_euler = (1.5708, 0, 0)
    border_obj.location.y   += 0.035
    objs_to_convert.append(border_obj)

for obj in objs_to_convert:
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    obj.select_set(False)

def assign(obj, name, color):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = False
    mat.diffuse_color = (*color, 1)
    obj.data.materials.append(mat)

assign(main_obj,   "white", (1, 1, 1))
if enable_border:
    assign(border_obj, "black", (0, 0, 0))

# ── Centre text in view ──────────────────────────────────────────────────────
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
for obj in bpy.context.selected_objects:
    obj.location = (0, 0, 0)

# ── Camera ───────────────────────────────────────────────────────────────────
cam_data = bpy.data.cameras.new("PreviewCam")
cam_data.type = 'ORTHO'
cam_obj = bpy.data.objects.new("PreviewCam", cam_data)
bpy.context.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj

# Position camera front-facing (matching the FBX rotation = 90° on X)
cam_obj.location    = (0, -12, 0)
cam_obj.rotation_euler = (math.pi / 2, 0, 0)

# Auto-fit orthographic scale to text width
bpy.context.view_layer.update()
main_obj.select_set(True)
bpy.context.view_layer.objects.active = main_obj
bpy.ops.object.select_all(action='SELECT')
bpy.ops.view3d.camera_to_view_selected() if False else None   # skip operator – manual fit
bbox_corners = [main_obj.matrix_world @ v.co for v in main_obj.data.vertices]
xs = [c.x for c in bbox_corners]
zs = [c.z for c in bbox_corners]
width  = max(xs) - min(xs) if xs else 4
height = max(zs) - min(zs) if zs else 1
cam_data.ortho_scale = max(width, height) * 1.35 + 1.0

# ── Lighting ─────────────────────────────────────────────────────────────────
def add_sun(name, energy, rotation):
    ldata = bpy.data.lights.new(name, type='SUN')
    ldata.energy = energy
    lobj = bpy.data.objects.new(name, ldata)
    bpy.context.collection.objects.link(lobj)
    lobj.rotation_euler = rotation

add_sun("Key",  3.0, (math.radians(45),  0,               math.radians(30)))
add_sun("Fill", 1.2, (math.radians(30),  math.radians(135), 0))
add_sun("Rim",  0.8, (math.radians(-20), 0,               math.radians(180)))

# ── Render settings ──────────────────────────────────────────────────────────
scene = bpy.context.scene
scene.render.engine      = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.context.scene.eevee, 'taa_render_samples') else 'BLENDER_EEVEE'
scene.render.resolution_x = 800
scene.render.resolution_y = 300
scene.render.resolution_percentage = 100
scene.render.film_transparent = True          # transparent background
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = output_png

# Fast render settings
try:
    scene.eevee.taa_render_samples = 4
except Exception:
    pass

bpy.ops.render.render(write_still=True)
