import bpy
import sys
import os

# Parse arguments
argv = sys.argv
text = argv[argv.index("--")+1]
output_path = argv[argv.index("--")+2]

# Load custom font
font_file = "BurbankBigCondensed-Black.ttf"
font_path = os.path.join(os.path.dirname(__file__), font_file)
if os.path.exists(font_path):
    font = bpy.data.fonts.load(font_path)
else:
    raise FileNotFoundError(f"Font file not found: {font_path}")

# Reset to factory settings (empty scene)
bpy.ops.wm.read_factory_settings(use_empty=True)

# Create 3D text curve
curve = bpy.data.curves.new(type="FONT", name="TextCurve")
curve.body = text
curve.font = font  # Assign custom font

# Create object and link to scene
obj = bpy.data.objects.new("TextObject", curve)
bpy.context.collection.objects.link(obj)

# Straighten text: ensure no rotation on Z axis
obj.rotation_euler = (0.0, 0.0, 0.0)

# Make this object active and convert to mesh
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
bpy.ops.object.convert(target='MESH')

# Deselect all, select only this mesh for export
bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)

# Export selected mesh as FBX
bpy.ops.export_scene.fbx(filepath=output_path, use_selection=True)