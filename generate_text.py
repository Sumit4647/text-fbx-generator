import bpy
import sys
import os

# Get CLI args after --
argv = sys.argv[sys.argv.index("--") + 1:]
text, fname = argv

# Reset scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Load custom font
font_path = os.path.join(os.path.dirname(__file__), "Font", "BurbankBigCondensed-Black.otf")
font = None
if os.path.exists(font_path):
    try:
        font = bpy.data.fonts.load(font_path)
        print("✅ Font loaded")
    except Exception as e:
        print(f"⚠️ Failed to load font: {e}")
else:
    print(f"⚠️ Font file not found: {font_path}")

# Create 3D text
curve = bpy.data.curves.new(type="FONT", name="TextCurve")
curve.body = text
if font:
    curve.font = font

obj = bpy.data.objects.new("TextObj", curve)
bpy.context.collection.objects.link(obj)

# Set active, rotate, convert to mesh
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
obj.rotation_euler = (0, 0, 0)  # Align Z-axis

bpy.ops.object.convert(target="MESH")

# Export mesh as FBX
bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.ops.export_scene.fbx(filepath=fname, use_selection=True)
print(f"✅ FBX exported to {fname}")
