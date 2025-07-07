import bpy, sys, os

argv = sys.argv[sys.argv.index("--") + 1:]
text, fname = argv

bpy.ops.wm.read_factory_settings(use_empty=True)

# Load font from /Font/
font_path = os.path.abspath("Font/BurbankBigCondensed-Black.otf")
if not os.path.exists(font_path):
    raise FileNotFoundError("Font file not found: " + font_path)

font = bpy.data.fonts.load(font_path)

# Create 3D text
curve = bpy.data.curves.new(type="FONT", name="FT")
curve.body = text
curve.font = font

obj = bpy.data.objects.new("TextObj", curve)
bpy.context.collection.objects.link(obj)

# Rotate to lie flat (optional tweak Z/X later)
obj.rotation_euler[0] = 1.5708

# Convert to mesh
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
bpy.ops.object.convert(target="MESH")

# Export
bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.ops.export_scene.fbx(filepath=fname, use_selection=True)
