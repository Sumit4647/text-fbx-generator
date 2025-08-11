import bpy, sys, os

# Parse args: text, font_key, output_path
argv = sys.argv[sys.argv.index("--")+1:]
text, font_key, output_path = argv

# Reset scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Font mapping
FONT_MAP = {
    "A4SPEED-Bold": "Font/A4SPEED-Bold.ttf",
    "Arial": "Font/Arial.ttf",
    "BebasNeue-Regular": "Font/BebasNeue-Regular.ttf",
    "Bold Drop": "Font/Bold Drop.ttf",
    "Bubblegum": "Font/Bubblegum.ttf",
    "BurbankBigCondensed-Black": "Font/BurbankBigCondensed-Black.otf",
    "Creamy Soup": "Font/Creamy Soup.otf",
    "Designer": "Font/Designer.otf",
    "Heavitas": "Font/Heavitas.ttf",
    "Kind Daily": "Font/Kind Daily.ttf",
    "LEMONMILK-Bold": "Font/LEMONMILK-Bold.otf",
    "Minecrafter.Alt": "Font/Minecrafter.Alt.ttf",
    "OpenSans-Bold": "Font/OpenSans-Bold.ttf",
    "PackyGreat": "Font/PackyGreat.ttf",
    "paladins": "Font/paladins.ttf",
    "Pricedown Bl": "Font/Pricedown Bl.otf",
    "Roboto-Regular": "Font/Roboto-Regular.ttf",
    "Square Game": "Font/Square Game.otf",
    "Super Greatly": "Font/Super Greatly.ttf",
    "SuperMario256": "Font/SuperMario256.ttf",
    "Supersonic Rocketship": "Font/Supersonic Rocketship.ttf",
    "THEBOLDFONT": "Font/THEBOLDFONT.ttf",
}

# Per-font style settings
FONT_SETTINGS = {
    "A4SPEED-Bold": dict(curve_res=1, curve_ext=0.074, border_res=1, border_bevel_res=2, border_ext=0.04, border_bevel_depth=None),
    "Arial": dict(curve_res=1, curve_ext=0.074, border_res=1, border_bevel_res=2, border_ext=0.04, border_bevel_depth=None),
    "BebasNeue-Regular": dict(curve_res=1, curve_ext=0.074, border_res=1, border_bevel_res=2, border_ext=0.04, border_bevel_depth=None),
    "Bold Drop": dict(curve_res=2, curve_ext=0.069, border_res=1, border_bevel_res=1, border_ext=0.074, border_bevel_depth=None),
    "Bubblegum": dict(curve_res=4, curve_ext=0.069, border_res=4, border_bevel_res=2, border_ext=0.074, border_bevel_depth=None),
    "BurbankBigCondensed-Black": dict(curve_res=7, curve_ext=0.069, border_res=5, border_bevel_res=1, border_ext=0.074, border_bevel_depth=None),
    "Creamy Soup": dict(curve_res=5, curve_ext=0.069, border_res=3, border_bevel_res=1, border_ext=0.074, border_bevel_depth=None),
    "Designer": dict(curve_res=6, curve_ext=0.069, border_res=3, border_bevel_res=1, border_ext=0.074, border_bevel_depth=None),
    "Heavitas": dict(curve_res=6, curve_ext=0.069, border_res=5, border_bevel_res=2, border_ext=0.074, border_bevel_depth=None),
    "Kind Daily": dict(curve_res=2, curve_ext=0.069, border_res=1, border_bevel_res=1, border_ext=0.074, border_bevel_depth=0.04),
    "LEMONMILK-Bold": dict(curve_res=7, curve_ext=0.069, border_res=6, border_bevel_res=1, border_ext=0.074, border_bevel_depth=0.029),
    "Minecrafter.Alt": dict(curve_res=1, curve_ext=0.069, border_res=1, border_bevel_res=1, border_ext=0.074, border_bevel_depth=0.039),
    "OpenSans-Bold": dict(curve_res=5, curve_ext=0.069, border_res=4, border_bevel_res=1, border_ext=0.074, border_bevel_depth=0.029),
    "PackyGreat": dict(curve_res=4, curve_ext=0.069, border_res=3, border_bevel_res=1, border_ext=0.074, border_bevel_depth=0.032),
    "paladins": dict(curve_res=1, curve_ext=0.069, border_res=1, border_bevel_res=1, border_ext=0.074, border_bevel_depth=0.032),
    "Pricedown Bl": dict(curve_res=4, curve_ext=0.069, border_res=3, border_bevel_res=1, border_ext=0.074, border_bevel_depth=0.032),
    "Roboto-Regular": dict(curve_res=4, curve_ext=0.069, border_res=3, border_bevel_res=1, border_ext=0.074, border_bevel_depth=0.021),
    "Square Game": dict(curve_res=7, curve_ext=0.069, border_res=5, border_bevel_res=1, border_ext=0.074, border_bevel_depth=0.03),
    "Super Greatly": dict(curve_res=3, curve_ext=0.069, border_res=2, border_bevel_res=1, border_ext=0.074, border_bevel_depth=0.03),
    "SuperMario256": dict(curve_res=1, curve_ext=0.069, border_res=1, border_bevel_res=1, border_ext=0.074, border_bevel_depth=0.03),
    "Supersonic Rocketship": dict(curve_res=5, curve_ext=0.069, border_res=6, border_bevel_res=1, border_ext=0.074, border_bevel_depth=0.03),
    "THEBOLDFONT": dict(curve_res=4, curve_ext=0.069, border_res=3, border_bevel_res=1, border_ext=0.074, border_bevel_depth=0.03),
}

# Load font
font_file = os.path.join(os.path.dirname(__file__), FONT_MAP[font_key])
if not os.path.exists(font_file):
    raise FileNotFoundError(font_file)
font = bpy.data.fonts.load(font_file)

# Get settings for current font
s = FONT_SETTINGS[font_key]

# Main text
curve = bpy.data.curves.new(type="FONT", name="TextCurve")
curve.body = text
curve.font = font
curve.resolution_u = s["curve_res"]
curve.extrude = s["curve_ext"]
curve.bevel_depth = 0
curve.bevel_resolution = 0

main_obj = bpy.data.objects.new("MainText", curve)
bpy.context.collection.objects.link(main_obj)
main_obj.rotation_euler = (1.5708, 0, 0)

# Border text
border_curve = curve.copy()
border_curve.resolution_u = s["border_res"]
border_curve.extrude = s["border_ext"]
border_curve.bevel_resolution = s["border_bevel_res"]
if s["border_bevel_depth"] is not None:
    border_curve.bevel_depth = s["border_bevel_depth"]

border_obj = bpy.data.objects.new("BorderText", border_curve)
bpy.context.collection.objects.link(border_obj)
border_obj.rotation_euler = (1.5708, 0, 0)
border_obj.location.y += 0.035

# Convert both to mesh
for obj in (main_obj, border_obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    obj.select_set(False)

# Assign white/black materials
def assign(obj, name, color):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = False
    mat.diffuse_color = (*color, 1)
    obj.data.materials.append(mat)

assign(main_obj, "white", (1, 1, 1))
assign(border_obj, "black", (0, 0, 0))

# Export FBX
main_obj.select_set(True)
border_obj.select_set(True)
bpy.ops.export_scene.fbx(filepath=output_path, use_selection=True)
