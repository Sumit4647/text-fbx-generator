import bpy, sys, os

# Parse args: text, font_key, output_path
argv = sys.argv[sys.argv.index("--")+1:]
text, font_key, output_path = argv

# Reset scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Determine font file path
# Map keys to font files in your Font/ folder
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
}

font_file = os.path.join(os.path.dirname(__file__), FONT_MAP.get(font_key))
if not os.path.exists(font_file):
    raise FileNotFoundError(font_file)
font = bpy.data.fonts.load(font_file)

# Create curve & style main text
curve = bpy.data.curves.new(type="FONT", name="TextCurve")
curve.body            = text
curve.font            = font
curve.resolution_u    = 9
curve.extrude         = 0.04
curve.bevel_depth     = 0
curve.bevel_resolution= 0

main_obj = bpy.data.objects.new("MainText", curve)
bpy.context.collection.objects.link(main_obj)
main_obj.rotation_euler = (1.5708, 0, 0)

# Duplicate for border
border_curve = curve.copy()
border_curve.body            = text
border_curve.font            = font
border_curve.resolution_u    = 5
border_curve.extrude         = 0.04
border_curve.bevel_depth     = 0.024
border_curve.bevel_resolution= 4

border_obj = bpy.data.objects.new("BorderText", border_curve)
bpy.context.collection.objects.link(border_obj)
border_obj.rotation_euler = (1.5708, 0, 0)
border_obj.location.y   += 0.035

# Convert both to mesh
for obj in (main_obj, border_obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    obj.select_set(False)

# Assign white / black materials
def assign(obj, name, color):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = False
    mat.diffuse_color = (*color, 1)
    obj.data.materials.append(mat)

assign(main_obj,  "white", (1,1,1))
assign(border_obj,"black", (0,0,0))

# Export only these two
main_obj.select_set(True)
border_obj.select_set(True)
bpy.ops.export_scene.fbx(filepath=output_path, use_selection=True)

Mainly will have to changes
# Create curve & style main text
curve.resolution_u    = 9
curve.extrude         = 0.04

# Duplicate for border
border_curve.resolution_u    = 5
border_curve.bevel_resolution= 4
border_curve.extrude         = 0.04
border_curve.bevel_depth     = 0.04