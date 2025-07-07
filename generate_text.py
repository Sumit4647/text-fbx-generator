import bpy
import sys
import os

# Parse CLI arguments: text and output filepath
argv = sys.argv[sys.argv.index("--") + 1:]
text, output_path = argv

# Reset to a clean scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Load custom font from Font folder
font_path = os.path.join(os.path.dirname(__file__), "Font", "BurbankBigCondensed-Black.otf")
if not os.path.exists(font_path):
    raise FileNotFoundError(f"Font file not found: {font_path}")
font = bpy.data.fonts.load(font_path)

# Create text curve and style main text
curve = bpy.data.curves.new(type="FONT", name="TextCurve")
curve.body = text
curve.font = font
curve.resolution_u = 9     # Preview resolution U
curve.extrude = 0.04       # Extrude depth (m)
curve.bevel_depth = 0      # No bevel on main
curve.bevel_resolution = 0 # No bevel resolution

# Create main text object
main_obj = bpy.data.objects.new("MainText", curve)
bpy.context.collection.objects.link(main_obj)
main_obj.rotation_euler = (1.5708, 0, 0)  # 90° on X for flat text

# Duplicate curve for border text and style
border_curve = curve.copy()
border_curve.body = text
border_curve.font = font
border_curve.resolution_u = 5    # Lower resolution for border
border_curve.extrude = 0.04      # Same extrude as main
border_curve.bevel_depth = 0.024 # Bevel depth for rounded border
border_curve.bevel_resolution = 4# Bevel smoothness

border_obj = bpy.data.objects.new("BorderText", border_curve)
bpy.context.collection.objects.link(border_obj)
border_obj.rotation_euler = (1.5708, 0, 0)
border_obj.location.y -= 0.05    # Offset 0.05m on Y for layering

# Convert both to mesh
for obj in (main_obj, border_obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    obj.select_set(False)

# Create and assign materials
mat_white = bpy.data.materials.get("white") or bpy.data.materials.new("white")
mat_white.use_nodes = False
mat_white.diffuse_color = (1.0, 1.0, 1.0, 1)
main_obj.data.materials.append(mat_white)

mat_black = bpy.data.materials.get("black") or bpy.data.materials.new("black")
mat_black.use_nodes = False
mat_black.diffuse_color = (0.0, 0.0, 0.0, 1)
border_obj.data.materials.append(mat_black)

# Select both for export
main_obj.select_set(True)
border_obj.select_set(True)

# Export selected objects as FBX
bpy.ops.export_scene.fbx(filepath=output_path, use_selection=True)

print(f"✅ Exported styled text FBX to {output_path}")
