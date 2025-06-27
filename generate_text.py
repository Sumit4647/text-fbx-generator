import bpy, sys

argv = sys.argv[sys.argv.index("--")+1:]
text, fname = argv

bpy.ops.wm.read_factory_settings(use_empty=True)

# Create 3D text
curve = bpy.data.curves.new(type="FONT", name="FT")
curve.body = text
obj = bpy.data.objects.new("TextObj", curve)
bpy.context.collection.objects.link(obj)

# Set object active and convert to mesh
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
bpy.ops.object.convert(target="MESH")

# Deselect all, select only the mesh
bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)

# Export selected as FBX
bpy.ops.export_scene.fbx(filepath=fname, use_selection=True)
