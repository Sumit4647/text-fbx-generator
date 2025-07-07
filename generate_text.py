import bpy
import sys
import os
import math

argv = sys.argv
text, fname = argv[argv.index("--")+1], argv[argv.index("--")+2]

bpy.ops.wm.read_factory_settings(use_empty=True)

curve = bpy.data.curves.new(type="FONT", name="TextCurve")
curve.body = text

# Try to load BurbankBigCondensed-Black if available next to this script
font_path = os.path.join(os.path.dirname(__file__), "BurbankBigCondensed-Black.otf")
if os.path.exists(font_path):
    curve.font = bpy.data.fonts.load(font_path)
obj = bpy.data.objects.new("TextObject", curve)
bpy.context.collection.objects.link(obj)

# Rotate so text stands upright along Z axis
obj.rotation_euler = (math.radians(90), 0, 0)

bpy.context.view_layer.objects.active = obj
obj.select_set(True)
bpy.ops.object.convert(target='MESH')

bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)

bpy.ops.export_scene.fbx(filepath=fname, use_selection=True)