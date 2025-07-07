import bpy
import sys
import os

# Parse CLI arguments (text and output file)
argv = sys.argv[sys.argv.index("--") + 1:]
text, output_path = argv

# Reset to a clean scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Load custom font
font_file = os.path.join(os.path.dirname(__file__), "Font", "BurbankBigCondensed-Black.otf")
if not os.path.exists(font_file):
    raise FileNotFoundError(f"Font file not found: {font_file}")
font = bpy.data.fonts.load(font_file)

# Create curve for text
curve = bpy.data.curves.new(type="FONT", name="TextCurve")
curve.body = text
curve.font = font
# Main text style
curve.resolution_u = 9
curve.extrude = 0.04
curve.bevel_depth = 0
curve.bevel_resolution = 0

# Create main text object and link
main_obj = bpy.data.objects.new("MainText", curve)
bpy.context.collection.objects.link(main_obj)
# Straighten on X axis
main_obj.rotation_euler = (1.5708, 0, 0)

# Convert main text to mesh
bpy.context.view_layer.objects.active = main_obj
main_obj.select_set(True)
bpy.ops.object.convert(target='MESH')

# Assign white material
mat_white = bpy.data.materials.get("white") or bpy.data.materials.new("white")
mat_white.use_nodes = False
mat_white.diffuse_color = (1.0, 1.0, 1.0, 1)
main_obj.data.materials.append(mat_white)

# Duplicate mesh for border
border_obj = main_obj.copy()
border_obj.data = main_obj.data.copy()
border_obj.name = "BorderText"
bpy.context.collection.objects.link(border_obj)

# Style border: offset, bevel
# (Curve bevel does not apply post-conversion, bevel already converted into mesh)
border_obj.location.y -= 0.05  # offset 0.05m on Y
# Note: bevel on mesh must be applied via modifier before conversion; skipping for simplicity

# Assign black material
mat_black = bpy.data.materials.get("black") or bpy.data.materials.new("black")
mat_black.use_nodes = False
mat_black.diffuse_color = (0.0, 0.0, 0.0, 1)
border_obj.data.materials.append(mat_black)

# Select both for export
main_obj.select_set(True)
border_obj.select_set(True)

# Export as FBX
bpy.ops.export_scene.fbx(filepath=output_path, use_selection=True)
print(f"Exported FBX: {output_path}")
