import bpy
import sys

argv = sys.argv
text, fname = argv[argv.index("--")+1], argv[argv.index("--")+2]

bpy.ops.wm.read_factory_settings(use_empty=True)

curve = bpy.data.curves.new(type="FONT", name="TextCurve")
curve.body = text
obj = bpy.data.objects.new("TextObject", curve)
bpy.context.collection.objects.link(obj)

bpy.context.view_layer.objects.active = obj
obj.select_set(True)
bpy.ops.object.convert(target='MESH')

bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)

bpy.ops.export_scene.fbx(filepath=fname, use_selection=True)
