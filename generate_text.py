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

# Create text curve
curve = bpy.data.curves.new(type="FONT", name="TextCurve")
curve.body = text
curve.font = font

# Style settings for main text
curve.resolution_u = 9        # Preview resolution U
curve.extrude = 0.04          # Extrude depth (meters)
curve.bevel_depth = 0         # No bevel depth
curve.bevel_resolution = 0    # No bevel resolution

# Create main text object
main_obj = bpy.data.objects.new("MainText", curve)
bpy.context.collection.objects.link(main_obj)

# Straighten text on X axis (90°)
main_obj.rotation_euler = (1.5708, 0, 0)  # 1.5708 rad = 90° on X\ n
# Duplicate for border/backplate
border_curve = curve.copy()
border_curve.body = text
border_curve.font = font

# Style for border text
border_curve.resolution_u = 5      # Lower resolution
border_curve.extrude = 0.04        # Same extrude
border_curve.bevel_depth = 0.024   # Bevel depth for rounding
border_curve.bevel_resolution = 4   # Bevel smoothness

border_obj = bpy.data.objects.new("BorderText", border_curve)
bpy.context.collection.objects.link(border_obj)

# Match rotation and position offset for border
border_obj.rotation_euler = (1.5708, 0, 0)
border_obj.location.y -= 0.03  # Move back 0.03m on Y axis

# Convert both to mesh and export selection
for obj in [main_obj, border_obj]:
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    obj.select_set(False)

# Select meshes for FBX export
main_obj.select_set(True)
border_obj.select_set(True)

# Export as FBX
bpy.ops.export_scene.fbx(filepath=output_path, use_selection=True)
print(f"Exported 3D text FBX: {output_path}")
