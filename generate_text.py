import bpy, sys

argv = sys.argv[sys.argv.index("--")+1:]
text, fname = argv

bpy.ops.wm.read_factory_settings(use_empty=True)

curve = bpy.data.curves.new(type="FONT", name="FT")
obj = bpy.data.objects.new("Text", curve)
bpy.context.collection.objects.link(obj)
obj.data.body = text

bpy.context.view_layer.objects.active = obj
bpy.ops.object.convert(target="MESH")

bpy.ops.export_scene.fbx(filepath=fname)
