import bpy
import os
import sys
import json

# Get arguments
argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"
text = argv[0]
font_path = argv[1]
output_path = argv[2]

# Font-specific parameters
FONT_PARAMS = {
    "A4SPEED-Bold":               {"main_res": 1, "main_ext": 0.074, "border_res": 1, "border_ext": 0.04,  "border_bevel_res": 2},
    "Arial":                      {"main_res": 1, "main_ext": 0.074, "border_res": 1, "border_ext": 0.04,  "border_bevel_res": 2},
    "BebasNeue-Regular":          {"main_res": 1, "main_ext": 0.074, "border_res": 1, "border_ext": 0.04,  "border_bevel_res": 2},
    "Bold Drop":                  {"main_res": 2, "main_ext": 0.069, "border_res": 1, "border_ext": 0.074, "border_bevel_res": 1},
    "Bubblegum":                  {"main_res": 4, "main_ext": 0.069, "border_res": 4, "border_ext": 0.074, "border_bevel_res": 2},
    "BurbankBigCondensed-Black":  {"main_res": 7, "main_ext": 0.069, "border_res": 5, "border_ext": 0.074, "border_bevel_res": 1},
    "Creamy Soup":                {"main_res": 5, "main_ext": 0.069, "border_res": 3, "border_ext": 0.074, "border_bevel_res": 1},
    "Designer":                   {"main_res": 6, "main_ext": 0.069, "border_res": 3, "border_ext": 0.074, "border_bevel_res": 1},
    "Heavitas":                   {"main_res": 6, "main_ext": 0.069, "border_res": 5, "border_ext": 0.074, "border_bevel_res": 2},
    "Kind Daily":                 {"main_res": 2, "main_ext": 0.069, "border_res": 1, "border_ext": 0.074, "border_bevel_res": 1, "border_bevel_depth": 0.04},
    "LEMONMILK-Bold":             {"main_res": 7, "main_ext": 0.069, "border_res": 6, "border_ext": 0.074, "border_bevel_res": 1, "border_bevel_depth": 0.029},
    "Minecrafter.Alt":            {"main_res": 1, "main_ext": 0.069, "border_res": 1, "border_ext": 0.074, "border_bevel_res": 1, "border_bevel_depth": 0.039},
    "OpenSans-Bold":              {"main_res": 5, "main_ext": 0.069, "border_res": 4, "border_ext": 0.074, "border_bevel_res": 1, "border_bevel_depth": 0.029},
    "PackyGreat":                 {"main_res": 4, "main_ext": 0.069, "border_res": 3, "border_ext": 0.074, "border_bevel_res": 1, "border_bevel_depth": 0.032},
    "paladins":                   {"main_res": 1, "main_ext": 0.069, "border_res": 1, "border_ext": 0.074, "border_bevel_res": 1, "border_bevel_depth": 0.032},
    "Pricedown Bl":               {"main_res": 4, "main_ext": 0.069, "border_res": 3, "border_ext": 0.074, "border_bevel_res": 1, "border_bevel_depth": 0.032},
    "Roboto-Regular":             {"main_res": 4, "main_ext": 0.069, "border_res": 3, "border_ext": 0.074, "border_bevel_res": 1, "border_bevel_depth": 0.021},
    "Square Game":                {"main_res": 7, "main_ext": 0.069, "border_res": 5, "border_ext": 0.074, "border_bevel_res": 1, "border_bevel_depth": 0.03},
    "Super Greatly":              {"main_res": 3, "main_ext": 0.069, "border_res": 2, "border_ext": 0.074, "border_bevel_res": 1, "border_bevel_depth": 0.03},
    "SuperMario256":              {"main_res": 1, "main_ext": 0.069, "border_res": 1, "border_ext": 0.074, "border_bevel_res": 1, "border_bevel_depth": 0.03},
    "Supersonic Rocketship":      {"main_res": 5, "main_ext": 0.069, "border_res": 6, "border_ext": 0.074, "border_bevel_res": 1, "border_bevel_depth": 0.03},
    "THEBOLDFONT":                {"main_res": 4, "main_ext": 0.069, "border_res": 3, "border_ext": 0.074, "border_bevel_res": 1, "border_bevel_depth": 0.03}
}

# Get font name without extension
font_name = os.path.splitext(os.path.basename(font_path))[0]
params = FONT_PARAMS.get(font_name, {"main_res": 9, "main_ext": 0.04, "border_res": 5, "border_ext": 0.04, "border_bevel_res": 4})

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create text object
bpy.ops.object.text_add()
text_obj = bpy.context.active_object
text_obj.data.body = text

# Set font
font = bpy.data.fonts.load(font_path)
text_obj.data.font = font

# Apply main text parameters
text_obj.data.resolution_u = params["main_res"]
text_obj.data.extrude = params["main_ext"]

# Duplicate for border
bpy.ops.object.duplicate()
border_obj = bpy.context.active_object
border_obj.data.resolution_u = params["border_res"]
border_obj.data.extrude = params["border_ext"]
border_obj.data.bevel_resolution = params["border_bevel_res"]
border_obj.data.bevel_depth = params.get("border_bevel_depth", 0.024)

# Move slightly behind to act as outline
border_obj.location.z -= 0.001

# Export to FBX
bpy.ops.export_scene.fbx(filepath=output_path, use_selection=True)
