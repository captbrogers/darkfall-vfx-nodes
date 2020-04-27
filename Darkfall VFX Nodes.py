bl_info = {
    "name": "Darkfall VFX Nodes",
    "author": "Darkfall",
    "version": (1, 6),
    "blender": (2, 80, 0),
    "location": "Compositor > Node Editor Toolbar > Darkfall VFX Nodes",
    "description": "Tools to help speed up your VFX Workflow for the following tasks." "VFX Eye Color Change." "VFX Scifi Eyes." "Patch Node." "Glitch Effect." "Sketch Effect." "Posterize Effect." "Ink Drop Effect",
        "category": "Nodes",
        "Blog": "http://bit.ly/2kB5XYt"
}


import bpy
import nodeitems_utils
from bpy.types import Header, Menu, Panel
from bpy.app.translations import pgettext_iface as iface_













# Create compositor planar tool
def create_planar_group(context, operator, group_name):
    
    #set render res to 100
    bpy.context.scene.render.resolution_percentage = 100
    
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree 
    
    # Create a group
    planar_group = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')
    
    # create group inputs
    group_inputs = planar_group.nodes.new('NodeGroupInput')
    group_inputs.location = (-200,0)
    planar_group.inputs.new('NodeSocketFloat','Area Of Effect Mask')
    planar_group.inputs.new('NodeSocketColor','Movie Clip')
    planar_group.inputs.new('NodeSocketColor','Image')
    planar_group.inputs.new('NodeSocketColor','Drop Shadow')
    planar_group.inputs.new('NodeSocketFloat','Mask Feather')
    planar_group.inputs.new('NodeSocketFloat','Drop Shadow Inner Feather')
    planar_group.inputs.new('NodeSocketFloat','Drop Shadow X')
    planar_group.inputs.new('NodeSocketFloat','Drop Shadow Y')
    planar_group.inputs[4].default_value = 0
    planar_group.inputs[5].default_value = 0
    planar_group.inputs[6].default_value = 0
    planar_group.inputs[7].default_value = 0
    
    
    
        # create group outputs
    group_outputs = planar_group.nodes.new('NodeGroupOutput')
    group_outputs.location = (2300,400)
    planar_group.outputs.new('NodeSocketColor','Output')
    
    
    
    #nodes to be added to group
        
    rerout1_node = planar_group.nodes.new(type= 'NodeReroute')
    rerout1_node.location = 0,150
    
    rerout2_node = planar_group.nodes.new(type= 'NodeReroute')
    rerout2_node.location = -100,150
    
        
    dil_node = planar_group.nodes.new(type= 'CompositorNodeDilateErode')
    dil_node.location = 0,500
    dil_node.label = "Drop Shadow Amount"
    dil_node.hide = False 
    dil_node.distance = -30
    
    blur1_node = planar_group.nodes.new(type= 'CompositorNodeBlur')
    blur1_node.location = -100,200
    blur1_node.size_x = 1
    blur1_node.size_y = 1
    blur1_node.inputs[1].default_value = 0
    blur1_node.filter_type = 'FAST_GAUSS'
    blur1_node.hide = True
    
    blur2_node = planar_group.nodes.new(type= 'CompositorNodeBlur')
    blur2_node.location = 0,250
    blur2_node.size_x = 1
    blur2_node.size_y = 1
    blur2_node.inputs[1].default_value = 0
    blur2_node.filter_type = 'FAST_GAUSS'
    blur2_node.hide = True
    
    blur3_node = planar_group.nodes.new(type= 'CompositorNodeBlur')
    blur3_node.location = 50,300
    blur3_node.size_x = 1
    blur3_node.size_y = 1
    blur3_node.inputs[1].default_value = 0
    blur3_node.filter_type = 'FAST_GAUSS'
    blur3_node.hide = True
    
    
    translate1_node = planar_group.nodes.new(type= 'CompositorNodeTranslate')
    translate1_node.location = 100,0
    translate1_node.hide = True
    
    mix1_node = planar_group.nodes.new(type= 'CompositorNodeMixRGB')
    mix1_node.location = 400,250
    mix1_node.hide = True
    mix1_node.blend_type = 'OVERLAY'
    mix1_node.use_alpha = True 
    
    
    math1_node = planar_group.nodes.new(type= 'CompositorNodeMath')
    math1_node.location = 300,0
    math1_node.use_clamp = True
    math1_node.operation = 'SUBTRACT'
    math1_node.hide = True 
    
    alphaover1_node = planar_group.nodes.new(type= 'CompositorNodeAlphaOver')
    math1_node.location = 500,0
    alphaover1_node.hide = True
    
    
    
    
     #link nodes together

   
    
    
    
    planar_group.links.new(rerout1_node.outputs[0], dil_node.inputs[0])
    planar_group.links.new(rerout1_node.outputs[0], blur1_node.inputs[0])
    planar_group.links.new(rerout1_node.outputs[0], blur2_node.inputs[0])
    planar_group.links.new(rerout2_node.outputs[0], blur1_node.inputs[1])
    planar_group.links.new(rerout2_node.outputs[0], blur2_node.inputs[1])
    planar_group.links.new(dil_node.outputs[0], translate1_node.inputs[0])
    planar_group.links.new(translate1_node.outputs[0], blur3_node.inputs[0])
    planar_group.links.new(blur3_node.outputs[0], math1_node.inputs[1])
    planar_group.links.new(math1_node.outputs[0], alphaover1_node.inputs[0])
    planar_group.links.new(blur2_node.outputs[0], math1_node.inputs[0])
    planar_group.links.new(blur1_node.outputs[0], mix1_node.inputs[0])
    planar_group.links.new(mix1_node.outputs[0], alphaover1_node.inputs[1])
    
    
    # link inputs
        
        
    planar_group.links.new(group_inputs.outputs['Area Of Effect Mask'], rerout1_node.inputs[0])
    planar_group.links.new(group_inputs.outputs['Movie Clip'], mix1_node.inputs[1])
    planar_group.links.new(group_inputs.outputs['Image'], mix1_node.inputs[2])
    planar_group.links.new(group_inputs.outputs['Drop Shadow'], alphaover1_node.inputs[2])
    planar_group.links.new(group_inputs.outputs['Mask Feather'], rerout2_node.inputs[0])
    planar_group.links.new(group_inputs.outputs['Drop Shadow Inner Feather'], blur3_node.inputs[1])
    planar_group.links.new(group_inputs.outputs['Drop Shadow X'], translate1_node.inputs[1])
    planar_group.links.new(group_inputs.outputs['Drop Shadow Y'], translate1_node.inputs[2])

    
    
        #link output
    planar_group.links.new(alphaover1_node.outputs[0], group_outputs.inputs['Output'])

    # return the group
    return planar_group













# Create compositor subsurface node
def create_subsurface_group(context, operator, group_name):
    
    #set render res to 100
    bpy.context.scene.render.resolution_percentage = 100
    
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree 
    
    # Create a group
    subsurface_group = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')
    
    # create group inputs
    group_inputs = subsurface_group.nodes.new('NodeGroupInput')
    group_inputs.location = (-200,0)
    subsurface_group.inputs.new('NodeSocketFloat','Area Of Effect Mask')
    subsurface_group.inputs.new('NodeSocketColor','Movie Clip')
    subsurface_group.inputs.new('NodeSocketColor','Image')
    subsurface_group.inputs.new('NodeSocketFloat','Mask Feather')
    
    
    
    
    
        # create group outputs
    group_outputs = subsurface_group.nodes.new('NodeGroupOutput')
    group_outputs.location = (2300,400)
    subsurface_group.outputs.new('NodeSocketColor','Output')
    
    
    
    #nodes to be added to group
        
    rerout1_node = subsurface_group.nodes.new(type= 'NodeReroute')
    rerout1_node.location = 0,150
    
    rerout2_node = subsurface_group.nodes.new(type= 'NodeReroute')
    rerout2_node.location = -100,150
    
        
    
    
    blur1_node = subsurface_group.nodes.new(type= 'CompositorNodeBlur')
    blur1_node.location = -100,200
    blur1_node.size_x = 1
    blur1_node.size_y = 1
    blur1_node.inputs[1].default_value = 0
    blur1_node.filter_type = 'FAST_GAUSS'
    blur1_node.hide = True
    
    
    
    
    
    translate1_node = subsurface_group.nodes.new(type= 'CompositorNodeTranslate')
    translate1_node.location = 100,0
    translate1_node.hide = True
    
    mix1_node = subsurface_group.nodes.new(type= 'CompositorNodeMixRGB')
    mix1_node.location = 400,250
    mix1_node.hide = True
    mix1_node.blend_type = 'DODGE'
    mix1_node.use_alpha = True 
    
    
    
    
    
    
    
    
    
     #link nodes together

    subsurface_group.links.new(rerout1_node.outputs[0], blur1_node.inputs[0])
    subsurface_group.links.new(rerout2_node.outputs[0], blur1_node.inputs[1])
    subsurface_group.links.new(blur1_node.outputs[0], mix1_node.inputs[0])
    
    
    # link inputs
        
        
    subsurface_group.links.new(group_inputs.outputs['Area Of Effect Mask'], rerout1_node.inputs[0])
    subsurface_group.links.new(group_inputs.outputs['Movie Clip'], mix1_node.inputs[1])
    subsurface_group.links.new(group_inputs.outputs['Image'], mix1_node.inputs[2])
    subsurface_group.links.new(group_inputs.outputs['Mask Feather'], rerout2_node.inputs[0])
    

    
    
        #link output
    subsurface_group.links.new(mix1_node.outputs[0], group_outputs.inputs['Output'])

    # return the group
    return subsurface_group

























# Create compositor group clone
def create_clone_group(context, operator, group_name):
    
    #set render res to 100
    bpy.context.scene.render.resolution_percentage = 100
    
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree 
    
    # Create a group
    clone_group = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')
    
    # create group inputs
    group_inputs = clone_group.nodes.new('NodeGroupInput')
    group_inputs.location = (-200,400)
    clone_group.inputs.new('NodeSocketFloat','Clone Mask')
    clone_group.inputs.new('NodeSocketFloat','Garbage Mask')
    clone_group.inputs.new('NodeSocketColor','Background Movie Clip')
    clone_group.inputs.new('NodeSocketFloat','Position X')
    clone_group.inputs.new('NodeSocketFloat','Position Y')
    clone_group.inputs.new('NodeSocketFloat','Rotation')
    clone_group.inputs.new('NodeSocketFloat','Scale')
    
    clone_group.inputs.new('NodeSocketFloat','Clone Feather')
    
    clone_group.inputs.new('NodeSocketFloat','Garbage Feather')
    clone_group.inputs[7].default_value = 1
    clone_group.inputs[6].default_value = 1
    
    
        # create group outputs
    group_outputs = clone_group.nodes.new('NodeGroupOutput')
    group_outputs.location = (2300,400)
    clone_group.outputs.new('NodeSocketColor','Output')
    
    
    
    #nodes to be added to group
        
    rerout1_node = clone_group.nodes.new(type= 'NodeReroute')
    rerout1_node.location = 0,150
    
    rerout2_node = clone_group.nodes.new(type= 'NodeReroute')
    rerout2_node.location = 0,100
    
    rerout3_node = clone_group.nodes.new(type= 'NodeReroute')
    rerout3_node.location = 0,200
    
    rerout4_node = clone_group.nodes.new(type= 'NodeReroute')
    rerout4_node.location = 0,0
    
    
    rerout9_node = clone_group.nodes.new(type= 'NodeReroute')
    rerout9_node.location = 0,400
    
    
    transf2_node = clone_group.nodes.new(type= 'CompositorNodeTransform')
    transf2_node.location = 200,200
    transf2_node.label = "Movie Transform2"
    transf2_node.inputs[0].name = "Movie Input"
    transf2_node.inputs[1].name = "Position X"
    transf2_node.inputs[2].name = "Position Y"
    transf2_node.inputs[3].name = "Rotation"
    transf2_node.hide = True 
    
    blur1_node = clone_group.nodes.new(type= 'CompositorNodeBlur')
    blur1_node.location = 800,500
    blur1_node.label = "Clone Mask Feather"
    blur1_node.size_x = 1
    blur1_node.size_y = 1
    blur1_node.inputs[1].name = "Patch Feather"
    blur1_node.inputs[1].default_value = 0
    blur1_node.hide = True
    
    blur2_node = clone_group.nodes.new(type= 'CompositorNodeBlur')
    blur2_node.location = 800,700
    blur2_node.label = "Garb Mask Feather"
    blur2_node.size_x = 1
    blur2_node.size_y = 1
    blur2_node.inputs[1].name = "Garb Feather"
    blur2_node.inputs[1].default_value = 0
    blur2_node.hide = True
    
    math1_node = clone_group.nodes.new(type= 'CompositorNodeMath')
    math1_node.location = 1100,600
    math1_node.label = "Garbage Math"
    math1_node.use_clamp = True
    math1_node.operation = 'SUBTRACT'
    math1_node.hide = True 
    
    mix1_node = clone_group.nodes.new(type= 'CompositorNodeMixRGB')
    mix1_node.location = 1300,0
    mix1_node.hide = True
    
    
     #link nodes together

   
    
    
    
    clone_group.links.new(blur1_node.outputs[0], math1_node.inputs[0])
    
    clone_group.links.new(blur2_node.outputs[0], math1_node.inputs[1])
        
    clone_group.links.new(math1_node.outputs[0], mix1_node.inputs[0])
    
    clone_group.links.new(rerout1_node.outputs[0], transf2_node.inputs[1])
    
    clone_group.links.new(rerout2_node.outputs[0], transf2_node.inputs[2])
    
    clone_group.links.new(rerout3_node.outputs[0], transf2_node.inputs[3])
    
    clone_group.links.new(rerout4_node.outputs[0], transf2_node.inputs[4])
    
    clone_group.links.new(rerout9_node.outputs[0], mix1_node.inputs[1])
    
    clone_group.links.new(rerout9_node.outputs[0], transf2_node.inputs[0])
    
    clone_group.links.new(transf2_node.outputs[0], mix1_node.inputs[2])

    
    
    # link inputs
    clone_group.links.new(group_inputs.outputs['Clone Mask'], blur1_node.inputs[0])
    
    clone_group.links.new(group_inputs.outputs['Garbage Mask'], blur2_node.inputs[0])
    
    clone_group.links.new(group_inputs.outputs['Background Movie Clip'], rerout9_node.inputs[0])
        
    clone_group.links.new(group_inputs.outputs['Position X'], rerout1_node.inputs[0])
    
    clone_group.links.new(group_inputs.outputs['Position Y'], rerout2_node.inputs[0])
    
    clone_group.links.new(group_inputs.outputs['Rotation'], rerout3_node.inputs[0])
    
    clone_group.links.new(group_inputs.outputs['Scale'], rerout4_node.inputs[0])
    
    clone_group.links.new(group_inputs.outputs['Clone Feather'], blur1_node.inputs[1])
    
    clone_group.links.new(group_inputs.outputs['Garbage Feather'], blur2_node.inputs[1])
    
    
        #link output
    clone_group.links.new(mix1_node.outputs[0], group_outputs.inputs['Output'])

    # return the group
    return clone_group




# Create compositor group Eye Col
def create_eyecol_group(context, operator, group_name):
    
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree 
    
    #set render res to 100
    bpy.context.scene.render.resolution_percentage = 100
    
    # Create a group
    eyecol_group = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')
    
    # Create group inputs
    

    group_inputs = eyecol_group.nodes.new('NodeGroupInput')
    group_inputs.location = (-200,400)
    
    
    group_inputs.location = (-200,400)
    eyecol_group.inputs.new('NodeSocketFloat','Eye Mask')
    eyecol_group.inputs.new('NodeSocketFloat','Eyelid Mask')
    eyecol_group.inputs.new('NodeSocketFloat','Garbage Mask')
    eyecol_group.inputs.new('NodeSocketColor','Movie Clip')
    eyecol_group.inputs.new('NodeSocketColor','Eye Color')
    eyecol_group.inputs.new('NodeSocketFloatFactor','Eye Brightness')
    eyecol_group.inputs.new('NodeSocketFloatFactor','Eyeball Brightness')
    eyecol_group.inputs.new('NodeSocketFloat','Eye Feather')
    eyecol_group.inputs.new('NodeSocketFloat','Eyelid Feather')
    eyecol_group.inputs.new('NodeSocketFloat','Garbage Feather')
    eyecol_group.inputs[5].default_value = 0
    eyecol_group.inputs[6].default_value = 0
    eyecol_group.inputs[4].default_value = (1, 1, 1, 1)
    eyecol_group.inputs[3].default_value = (1, 1, 1, 1)
    eyecol_group.inputs[1].default_value = 1
    eyecol_group.inputs[5].max_value = 1
    eyecol_group.inputs[6].max_value = 1
    eyecol_group.inputs[5].min_value = 0
    eyecol_group.inputs[6].min_value = 0
    

        
    

    # Create group outputs
    group_outputs = eyecol_group.nodes.new('NodeGroupOutput')
    group_outputs.location = (2800,400)
    eyecol_group.outputs.new('NodeSocketColor','Output')

    # Nodes inside group
    
    eyemath_node = eyecol_group.nodes.new('CompositorNodeMath')
    eyemath_node.location = 700,400
    eyemath_node.operation = 'MULTIPLY'
    eyemath_node.use_clamp = True
    eyemath_node.label = "Eye Math"
    eyemath_node.inputs[0].default_value = 1
    eyemath_node.inputs[1].default_value = 0
    eyemath_node.hide = True

    garbmath_node = eyecol_group.nodes.new('CompositorNodeMath')
    garbmath_node.location = 900,200
    garbmath_node.operation = 'SUBTRACT'
    garbmath_node.use_clamp = True
    garbmath_node.inputs[0].default_value = 1
    garbmath_node.inputs[1].default_value = 0
    garbmath_node.hide = True
    
    eyeballmath_node = eyecol_group.nodes.new('CompositorNodeMath')
    eyeballmath_node.location = 1150,700
    eyeballmath_node.operation = 'MULTIPLY'
    eyeballmath_node.use_clamp = True
    eyemath_node.inputs[0].default_value = 0
    eyemath_node.inputs[1].default_value = 1
    eyeballmath_node.hide = True
    
    
    inv_node = eyecol_group.nodes.new(type= 'CompositorNodeInvert')
    inv_node.location = 700,700
    inv_node.hide = True
    
    inv2_node = eyecol_group.nodes.new(type= 'CompositorNodeInvert')
    inv2_node.location = 1600,400
    inv2_node.hide = True
    
    inv3_node = eyecol_group.nodes.new(type= 'CompositorNodeInvert')
    inv3_node.location = 2000,200
    inv3_node.hide = True
    
    
    
       
    mix_node = eyecol_group.nodes.new(type= 'CompositorNodeMixRGB')
    mix_node.location = 1400, 200
    mix_node.blend_type = 'SOFT_LIGHT'
    mix_node.use_clamp = True
    mix_node.hide = True
    

    
    blur1_node = eyecol_group.nodes.new(type= 'CompositorNodeBlur')
    blur1_node.location = 500,700
    blur1_node.size_x = 1
    blur1_node.size_y = 1
    blur1_node.inputs[1].default_value = 0
    blur1_node.label = "Eye Mask Blur"
    blur1_node.hide = True
    
        
    
    blur2_node = eyecol_group.nodes.new(type= 'CompositorNodeBlur')
    blur2_node.location = 200,500
    blur2_node.size_x = 1
    blur2_node.size_y = 1
    blur2_node.inputs[1].default_value = 0
    blur2_node.label = "Eyelid Mask Blur"
    blur2_node.hide = True
    
    blur3_node = eyecol_group.nodes.new(type= 'CompositorNodeBlur')
    blur3_node.location = 500,200
    blur3_node.size_x = 1
    blur3_node.size_y = 1
    blur3_node.inputs[1].default_value = 0
    blur3_node.label = "Garbage Mask Blur"
    blur3_node.hide = True
    
    
        
    rgb1_node = eyecol_group.nodes.new(type= 'CompositorNodeCurveRGB')
    rgb1_node.location = 1800, 400
    rgb1_node.label = "Eyeball Brightness"
    rgb1_node.hide = True
    
    
        
    rgb2_node = eyecol_group.nodes.new(type= 'CompositorNodeCurveRGB')
    rgb2_node.location = 2200, 400
    rgb2_node.label = "Eye Color Brightness"
    rgb2_node.hide = True
    
    
    rerout1_node = eyecol_group.nodes.new(type= 'NodeReroute')
    rerout1_node.location = 400, 400
    
    
    
    #link nodes together
    
    eyecol_group.links.new(eyemath_node.outputs[0], garbmath_node.inputs[0])
    
    eyecol_group.links.new(garbmath_node.outputs[0], mix_node.inputs[0]) 
    
    eyecol_group.links.new(blur1_node.outputs[0], eyemath_node.inputs[0])
    
    eyecol_group.links.new(blur2_node.outputs[0], rerout1_node.inputs[0])   
    
    eyecol_group.links.new(rerout1_node.outputs[0], eyemath_node.inputs[1])
    
    eyecol_group.links.new(rerout1_node.outputs[0], eyeballmath_node.inputs[1])
                
            
    eyecol_group.links.new(blur3_node.outputs[0], garbmath_node.inputs[1])
    
    eyecol_group.links.new(blur1_node.outputs[0], inv_node.inputs[1])
    
    
    eyecol_group.links.new(inv_node.outputs[0], eyeballmath_node.inputs[0])
    
    eyecol_group.links.new(mix_node.outputs[0], rgb1_node.inputs[1])
    
    eyecol_group.links.new(eyeballmath_node.outputs[0], rgb1_node.inputs[0])
    
    eyecol_group.links.new(rgb1_node.outputs[0], rgb2_node.inputs[1])
    
    eyecol_group.links.new(garbmath_node.outputs[0], rgb2_node.inputs[0])
    
    eyecol_group.links.new(inv2_node.outputs[0], rgb1_node.inputs[3])
    
    eyecol_group.links.new(inv3_node.outputs[0], rgb2_node.inputs[3])
    
    
    
        
    

    # Link inputs
    eyecol_group.links.new(group_inputs.outputs['Eye Mask'], blur1_node.inputs[0])
    
    eyecol_group.links.new(group_inputs.outputs['Eyelid Mask'], blur2_node.inputs[0])
    eyecol_group.links.new(group_inputs.outputs['Garbage Mask'], blur3_node.inputs[0])
    
    eyecol_group.links.new(group_inputs.outputs['Movie Clip'], mix_node.inputs[1])
    
    eyecol_group.links.new(group_inputs.outputs['Eye Color'], mix_node.inputs[2])
    
    eyecol_group.links.new(group_inputs.outputs['Eye Brightness'], inv3_node.inputs[1])
    
    eyecol_group.links.new(group_inputs.outputs['Eyeball Brightness'], inv2_node.inputs[1])
    
    eyecol_group.links.new(group_inputs.outputs['Eye Feather'], blur1_node.inputs[1])

    
    eyecol_group.links.new(group_inputs.outputs['Garbage Feather'], blur3_node.inputs[1])
    
    eyecol_group.links.new(group_inputs.outputs['Eyelid Feather'], blur2_node.inputs[1])
    
    
    

    # link output
    eyecol_group.links.new(rgb2_node.outputs[0], group_outputs.inputs['Output'])

    # return the group
    return eyecol_group






# Create compositor group glitch
def create_glitch_group(context, operator, group_name):
    
    #set render res to 100
    bpy.context.scene.render.resolution_percentage = 100
    
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree 
    
    


    
    # Create a group
    glitch_group = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')
    
    
    # create group inputs
    group_inputs = glitch_group.nodes.new('NodeGroupInput')
    group_inputs.location = (-300,0)
    
    glitch_group.inputs.new('NodeSocketFloatFactor','Area of Effect')
    
    glitch_group.inputs.new('NodeSocketColor','Movie Clip')
    
    glitch_group.inputs.new('NodeSocketColor','Glitch Image')
    
    glitch_group.inputs.new('NodeSocketFloat','Glitch Image Offset')
    
    glitch_group.inputs.new('NodeSocketFloat','Glitch Image Size')  
    
    glitch_group.inputs.new('NodeSocketFloat','Chromatic Amount')  

    glitch_group.inputs.new('NodeSocketFloat','Glitch Movement') 

    glitch_group.inputs.new('NodeSocketFloat','Movie Clip Scale')

    glitch_group.inputs.new('NodeSocketFloat','Movie Clip Pos X')

    glitch_group.inputs.new('NodeSocketFloat','Movie Clip Pos Y')    
    
    glitch_group.inputs[0].default_value = 0
    glitch_group.inputs[0].min_value = 0
    glitch_group.inputs[0].max_value = 1
    glitch_group.inputs[4].default_value = 1
    glitch_group.inputs[7].default_value = 1
    
    
    

    
        # create group outputs
    group_outputs = glitch_group.nodes.new('NodeGroupOutput')
    group_outputs.location = (1700,0)
    glitch_group.outputs.new('NodeSocketColor','Output')
    
    
    
    #nodes to be added to group
        
    rerout1_node = glitch_group.nodes.new(type= 'NodeReroute')
    rerout1_node.location = 0,0
    
    scale1_node = glitch_group.nodes.new(type= 'CompositorNodeScale')
    scale1_node.location = 100,150
    scale1_node.label = "Scale"
    scale1_node.space = 'RENDER_SIZE'
    scale1_node.hide = True
    
    transf2_node = glitch_group.nodes.new(type= 'CompositorNodeTransform')
    transf2_node.location = 200,50
    transf2_node.label = "Glitch Size and Movement"
    transf2_node.hide = True
    
    
    
    transf3_node = glitch_group.nodes.new(type= 'CompositorNodeTransform')
    transf3_node.location = 200,-200
    transf3_node.label = "Glitch Offset"
    transf3_node.hide = True
    
    mix1_node = glitch_group.nodes.new(type= 'CompositorNodeMixRGB')
    mix1_node.location = 400,0
    mix1_node.hide = True
    mix1_node.use_clamp = True
    
    
    sep1_node = glitch_group.nodes.new(type= 'CompositorNodeSepRGBA')
    sep1_node.location = 600,0
    sep1_node.hide = True
    
    transl1_node = glitch_group.nodes.new(type= 'CompositorNodeTranslate')
    transl1_node.location = 800,200
    transl1_node.label = "Glitch Effect Amount (chromatic)"
    
    comb1_node = glitch_group.nodes.new(type= 'CompositorNodeCombRGBA')
    comb1_node.location = 1000,0
    comb1_node.hide = True
    
    transf1_node = glitch_group.nodes.new(type= 'CompositorNodeTransform')
    transf1_node.location = 1200,0
    transf1_node.hide = True
    
    mix2_node = glitch_group.nodes.new(type= 'CompositorNodeMixRGB')
    mix2_node.location = 1400,0
    mix2_node.hide = True
    mix2_node.use_clamp = True
    
    
    
    
    #link nodes together

        
    glitch_group.links.new(transf2_node.outputs[0], mix1_node.inputs[0])
    
    glitch_group.links.new(scale1_node.outputs[0], transf2_node.inputs[0])
    
    glitch_group.links.new(transf2_node.outputs[0], mix1_node.inputs[0])
    
    glitch_group.links.new(mix1_node.outputs[0], sep1_node.inputs[0])
    
    glitch_group.links.new(sep1_node.outputs[0], transl1_node.inputs[0])
    
    glitch_group.links.new(transl1_node.outputs[0], comb1_node.inputs[0])
    
    glitch_group.links.new(sep1_node.outputs[1], comb1_node.inputs[1])
    
    glitch_group.links.new(sep1_node.outputs[2], comb1_node.inputs[2])
    
    glitch_group.links.new(comb1_node.outputs[0], transf1_node.inputs[0])
    
    glitch_group.links.new(rerout1_node.outputs[0], mix1_node.inputs[1])
    
    glitch_group.links.new(rerout1_node.outputs[0], transf3_node.inputs[0])
    
    glitch_group.links.new(rerout1_node.outputs[0], mix2_node.inputs[2])
    
    glitch_group.links.new(transf3_node.outputs[0], mix1_node.inputs[2])
    
    glitch_group.links.new(transf1_node.outputs[0], mix2_node.inputs[1])
    
        # link inputs

    glitch_group.links.new(group_inputs.outputs['Area of Effect'], mix2_node.inputs[0])
    
    glitch_group.links.new(group_inputs.outputs['Movie Clip'], rerout1_node.inputs[0])
    
    glitch_group.links.new(group_inputs.outputs['Glitch Image'], scale1_node.inputs[0])
    
    glitch_group.links.new(group_inputs.outputs['Glitch Image Size'], transf2_node.inputs[4])
    
    glitch_group.links.new(group_inputs.outputs['Glitch Movement'], transf2_node.inputs[2])
    
    glitch_group.links.new(group_inputs.outputs['Chromatic Amount'], transl1_node.inputs[1])
    
    glitch_group.links.new(group_inputs.outputs['Movie Clip Scale'], transf1_node.inputs[4])
    
    glitch_group.links.new(group_inputs.outputs['Movie Clip Pos X'], transf1_node.inputs[1])
    
    glitch_group.links.new(group_inputs.outputs['Movie Clip Pos Y'], transf1_node.inputs[2])
    
    glitch_group.links.new(group_inputs.outputs['Glitch Image Offset'], transf3_node.inputs[1])
    
    
    
    
        #link output
    glitch_group.links.new(mix2_node.outputs[0], group_outputs.inputs['Output'])
    
    
    # return the group
    return glitch_group








# Operator for Gradient
class NODE_OT_texGroupGradient(bpy.types.Operator):
    bl_idname = "node.gradient_operator"
    bl_label = "Gradient Node"
    bl_description = "Click this button to add the Gradient Node"

    


    def execute(self, context):

        # ---------------------------------------------------------
        # Create the texture
        # ---------------------------------------------------------

        # Create the texture
        my_texture = bpy.data.textures.new('GradientTexture', 'IMAGE')

        # Enable use nodes
        my_texture.use_nodes = True

        # Get the tree
        tex_tree = my_texture.node_tree
        

        # Clear default nodes
        for node in tex_tree.nodes:
            tex_tree.nodes.remove(node)

        # Create Nodes
        out = tex_tree.nodes.new('TextureNodeOutput')
        out.location = (400,100)
        
        blend = tex_tree.nodes.new('TextureNodeTexBlend')
        blend.location = (0,100)
        #blend.use_flip_axis = 'VERTICAL'
        
        rot = tex_tree.nodes.new('TextureNodeRotate')
        rot.location = (200,100)
        rot.inputs[1].default_value = -0.25



        
        # Link Group to Output
        tex_tree.links.new(blend.outputs[0], rot.inputs[0])
        tex_tree.links.new(rot.outputs[0], out.inputs[0])

        # ---------------------------------------------------------
        # Compositor Action
        # ---------------------------------------------------------
        ################
        ##############
        #########
        #####
        ###
        ##
        
        
        
        # Enable use nodes in the compositor
        context.scene.use_nodes = True

        # Get the tree
        comp_tree = context.scene.node_tree

        

        # Create the texture node
        
        
        comp_node_texture = comp_tree.nodes.new('CompositorNodeTexture')
        comp_node_texture.label = "Gradient"
        comp_node_texture.use_custom_color = True
        comp_node_texture.color = (0.371155, 0.59809, 0.608)
        comp_node_texture.location = 900,0 
        comp_node_texture.width = 180
        comp_node_texture.select = False
        comp_node_texture.outputs[0].hide = True
        
        
        
          
        

        # Assign the newly created texture
        comp_node_texture.texture = my_texture
        
        


        return {'FINISHED'}
    








# Operator for Scanlines
class NODE_OT_texGroupScanlines(bpy.types.Operator):
    bl_idname = "node.scanline_operator"
    bl_label = "Scan lines Node"
    bl_description = "Click this button to add the Scan lines Generator Node"

    


    def execute(self, context):

        # ---------------------------------------------------------
        # Create the texture
        # ---------------------------------------------------------

        # Create the texture
        my_texture = bpy.data.textures.new('ScanlinesTexture', 'IMAGE')

        # Enable use nodes
        my_texture.use_nodes = True

        # Get the tree
        tex_tree = my_texture.node_tree
        

        # Clear default nodes
        for node in tex_tree.nodes:
            tex_tree.nodes.remove(node)

        # Create Nodes
        out = tex_tree.nodes.new('TextureNodeOutput')
        out.location = (2000,100)
        
        blend = tex_tree.nodes.new('TextureNodeTexBlend')
        blend.location = (0,100)
        #blend.use_flip_axis = 'VERTICAL'
        
        rot = tex_tree.nodes.new('TextureNodeRotate')
        rot.location = (200,100)
        rot.inputs[1].default_value = -0.25
        rot.hide = True
        
        math1 = tex_tree.nodes.new('TextureNodeMath')
        math1.location = (400,100)
        math1.label = "Math1 Multiply1"
        math1.operation = 'MULTIPLY'
        math1.inputs[1].default_value = 50
        math1.hide = True
        
        math2 = tex_tree.nodes.new('TextureNodeMath')
        math2.location = (400,-100)
        math2.label = "Math2 Multiply2"
        math2.operation = 'MULTIPLY'
        math2.inputs[1].default_value = 100
        math2.hide = True
        
        math3 = tex_tree.nodes.new('TextureNodeMath')
        math3.location = (400,-300)
        math3.label = "Math3 Multiply3"
        math3.operation = 'MULTIPLY'
        math3.inputs[1].default_value = 30
        math3.hide = True
        
        math4 = tex_tree.nodes.new('TextureNodeMath')
        math4.location = (600,100)
        math4.label = "Math4 Modulo1"
        math4.operation = 'MODULO'
        math4.inputs[1].default_value = 2
        math4.hide = True
        
        math5 = tex_tree.nodes.new('TextureNodeMath')
        math5.location = (600,-100)
        math5.label = "Math5 Modulo2"
        math5.operation = 'MODULO'
        math5.inputs[1].default_value = 1
        math5.hide = True
        
        math6 = tex_tree.nodes.new('TextureNodeMath')
        math6.location = (600,-300)
        math6.label = "Math6 Modulo3"
        math6.operation = 'MODULO'
        math6.inputs[1].default_value = 1
        math6.hide = True
        
        math7 = tex_tree.nodes.new('TextureNodeMath')
        math7.location = (800,100)
        math7.label = "Math7 Greater1"
        math7.operation = 'GREATER_THAN'
        math7.inputs[1].default_value = 0.5
        math7.hide = True
        
        math8 = tex_tree.nodes.new('TextureNodeMath')
        math8.location = (800,-100)
        math8.label = "Math8 Greater2"
        math8.operation = 'GREATER_THAN'
        math8.inputs[1].default_value = 0.5
        math8.hide = True
        
        math9 = tex_tree.nodes.new('TextureNodeMath')
        math9.location = (800,-300)
        math9.label = "Math9 Greater3"
        math9.operation = 'GREATER_THAN'
        math9.inputs[1].default_value = 0.5
        math9.hide = True
        
        math10 = tex_tree.nodes.new('TextureNodeMath')
        math10.location = (1000,0)
        math10.label = "Math10 Subtract1"
        math10.operation = 'SUBTRACT'
        math10.hide = True
        
        math11 = tex_tree.nodes.new('TextureNodeMath')
        math11.location = (1200,-100)
        math11.label = "Math11 Subtract2"
        math11.operation = 'SUBTRACT'
        math11.use_clamp = True
        math11.hide = True
        


        
        # Link Group to Output
        tex_tree.links.new(blend.outputs[0], rot.inputs[0])
        tex_tree.links.new(rot.outputs[0], math1.inputs[0])
        tex_tree.links.new(rot.outputs[0], math2.inputs[0])
        tex_tree.links.new(rot.outputs[0], math3.inputs[0])
        tex_tree.links.new(math1.outputs[0], math4.inputs[0])
        tex_tree.links.new(math2.outputs[0], math5.inputs[0])
        tex_tree.links.new(math3.outputs[0], math6.inputs[0])
        tex_tree.links.new(math4.outputs[0], math7.inputs[0])
        tex_tree.links.new(math5.outputs[0], math8.inputs[0])
        tex_tree.links.new(math6.outputs[0], math9.inputs[0])
        tex_tree.links.new(math7.outputs[0], math10.inputs[0])
        tex_tree.links.new(math8.outputs[0], math10.inputs[1])
        tex_tree.links.new(math9.outputs[0], math11.inputs[1])
        tex_tree.links.new(math10.outputs[0], math11.inputs[0])
        tex_tree.links.new(math11.outputs[0], out.inputs[0])

        # ---------------------------------------------------------
        # Compositor Action
        # ---------------------------------------------------------
        ################
        ##############
        #########
        #####
        ###
        ##
        
        
        
        # Enable use nodes in the compositor
        context.scene.use_nodes = True

        # Get the tree
        comp_tree = context.scene.node_tree

        

        # Create the texture node
        
        
        comp_node_texture = comp_tree.nodes.new('CompositorNodeTexture')
        comp_node_texture.label = "Scan lines"
        comp_node_texture.use_custom_color = True
        comp_node_texture.color = (0.177214, 0.177214, 0.177214)
        

        comp_node_texture.location = -50,400 
        comp_node_texture.width = 180
        comp_node_texture.select = False
        comp_node_texture.outputs[0].hide = True
        #comp_node_texture.inputs.new('NodeSocketColor', 'Color 1')
        #comp_node_texture.inputs.new('NodeSocketColor', 'Color 2')
        
        
               
        

        # Assign the newly created texture
        comp_node_texture.texture = my_texture
        
        


        return {'FINISHED'}














# Operator for Film Grain1 (col)
class NODE_OT_texGroupFilmGrain(bpy.types.Operator):
    bl_idname = "node.filmgrain1_operator"
    bl_label = "Color"
    bl_description = "Click this button to add the Film Grain Node. This Grain contains colors."

    


    def execute(self, context):

        # ---------------------------------------------------------
        # Create the texture
        # ---------------------------------------------------------

        # Create the texture
        my_texture = bpy.data.textures.new('FilmGrain1Texture', 'IMAGE')

        # Enable use nodes
        my_texture.use_nodes = True

        # Get the tree
        tex_tree = my_texture.node_tree
        

        # Clear default nodes
        for node in tex_tree.nodes:
            tex_tree.nodes.remove(node)

        # Create Nodes
        out = tex_tree.nodes.new('TextureNodeOutput')
        out.location = (800,100)
        
        noise1 = tex_tree.nodes.new('TextureNodeTexNoise')
        noise1.location = (0,100)
        noise1.inputs[0].default_value = (1, 0, 0, 1)
        
        noise2 = tex_tree.nodes.new('TextureNodeTexNoise')
        noise2.location = (0,-200)
        noise2.inputs[0].default_value = (0, 1, 0, 1)
        
        noise3 = tex_tree.nodes.new('TextureNodeTexNoise')
        noise3.location = (0,-500)
        noise3.inputs[0].default_value = (0, 0, 1, 1)
        
        mix1 = tex_tree.nodes.new('TextureNodeMixRGB')
        mix1.location = (200, 50)
        mix1.use_clamp = True
        mix1.inputs[0].default_value = 1
        mix1.blend_type = 'ADD'
        
        mix2 = tex_tree.nodes.new('TextureNodeMixRGB')
        mix2.location = (400, 0)
        mix2.use_clamp = True
        mix2.inputs[0].default_value = 1
        mix2.blend_type = 'ADD'
        
        mix3 = tex_tree.nodes.new('TextureNodeMixRGB')
        mix3.location = (600, 0)
        mix3.use_clamp = True
        mix3.inputs[0].default_value = 1
        mix3.inputs[2].default_value = (1, 1, 1, 1)
        mix3.blend_type = 'SUBTRACT'
        
        
        # Link Group to Output
        tex_tree.links.new(noise1.outputs[0], mix1.inputs[1])
        tex_tree.links.new(noise2.outputs[0], mix1.inputs[2])
        tex_tree.links.new(mix1.outputs[0], mix2.inputs[1])
        tex_tree.links.new(noise3.outputs[0], mix2.inputs[2])
        tex_tree.links.new(mix2.outputs[0], mix3.inputs[1])
        tex_tree.links.new(mix3.outputs[0], out.inputs[0])

        # ---------------------------------------------------------
        # Compositor Action
        # ---------------------------------------------------------
        ################
        ##############
        #########
        #####
        ###
        ##
        
        
        
        # Enable use nodes in the compositor
        context.scene.use_nodes = True

        # Get the tree
        comp_tree = context.scene.node_tree

        

        # Create the texture node
        
        
        comp_node_texture = comp_tree.nodes.new('CompositorNodeTexture')
        comp_node_texture.label = "Film Grain (color)"
        comp_node_texture.use_custom_color = True
        comp_node_texture.color = (0.580389, 0.516283, 0.608)
        comp_node_texture.location = -50,0 
        comp_node_texture.width = 180
        comp_node_texture.select = False
        comp_node_texture.outputs[0].hide = True
        
        
        
          
        

        # Assign the newly created texture
        comp_node_texture.texture = my_texture
        
        


        return {'FINISHED'}




# Operator for Film Grain2 (b and w)
class NODE_OT_texGroupFilmGrain2(bpy.types.Operator):
    bl_idname = "node.filmgrain2_operator"
    bl_label = "B & W"
    bl_description = "Click this button to add the Film Grain Node. This Grain is Black and White."

    


    def execute(self, context):

        # ---------------------------------------------------------
        # Create the texture
        # ---------------------------------------------------------

        # Create the texture
        my_texture = bpy.data.textures.new('FilmGrain2Texture', 'IMAGE')

        # Enable use nodes
        my_texture.use_nodes = True

        # Get the tree
        tex_tree = my_texture.node_tree
        

        # Clear default nodes
        for node in tex_tree.nodes:
            tex_tree.nodes.remove(node)

        # Create Nodes
        out = tex_tree.nodes.new('TextureNodeOutput')
        out.location = (800,100)
        
        noise1 = tex_tree.nodes.new('TextureNodeTexNoise')
        noise1.location = (0,100)
        
        
        
        # Link Group to Output
        
        tex_tree.links.new(noise1.outputs[0], out.inputs[0])

        # ---------------------------------------------------------
        # Compositor Action
        # ---------------------------------------------------------
        ################
        ##############
        #########
        #####
        ###
        ##
        
        
        
        # Enable use nodes in the compositor
        context.scene.use_nodes = True

        # Get the tree
        comp_tree = context.scene.node_tree

        

        # Create the texture node
        
        
        comp_node_texture = comp_tree.nodes.new('CompositorNodeTexture')
        comp_node_texture.label = "Film Grain (B & W)"
        comp_node_texture.use_custom_color = True
        comp_node_texture.color = (0.580389, 0.516283, 0.608)
        comp_node_texture.location = -50,-200
        comp_node_texture.width = 180
        comp_node_texture.select = False
        comp_node_texture.outputs[0].hide = True
        
        
        
          
        

        # Assign the newly created texture
        comp_node_texture.texture = my_texture
        
        


        return {'FINISHED'}







































# Create compositor group Ink Drop
def create_inkdrop_group(context, operator, group_name):
    
    #set render res to 100
    bpy.context.scene.render.resolution_percentage = 100
    
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree 
    
    # Create a group
    inkdrop_group = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')
    
    
        # create group inputs
    group_inputs = inkdrop_group.nodes.new('NodeGroupInput')
    group_inputs.location = (-200,0)
    
    inkdrop_group.inputs.new('NodeSocketColor','Smoke Movie Clip')
    
    inkdrop_group.inputs.new('NodeSocketColor','Black and White Text Image')
    
    # create group outputs
    group_outputs = inkdrop_group.nodes.new('NodeGroupOutput')
    group_outputs.location = (2000,0)
    inkdrop_group.outputs.new('NodeSocketColor','Output')
    
    
    
        #nodes to be added to group
        
    rgb_node = inkdrop_group.nodes.new(type= 'CompositorNodeCurveRGB')
    rgb_node.location = 600,150
    
            
    mix_node = inkdrop_group.nodes.new(type= 'CompositorNodeMixRGB')
    mix_node.location = 400,150
    mix_node.hide = True
    
    rgbtobw_node = inkdrop_group.nodes.new(type= 'CompositorNodeRGBToBW')
    rgbtobw_node.location = 250,160
    rgbtobw_node.hide = True
    
    inv_node = inkdrop_group.nodes.new(type= 'CompositorNodeInvert')
    inv_node.location = 200,0
    inv_node.hide = True
    
    
    #link nodes together
         
    inkdrop_group.links.new(rgbtobw_node.outputs[0], mix_node.inputs[0])
    
    inkdrop_group.links.new(inv_node.outputs[0], mix_node.inputs[1])
    
    inkdrop_group.links.new(mix_node.outputs[0], rgb_node.inputs[1])
    
    # link inputs
    
    inkdrop_group.links.new(group_inputs.outputs['Smoke Movie Clip'], rgbtobw_node.inputs[0])
    
    inkdrop_group.links.new(group_inputs.outputs['Black and White Text Image'], inv_node.inputs[0])
    
    
        #link output
    inkdrop_group.links.new(rgb_node.outputs[0], group_outputs.inputs['Output'])

    # return the group
    return inkdrop_group


# Create compositor group Patch 
def create_patch_group(context, operator, group_name):
    
    #set render res to 100
    bpy.context.scene.render.resolution_percentage = 100
    
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree 
    
    
    
    # Create a group
    patch_group = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')
    
    # Create group inputs
    

    group_inputs = patch_group.nodes.new('NodeGroupInput')
    group_inputs.location = (-200,400)
    
    
    # create group inputs
    group_inputs = patch_group.nodes.new('NodeGroupInput')
    group_inputs.location = (-200,400)
    patch_group.inputs.new('NodeSocketFloat','Patch Mask')
    patch_group.inputs.new('NodeSocketFloat','Garbage Mask')
    patch_group.inputs.new('NodeSocketColor','Background Movie Clip')
    patch_group.inputs.new('NodeSocketColor','Patch Movie Clip')
    patch_group.inputs.new('NodeSocketFloat','Position X')
    patch_group.inputs.new('NodeSocketFloat','Position Y')
    patch_group.inputs.new('NodeSocketFloat','Rotation')
    patch_group.inputs.new('NodeSocketFloat','Scale')
    patch_group.inputs.new('NodeSocketFloat','Perspective X')
    patch_group.inputs.new('NodeSocketFloat','Perspective Y')
    
    patch_group.inputs.new('NodeSocketFloat','Patch Feather')
    
    patch_group.inputs.new('NodeSocketFloat','Garbage Feather')
    
    patch_group.inputs.new('NodeSocketFloat','Track Pos Input X')
    patch_group.inputs.new('NodeSocketFloat','Track Pos Input Y')
    patch_group.inputs[7].default_value = 1
    patch_group.inputs[8].default_value = 1
    patch_group.inputs[9].default_value = 1
    patch_group.inputs[1].default_value = 1
    patch_group.inputs[1].default_value = 0    
    
    
    
    # Create group outputs
    group_outputs = patch_group.nodes.new('NodeGroupOutput')
    group_outputs.location = (2800,400)
    patch_group.outputs.new('NodeSocketColor','Output')

    #nodes to be added to group
        
    rerout1_node = patch_group.nodes.new(type= 'NodeReroute')
    rerout1_node.location = 0,0
    
    rerout2_node = patch_group.nodes.new(type= 'NodeReroute')
    rerout2_node.location = 0,100
    
    rerout3_node = patch_group.nodes.new(type= 'NodeReroute')
    rerout3_node.location = 0,200
    
    rerout4_node = patch_group.nodes.new(type= 'NodeReroute')
    rerout4_node.location = 0,300
    
    rerout5_node = patch_group.nodes.new(type= 'NodeReroute')
    rerout5_node.location = 0,400
    
    rerout6_node = patch_group.nodes.new(type= 'NodeReroute')
    rerout6_node.location = 0,500
    
    rerout7_node = patch_group.nodes.new(type= 'NodeReroute')
    rerout7_node.location = 0,700
    
    rerout8_node = patch_group.nodes.new(type= 'NodeReroute')
    rerout8_node.location = 0,800
    

    
    transf1_node = patch_group.nodes.new(type= 'CompositorNodeTransform')
    transf1_node.location = 200,500
    transf1_node.label = "Patch Mask Transform"
    transf1_node.inputs[0].name = "Mask Input"
    transf1_node.inputs[1].name = "Position X"
    transf1_node.inputs[2].name = "Position Y"
    transf1_node.inputs[3].name = "Rotation"
    transf1_node.hide = True 
    
    
    transf2_node = patch_group.nodes.new(type= 'CompositorNodeTransform')
    transf2_node.location = 200,200
    transf2_node.label = "Patch Movie Transform"
    transf2_node.inputs[0].name = "Mask Input"
    transf2_node.inputs[1].name = "Position X"
    transf2_node.inputs[2].name = "Position Y"
    transf2_node.inputs[3].name = "Rotation"
    transf2_node.hide = True 
    
    scale1_node = patch_group.nodes.new(type= 'CompositorNodeScale')
    scale1_node.location = 400,500
    scale1_node.label = "Mask Perspective Scale"
    scale1_node.hide = True 
    
    scale2_node = patch_group.nodes.new(type= 'CompositorNodeScale')
    scale2_node.location = 400,200
    scale2_node.label = "Movie Perspective Scale"
    scale2_node.hide = True 
    
    
    transl1_node = patch_group.nodes.new(type= 'CompositorNodeTranslate')
    transl1_node.location = 600,500
    transl1_node.label = "Patch Mask Track Input"
    transl1_node.hide = True 
    
    transl2_node = patch_group.nodes.new(type= 'CompositorNodeTranslate')
    transl2_node.location = 600,200
    transl2_node.label = "Patch Movie Track Input"
    transl2_node.hide = True 
    
    blur1_node = patch_group.nodes.new(type= 'CompositorNodeBlur')
    blur1_node.location = 800,500
    blur1_node.label = "Patch Mask Feather"
    blur1_node.size_x = 1
    blur1_node.size_y = 1
    blur1_node.inputs[1].name = "Patch Feather"
    blur1_node.inputs[1].default_value = 0
    blur1_node.hide = True
    
    blur2_node = patch_group.nodes.new(type= 'CompositorNodeBlur')
    blur2_node.location = 800,700
    blur2_node.label = "Garb Mask Feather"
    blur2_node.size_x = 1
    blur2_node.size_y = 1
    blur2_node.inputs[1].name = "Garb Feather"
    blur2_node.inputs[1].default_value = 0
    blur2_node.hide = True
    
    math1_node = patch_group.nodes.new(type= 'CompositorNodeMath')
    math1_node.location = 1100,600
    math1_node.label = "Garbage Math"
    math1_node.use_clamp = True
    math1_node.operation = 'SUBTRACT'
    math1_node.hide = True 
    
    mix1_node = patch_group.nodes.new(type= 'CompositorNodeMixRGB')
    mix1_node.location = 1300,0
    mix1_node.hide = True
    
    
     #link nodes together

    patch_group.links.new(transf1_node.outputs[0], scale1_node.inputs[0])
    
    patch_group.links.new(scale1_node.outputs[0], transl1_node.inputs[0])
    
    patch_group.links.new(transl1_node.outputs[0], blur1_node.inputs[0])
    
    patch_group.links.new(transf2_node.outputs[0], scale2_node.inputs[0])
    
    patch_group.links.new(scale2_node.outputs[0], transl2_node.inputs[0])
    
    patch_group.links.new(transl2_node.outputs[0], mix1_node.inputs[2])
    
    patch_group.links.new(blur1_node.outputs[0], math1_node.inputs[0])
    
    patch_group.links.new(blur2_node.outputs[0], math1_node.inputs[1])
        
    patch_group.links.new(math1_node.outputs[0], mix1_node.inputs[0])
    
    patch_group.links.new(rerout1_node.outputs[0], transf1_node.inputs[1])
    
    patch_group.links.new(rerout1_node.outputs[0], transf2_node.inputs[1])
    
    patch_group.links.new(rerout2_node.outputs[0], transf1_node.inputs[2])
    
    patch_group.links.new(rerout2_node.outputs[0], transf2_node.inputs[2])
    
    patch_group.links.new(rerout3_node.outputs[0], transf1_node.inputs[3])
    
    patch_group.links.new(rerout3_node.outputs[0], transf2_node.inputs[3])
    
    patch_group.links.new(rerout4_node.outputs[0], transf1_node.inputs[4])
    
    patch_group.links.new(rerout4_node.outputs[0], transf2_node.inputs[4])
    
    patch_group.links.new(rerout5_node.outputs[0], scale1_node.inputs[1])
    
    patch_group.links.new(rerout5_node.outputs[0], scale2_node.inputs[1])
    
    patch_group.links.new(rerout6_node.outputs[0], scale1_node.inputs[2])
    
    patch_group.links.new(rerout6_node.outputs[0], scale2_node.inputs[2])
    
    patch_group.links.new(rerout7_node.outputs[0], transl1_node.inputs[1])
    
    patch_group.links.new(rerout7_node.outputs[0], transl2_node.inputs[1])
    
    patch_group.links.new(rerout8_node.outputs[0], transl1_node.inputs[2])
    
    patch_group.links.new(rerout8_node.outputs[0], transl2_node.inputs[2])

    
    
    # link inputs
    patch_group.links.new(group_inputs.outputs['Patch Mask'], transf1_node.inputs[0])
    
    patch_group.links.new(group_inputs.outputs['Garbage Mask'], blur2_node.inputs[0])
    
    patch_group.links.new(group_inputs.outputs['Background Movie Clip'], mix1_node.inputs[1])
    
    patch_group.links.new(group_inputs.outputs['Patch Movie Clip'], transf2_node.inputs[0])
    
    patch_group.links.new(group_inputs.outputs['Position X'], rerout1_node.inputs[0])
    
    patch_group.links.new(group_inputs.outputs['Position Y'], rerout2_node.inputs[0])
    
    patch_group.links.new(group_inputs.outputs['Rotation'], rerout3_node.inputs[0])
    
    patch_group.links.new(group_inputs.outputs['Scale'], rerout4_node.inputs[0])
    
    patch_group.links.new(group_inputs.outputs['Perspective X'], rerout5_node.inputs[0])
    
    patch_group.links.new(group_inputs.outputs['Perspective Y'], rerout6_node.inputs[0])
    
    patch_group.links.new(group_inputs.outputs['Track Pos Input X'], rerout7_node.inputs[0])
    
    patch_group.links.new(group_inputs.outputs['Track Pos Input Y'], rerout8_node.inputs[0])
    
    patch_group.links.new(group_inputs.outputs['Patch Feather'], blur1_node.inputs[1])
    
    patch_group.links.new(group_inputs.outputs['Garbage Feather'], blur2_node.inputs[1])
    
    
        #link output
    patch_group.links.new(mix1_node.outputs[0], group_outputs.inputs['Output'])

    # return the group
    return patch_group






# Create compositor group Marker Removal 
def create_markerrem_group(context, operator, group_name):
    
    #set render res to 100
    bpy.context.scene.render.resolution_percentage = 100
    
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree 
    
    
    
    # Create a group
    markerrem_group = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')
    
    # Create group inputs
    

    group_inputs = markerrem_group.nodes.new('NodeGroupInput')
    group_inputs.location = (-200,400)
    
    
    # create group inputs
    group_inputs = markerrem_group.nodes.new('NodeGroupInput')
    group_inputs.location = (-200,400)
    markerrem_group.inputs.new('NodeSocketFloat','Marker Removal Mask')
    markerrem_group.inputs.new('NodeSocketColor','Movie Clip')
    markerrem_group.inputs.new('NodeSocketFloat','Position X')
    markerrem_group.inputs.new('NodeSocketFloat','Position Y')
    markerrem_group.inputs.new('NodeSocketFloat','Marker Feather')
    markerrem_group.inputs.new('NodeSocketFloat','Brightness')
    markerrem_group.inputs.new('NodeSocketFloat','Saturation')
    
    markerrem_group.inputs[2].default_value = 0
    markerrem_group.inputs[3].default_value = 0
    markerrem_group.inputs[4].default_value = 0 
    markerrem_group.inputs[5].default_value = 1 
    markerrem_group.inputs[6].default_value = 1  
    
    
    
    # Create group outputs
    group_outputs = markerrem_group.nodes.new('NodeGroupOutput')
    group_outputs.location = (2800,400)
    markerrem_group.outputs.new('NodeSocketColor','Output')

    #nodes to be added to group
        
    rerout1_node = markerrem_group.nodes.new(type= 'NodeReroute')
    rerout1_node.location = 0,0
    
    
    
    blur1_node = markerrem_group.nodes.new(type= 'CompositorNodeBlur')
    blur1_node.location = 200,500
    blur1_node.label = "Marker Mask Feather"
    blur1_node.size_x = 1
    blur1_node.size_y = 1
    blur1_node.inputs[1].name = "Marker Mask"
    blur1_node.inputs[1].default_value = 0
    blur1_node.hide = True
    
    hue_node = markerrem_group.nodes.new(type= 'CompositorNodeHueSat')
    hue_node.location = 200,0
    hue_node.hide = True 
    
    trans_node = markerrem_group.nodes.new(type= 'CompositorNodeTranslate')
    trans_node.location = 400,500
    trans_node.label = "Marker Mask Translate"
    trans_node.inputs[0].name = "Marker Mask Input"
    trans_node.inputs[1].name = "Position X"
    trans_node.inputs[2].name = "Position Y"
    trans_node.hide = True 
    
    mix1_node = markerrem_group.nodes.new(type= 'CompositorNodeMixRGB')
    mix1_node.location = 600,0
    mix1_node.hide = True
    
    
    
    
    
     #link nodes together
     
    markerrem_group.links.new(rerout1_node.outputs[0], mix1_node.inputs[1])
    markerrem_group.links.new(rerout1_node.outputs[0], hue_node.inputs[0])
    markerrem_group.links.new(blur1_node.outputs[0], mix1_node.inputs[0])
    markerrem_group.links.new(hue_node.outputs[0], trans_node.inputs[0])
    markerrem_group.links.new(trans_node.outputs[0], mix1_node.inputs[2])

    
    
    # link inputs
    markerrem_group.links.new(group_inputs.outputs['Marker Removal Mask'], blur1_node.inputs[0])
    
    
    markerrem_group.links.new(group_inputs.outputs['Movie Clip'], rerout1_node.inputs[0])
    
    markerrem_group.links.new(group_inputs.outputs['Position X'], trans_node.inputs[1])
    
    markerrem_group.links.new(group_inputs.outputs['Position Y'], trans_node.inputs[2])
    
    
    markerrem_group.links.new(group_inputs.outputs['Marker Feather'], blur1_node.inputs[1])
    
    markerrem_group.links.new(group_inputs.outputs['Brightness'], hue_node.inputs[3])
    
    markerrem_group.links.new(group_inputs.outputs['Saturation'], hue_node.inputs[2])
    
    
    
    
        #link output
    markerrem_group.links.new(mix1_node.outputs[0], group_outputs.inputs['Output'])

    # return the group
    return markerrem_group








# Create compositor group Transition Node 
def create_transition_group(context, operator, group_name):
    
    
    
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree 
    
    
    
    # Create a group
    transition_group = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')
    
    
    
    # create group inputs
    group_inputs = transition_group.nodes.new('NodeGroupInput')
    group_inputs.location = (-200,400)
    
    transition_group.inputs.new('NodeSocketFloatFactor','Transition Factor')
    transition_group.inputs.new('NodeSocketColor','Original Video Clip')
    transition_group.inputs.new('NodeSocketColor','Edited Video Clip')
    
    
    
    transition_group.inputs[0].default_value = 0
    transition_group.inputs[0].min_value = 0
    transition_group.inputs[0].max_value = 1
    
    
    
    
    # Create group outputs
    group_outputs = transition_group.nodes.new('NodeGroupOutput')
    group_outputs.location = (600,400)
    transition_group.outputs.new('NodeSocketColor','Output')

    #nodes to be added to group
        
    mix1_node = transition_group.nodes.new(type= 'CompositorNodeMixRGB')
    mix1_node.location = 200,400
    mix1_node.use_clamp = True
    
    
    
    # link inputs
    transition_group.links.new(group_inputs.outputs['Transition Factor'], mix1_node.inputs[0])
    
    
    transition_group.links.new(group_inputs.outputs['Edited Video Clip'], mix1_node.inputs[1])
    
    transition_group.links.new(group_inputs.outputs['Original Video Clip'], mix1_node.inputs[2])
    
    
    
    
    
    
        #link output
    transition_group.links.new(mix1_node.outputs[0], group_outputs.inputs['Output'])

    # return the group
    return transition_group










# Create compositor group posterize 1
def create_post1_group(context, operator, group_name):
    
    #set render res to 100
    bpy.context.scene.render.resolution_percentage = 100
    
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree 
    
    # Create a group
    post1_group = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')
    
    # create group inputs
    group_inputs = post1_group.nodes.new('NodeGroupInput')
    group_inputs.location = (-200,0)
    
    post1_group.inputs.new('NodeSocketColor','Movie Clip')
    post1_group.inputs.new('NodeSocketFloat','Value 1')
    post1_group.inputs.new('NodeSocketFloat','Value 2')
    post1_group.inputs.new('NodeSocketFloat','Value 3')
    post1_group.inputs[1].default_value = 9.1
    post1_group.inputs[2].default_value = 1.3
    post1_group.inputs[3].default_value = 9
    
    # create group outputs
    group_outputs = post1_group.nodes.new('NodeGroupOutput')
    group_outputs.location = (2000,0)
    post1_group.outputs.new('NodeSocketColor','Output')
    
        #nodes to be added to group
        
    rerout1_node = post1_group.nodes.new(type= 'NodeReroute')
    rerout1_node.location = 0,0
    
    math1_node = post1_group.nodes.new(type= 'CompositorNodeMath')
    math1_node.location = 200,0
    math1_node.operation = 'MULTIPLY'
    math1_node.inputs[1].default_value = 5
    
    math2_node = post1_group.nodes.new(type= 'CompositorNodeMath')
    math2_node.location = 400,0
    math2_node.operation = 'SUBTRACT'
    math2_node.inputs[1].default_value = 0.1
    
    math3_node = post1_group.nodes.new(type= 'CompositorNodeMath')
    math3_node.location = 600,0
    math3_node.operation = 'ROUND'
    math3_node.inputs[1].default_value = 0
    
    math4_node = post1_group.nodes.new(type= 'CompositorNodeMath')
    math4_node.location = 800,0
    math4_node.operation = 'DIVIDE'
    math4_node.inputs[1].default_value = 2
    
    mix_node = post1_group.nodes.new(type= 'CompositorNodeMixRGB')
    mix_node.location = 1000,0
    mix_node.blend_type = 'SOFT_LIGHT'
    
    
        #link nodes together
     
    post1_group.links.new(rerout1_node.outputs[0], math1_node.inputs[0])
    
    post1_group.links.new(rerout1_node.outputs[0], mix_node.inputs[2])
    
    post1_group.links.new(math1_node.outputs[0], math2_node.inputs[0]) 
    
    post1_group.links.new(math2_node.outputs[0], math3_node.inputs[0]) 
    
    post1_group.links.new(math3_node.outputs[0], math4_node.inputs[0]) 
    
    post1_group.links.new(math4_node.outputs[0], mix_node.inputs[1])
    
    # link inputs
    
    post1_group.links.new(group_inputs.outputs['Movie Clip'], rerout1_node.inputs[0])
    post1_group.links.new(group_inputs.outputs['Value 1'], math1_node.inputs[1])
    post1_group.links.new(group_inputs.outputs['Value 2'], math2_node.inputs[1])
    post1_group.links.new(group_inputs.outputs['Value 3'], math4_node.inputs[1])
    
    #link output
    post1_group.links.new(mix_node.outputs[0], group_outputs.inputs['Output'])

    # return the group
    return post1_group




# Create compositor group posterize 2
def create_post2_group(context, operator, group_name):
    
    #set render res to 100
    bpy.context.scene.render.resolution_percentage = 100
    
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree 
    
    # Create a group
    post2_group = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')
    
     # create group inputs
    group_inputs = post2_group.nodes.new('NodeGroupInput')
    group_inputs.location = (-200,0)
    
    post2_group.inputs.new('NodeSocketColor','Movie Clip')
    post2_group.inputs.new('NodeSocketFloat','Value 1')
    post2_group.inputs.new('NodeSocketFloat','Value 2')
    post2_group.inputs.new('NodeSocketFloat','Value 3')
    post2_group.inputs[1].default_value = 15
    post2_group.inputs[2].default_value = 0.2
    post2_group.inputs[3].default_value = 9
    
    # create group outputs
    group_outputs = post2_group.nodes.new('NodeGroupOutput')
    group_outputs.location = (2000,0)
    post2_group.outputs.new('NodeSocketColor','Output')
    
        #nodes to be added to group
        
    rerout1_node = post2_group.nodes.new(type= 'NodeReroute')
    rerout1_node.location = 0,0
    
    math1_node = post2_group.nodes.new(type= 'CompositorNodeMath')
    math1_node.location = 200,0
    math1_node.operation = 'MULTIPLY'
    math1_node.inputs[1].default_value = 10
    
    math2_node = post2_group.nodes.new(type= 'CompositorNodeMath')
    math2_node.location = 400,0
    math2_node.operation = 'SUBTRACT'
    math2_node.inputs[1].default_value = 0
    
    math3_node = post2_group.nodes.new(type= 'CompositorNodeMath')
    math3_node.location = 600,0
    math3_node.operation = 'ROUND'
    math3_node.inputs[1].default_value = 0
    
    math4_node = post2_group.nodes.new(type= 'CompositorNodeMath')
    math4_node.location = 800,0
    math4_node.operation = 'DIVIDE'
    math4_node.inputs[1].default_value = 9
    
    mix_node = post2_group.nodes.new(type= 'CompositorNodeMixRGB')
    mix_node.location = 1000,0
    mix_node.blend_type = 'ADD'
    
    
        #link nodes together
     
    post2_group.links.new(rerout1_node.outputs[0], math1_node.inputs[0])
    
    post2_group.links.new(rerout1_node.outputs[0], mix_node.inputs[2])
    
    post2_group.links.new(math1_node.outputs[0], math2_node.inputs[0]) 
    
    post2_group.links.new(math2_node.outputs[0], math3_node.inputs[0]) 
    
    post2_group.links.new(math3_node.outputs[0], math4_node.inputs[0]) 
    
    post2_group.links.new(math4_node.outputs[0], mix_node.inputs[1])
    
    # link inputs
    
    post2_group.links.new(group_inputs.outputs['Movie Clip'], rerout1_node.inputs[0])
    post2_group.links.new(group_inputs.outputs['Value 1'], math1_node.inputs[1])
    post2_group.links.new(group_inputs.outputs['Value 2'], math2_node.inputs[1])
    post2_group.links.new(group_inputs.outputs['Value 3'], math4_node.inputs[1])
    
    #link output
    post2_group.links.new(mix_node.outputs[0], group_outputs.inputs['Output'])

    # return the group
    return post2_group




    








# Create compositor group posterize 3
def create_post3_group(context, operator, group_name):
    
    #set render res to 100
    bpy.context.scene.render.resolution_percentage = 100
    
    # Create a group
    post3_group = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')
    
     # create group inputs
    group_inputs = post3_group.nodes.new('NodeGroupInput')
    group_inputs.location = (-200,0)
    
    post3_group.inputs.new('NodeSocketColor','Movie Clip')
    post3_group.inputs.new('NodeSocketFloat','Value 1')
    post3_group.inputs.new('NodeSocketFloat','Value 2')
    post3_group.inputs.new('NodeSocketFloat','Value 3')
    post3_group.inputs[1].default_value = 6
    post3_group.inputs[2].default_value = 0.5
    post3_group.inputs[3].default_value = 5
    
    # create group outputs
    group_outputs = post3_group.nodes.new('NodeGroupOutput')
    group_outputs.location = (2000,0)
    post3_group.outputs.new('NodeSocketColor','Output')
    
        #nodes to be added to group
        
    rerout1_node = post3_group.nodes.new(type= 'NodeReroute')
    rerout1_node.location = 0,0
    
    math1_node = post3_group.nodes.new(type= 'CompositorNodeMath')
    math1_node.location = 200,0
    math1_node.operation = 'MULTIPLY'
    math1_node.inputs[1].default_value = 6
    
    math2_node = post3_group.nodes.new(type= 'CompositorNodeMath')
    math2_node.location = 400,0
    math2_node.operation = 'SUBTRACT'
    math2_node.inputs[1].default_value = 0.5
    
    math3_node = post3_group.nodes.new(type= 'CompositorNodeMath')
    math3_node.location = 600,0
    math3_node.operation = 'ROUND'
    math3_node.inputs[1].default_value = 0
    
    math4_node = post3_group.nodes.new(type= 'CompositorNodeMath')
    math4_node.location = 800,0
    math4_node.operation = 'DIVIDE'
    math4_node.inputs[1].default_value = 5
    
    mix_node = post3_group.nodes.new(type= 'CompositorNodeMixRGB')
    mix_node.location = 1000,0
    mix_node.blend_type = 'COLOR'
    
       
    
        #link nodes together
     
    post3_group.links.new(rerout1_node.outputs[0], math1_node.inputs[0])
    
    post3_group.links.new(rerout1_node.outputs[0], mix_node.inputs[2])
    
    post3_group.links.new(math1_node.outputs[0], math2_node.inputs[0]) 
    
    post3_group.links.new(math2_node.outputs[0], math3_node.inputs[0]) 
    
    post3_group.links.new(math3_node.outputs[0], math4_node.inputs[0]) 
    
    post3_group.links.new(math4_node.outputs[0], mix_node.inputs[1])
    
        # link inputs
    
    post3_group.links.new(group_inputs.outputs['Movie Clip'], rerout1_node.inputs[0])
    post3_group.links.new(group_inputs.outputs['Value 1'], math1_node.inputs[1])
    post3_group.links.new(group_inputs.outputs['Value 2'], math2_node.inputs[1])
    post3_group.links.new(group_inputs.outputs['Value 3'], math4_node.inputs[1])
    
        #link output
    post3_group.links.new(mix_node.outputs[0], group_outputs.inputs['Output'])

    # return the group
    return post3_group


# Create compositor group Scifi Eyes
def create_scifieye_group(context, operator, group_name):
    
    #set render res to 100
    bpy.context.scene.render.resolution_percentage = 100  
    
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree 
    
    
    
    
    
    
    # Create a group
    scifieye_group = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')

    # Create group inputs
    group_inputs = scifieye_group.nodes.new('NodeGroupInput')
    group_inputs.location = (-500,400)
    scifieye_group.inputs.new('NodeSocketFloat','Eye Lid Mask')
    scifieye_group.inputs.new('NodeSocketFloat','Shadow Mask')
    scifieye_group.inputs.new('NodeSocketColor','Movie Clip')
    scifieye_group.inputs.new('NodeSocketColor','Eye Image')
    scifieye_group.inputs.new('NodeSocketFloat','Left Eye: X')
    scifieye_group.inputs.new('NodeSocketFloat','Left Eye: Y')
    scifieye_group.inputs.new('NodeSocketFloatAngle','Left Eye: Rotation')
    scifieye_group.inputs.new('NodeSocketFloat','Left Eye: Scale')
    scifieye_group.inputs.new('NodeSocketFloat','Right Eye: X')
    scifieye_group.inputs.new('NodeSocketFloat','Right Eye: Y')
    scifieye_group.inputs.new('NodeSocketFloatAngle','Right Eye: Rotation')
    scifieye_group.inputs.new('NodeSocketFloat','Right Eye: Scale')
    scifieye_group.inputs.new('NodeSocketFloatFactor','Eyeball Brightness')
    scifieye_group.inputs.new('NodeSocketFloat','Eye Mask Feather')
    scifieye_group.inputs.new('NodeSocketFloat','Shadow Feather')
    scifieye_group.inputs.new('NodeSocketFloat','Left Eye (Track Pos X)')
    scifieye_group.inputs.new('NodeSocketFloat','Left Eye (Track Pos Y)')
    scifieye_group.inputs.new('NodeSocketFloat','Right Eye (Track Pos X)')
    scifieye_group.inputs.new('NodeSocketFloat','Right Eye (Track Pos Y)')
    scifieye_group.inputs[7].default_value = 0.5
    scifieye_group.inputs[11].default_value = 0.5
    scifieye_group.inputs[8].default_value = 550
    scifieye_group.inputs[0].default_value = 1
    scifieye_group.inputs[12].max_value = 1
    scifieye_group.inputs[12].min_value = 0
    scifieye_group.inputs[12].default_value = 0
    
    
        

    # Create group outputs
    group_outputs = scifieye_group.nodes.new('NodeGroupOutput')
    group_outputs.location = (2000,400)
    scifieye_group.outputs.new('NodeSocketColor','Output')
    
    
    

    #nodes to be added to group
        
    rerout1_node = scifieye_group.nodes.new(type= 'NodeReroute')
    rerout1_node.location = 0,0
    
    rerout2_node = scifieye_group.nodes.new(type= 'NodeReroute')
    rerout2_node.location = 50,300
    
    rerout3_node = scifieye_group.nodes.new(type= 'NodeReroute')
    rerout3_node.location = 50,500
    
    
    transf1_node = scifieye_group.nodes.new(type= 'CompositorNodeTransform')
    transf1_node.location = 180,150
    transf1_node.inputs[4].default_value = 0.5
    transf1_node.label = "Left Eye Position"
    transf1_node.hide = True
    
    blur1_node = scifieye_group.nodes.new(type= 'CompositorNodeBlur')
    blur1_node.location = -200,150
    blur1_node.size_x = 1
    blur1_node.size_y = 1
    blur1_node.inputs[1].default_value = 0
    blur1_node.label = "Eye M F"
    blur1_node.hide = True
    
    rgb1_node = scifieye_group.nodes.new(type= 'CompositorNodeCurveRGB')
    rgb1_node.location = 180,400
    rgb1_node.label = "Eye Ball Brightness"
    rgb1_node.hide = True
    
    inv1_node = scifieye_group.nodes.new(type= 'CompositorNodeInvert')
    inv1_node.location = 80,400
    inv1_node.hide = True
    
    transf2_node = scifieye_group.nodes.new(type= 'CompositorNodeTransform')
    transf2_node.location = 100,-50
    transf2_node.inputs[4].default_value = 0.5
    transf2_node.label = "Right Eye Position"
    transf2_node.hide = True
    
    translate1_node = scifieye_group.nodes.new(type= 'CompositorNodeTranslate')
    translate1_node.location = 360,150
    translate1_node.label = "Left Eye Track Position"
    translate1_node.hide = True
    
    translate2_node = scifieye_group.nodes.new(type= 'CompositorNodeTranslate')
    translate2_node.location = 360,-50
    translate2_node.label = "Right Eye Track Position"
    translate2_node.hide = True
    
    alphaover1_node = scifieye_group.nodes.new(type= 'CompositorNodeAlphaOver')
    alphaover1_node.location = 600,300
    alphaover1_node.use_premultiply = True
    alphaover1_node.hide = True
    alphaover1_node.label = "Alpha 1"
    
        
    alphaover2_node = scifieye_group.nodes.new(type= 'CompositorNodeAlphaOver')
    alphaover2_node.location = 1000,300
    alphaover2_node.use_premultiply = True 
    alphaover2_node.hide = True   
    
    math1_node = scifieye_group.nodes.new(type= 'CompositorNodeMath')
    math1_node.location = 1050,200
    math1_node.hide = True  
    math1_node.operation = 'MULTIPLY'
    math1_node.use_clamp = True
    
    blur2_node = scifieye_group.nodes.new(type= 'CompositorNodeBlur')
    blur2_node.location = 1200,200
    blur2_node.hide = True  
    blur2_node.size_x = 1
    blur2_node.size_y = 1
    blur2_node.inputs[1].default_value = 0
    blur2_node.label = "Shadow Feather"
    blur2_node.hide = True
    
    
    
    alphaover3_node = scifieye_group.nodes.new(type= 'CompositorNodeAlphaOver')
    alphaover3_node.location = 1350,300
    alphaover3_node.inputs[2].default_value = (0, 0, 0, 0.5)
    alphaover3_node.label = "Shadow"
    alphaover3_node.hide = True
    
    
    
    #link nodes together
    
        
    scifieye_group.links.new(transf1_node.outputs[0], translate1_node.inputs[0])
    
    scifieye_group.links.new(translate1_node.outputs[0], alphaover1_node.inputs[2])
    
    
    scifieye_group.links.new(transf2_node.outputs[0], translate2_node.inputs[0])
    
    scifieye_group.links.new(translate2_node.outputs[0], alphaover2_node.inputs[2])
    
    scifieye_group.links.new(alphaover1_node.outputs[0], alphaover2_node.inputs[1])
    
    
    scifieye_group.links.new(alphaover2_node.outputs[0], alphaover3_node.inputs[1])
    
        
    scifieye_group.links.new(rerout1_node.outputs[0], transf1_node.inputs[0])
    
    scifieye_group.links.new(rerout1_node.outputs[0], transf2_node.inputs[0])

     
    scifieye_group.links.new(rerout2_node.outputs[0], alphaover1_node.inputs[0])
     
    scifieye_group.links.new(rerout2_node.outputs[0], alphaover2_node.inputs[0])
    
    scifieye_group.links.new(rgb1_node.outputs[0], alphaover1_node.inputs[1])
    
    scifieye_group.links.new(rerout2_node.outputs[0], rgb1_node.inputs[0])
    
    scifieye_group.links.new(blur1_node.outputs[0], rerout2_node.inputs[0])
    
    scifieye_group.links.new(rerout2_node.outputs[0], math1_node.inputs[1])
    
    scifieye_group.links.new(math1_node.outputs[0], blur2_node.inputs[0])
    
    scifieye_group.links.new(blur2_node.outputs[0], alphaover3_node.inputs[0])
    
    scifieye_group.links.new(inv1_node.outputs[0], rgb1_node.inputs[3])
    
    
    
    
    




        # link inputs
    scifieye_group.links.new(group_inputs.outputs['Eye Image'], rerout1_node.inputs[0])
    
    scifieye_group.links.new(group_inputs.outputs['Movie Clip'], rgb1_node.inputs[1])
    
    scifieye_group.links.new(group_inputs.outputs['Eye Lid Mask'], blur1_node.inputs[0])
    
    scifieye_group.links.new(group_inputs.outputs['Shadow Mask'], math1_node.inputs[0])
    scifieye_group.links.new(group_inputs.outputs['Shadow Feather'], blur2_node.inputs[1])
        
    scifieye_group.links.new(group_inputs.outputs['Left Eye (Track Pos X)'], translate1_node.inputs[1])
    
    scifieye_group.links.new(group_inputs.outputs['Left Eye (Track Pos Y)'], translate1_node.inputs[2])
    
    scifieye_group.links.new(group_inputs.outputs['Right Eye (Track Pos X)'], translate2_node.inputs[1])
    
    scifieye_group.links.new(group_inputs.outputs['Right Eye (Track Pos Y)'], translate2_node.inputs[2])
    
    scifieye_group.links.new(group_inputs.outputs['Left Eye: X'], transf1_node.inputs[1])
    
    scifieye_group.links.new(group_inputs.outputs['Left Eye: Y'], transf1_node.inputs[2])
    
    scifieye_group.links.new(group_inputs.outputs['Right Eye: X'], transf2_node.inputs[1])
    
    scifieye_group.links.new(group_inputs.outputs['Right Eye: Y'], transf2_node.inputs[2])
    
    scifieye_group.links.new(group_inputs.outputs['Left Eye: Rotation'], transf1_node.inputs[3])
    
    scifieye_group.links.new(group_inputs.outputs['Right Eye: Rotation'], transf2_node.inputs[3])
    
    scifieye_group.links.new(group_inputs.outputs['Left Eye: Scale'], transf1_node.inputs[4])
    
    scifieye_group.links.new(group_inputs.outputs['Right Eye: Scale'], transf2_node.inputs[4])
    
    scifieye_group.links.new(group_inputs.outputs['Eyeball Brightness'], inv1_node.inputs[1])
    
    scifieye_group.links.new(group_inputs.outputs['Eye Mask Feather'], blur1_node.inputs[1])
   
   
   
    
    #link output
    scifieye_group.links.new(alphaover3_node.outputs[0], group_outputs.inputs['Output'])
    
    

    # return the group
    return scifieye_group


# Create compositor group color presets
def create_colpre_group(context, operator, group_name):
    
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree 
    
        
    # Create a group
    colpre_group = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')
    
    # create group inputs
    group_inputs = colpre_group.nodes.new('NodeGroupInput')
    group_inputs.location = (-200,0)
    
        
    # create group outputs
    group_outputs = colpre_group.nodes.new('NodeGroupOutput')
    group_outputs.location = (200,0)
    colpre_group.outputs.new('NodeSocketColor','Natural White')
    colpre_group.outputs.new('NodeSocketColor','Slightly Aged')
    colpre_group.outputs.new('NodeSocketColor','Parchment 1')
    colpre_group.outputs.new('NodeSocketColor','Parchment 2')
    
    
       #nodes to be added to group
        
    natwhite_node = colpre_group.nodes.new(type= 'CompositorNodeRGB')
    natwhite_node.location = 0,200
    natwhite_node.location = 0,200
    natwhite_node.outputs[0].default_value = (0.938686, 0.930111, 0.846874, 1)
    natwhite_node.hide = True
    
    aged_node = colpre_group.nodes.new(type= 'CompositorNodeRGB')
    aged_node.location = 0,100
    aged_node.outputs[0].default_value = (0.887923, 0.854993, 0.597202, 1)
    aged_node.hide = True
    
    parch1_node = colpre_group.nodes.new(type= 'CompositorNodeRGB')
    parch1_node.location = 0,-100
    parch1_node.outputs[0].default_value = (0.83077, 0.665387, 0.450786, 1)
    parch1_node.hide = True
    
    parch2_node = colpre_group.nodes.new(type= 'CompositorNodeRGB')
    parch2_node.location = 0,-200
    parch2_node.outputs[0].default_value = (0.879623, 0.879623, 0.658375, 1)
    parch2_node.hide = True
    
    
    
        #link output
    colpre_group.links.new(natwhite_node.outputs[0], group_outputs.inputs['Natural White'])
    
    colpre_group.links.new(aged_node.outputs[0], group_outputs.inputs['Slightly Aged'])
    
    colpre_group.links.new(parch1_node.outputs[0], group_outputs.inputs['Parchment 1'])
    
    colpre_group.links.new(parch2_node.outputs[0], group_outputs.inputs['Parchment 2'])

    # return the group
    return colpre_group






# Create compositor group sketch
def create_sketch_group(context, operator, group_name):
    
    #set render res to 100
    bpy.context.scene.render.resolution_percentage = 100  
    
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree 
    
        
    # Create a group
    sketch_group = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')
    
    # create group inputs
    group_inputs = sketch_group.nodes.new('NodeGroupInput')
    group_inputs.location = (-200,400)
    
    sketch_group.inputs.new('NodeSocketColor','Movie Clip')
    
    sketch_group.inputs.new('NodeSocketFloat','Sketch Amount')
    
    sketch_group.inputs.new('NodeSocketFloat','Paper Image')
    
    sketch_group.inputs.new('NodeSocketColor','Paper Color')
    
    
    sketch_group.inputs[2].default_value = 1
    sketch_group.inputs[3].default_value = (1, 1, 1, 1)

    
    # create group outputs
    group_outputs = sketch_group.nodes.new('NodeGroupOutput')
    group_outputs.location = (2000,0)
    sketch_group.outputs.new('NodeSocketColor','Output')
    
    
        #nodes to be added to group
        
    rerout1_node = sketch_group.nodes.new(type= 'NodeReroute')
    rerout1_node.location = 0,0
    
    scale1_node = sketch_group.nodes.new(type= 'CompositorNodeScale')
    scale1_node.location = 100,-150
    scale1_node.label = "Scale 1"
    scale1_node.space = 'RENDER_SIZE'
    scale1_node.hide = True
    
    scale2_node = sketch_group.nodes.new(type= 'CompositorNodeScale')
    scale2_node.location = 100,150
    scale2_node.label = "Scale 2"
    scale2_node.space = 'RENDER_SIZE'
    scale2_node.hide = True
    
    
    
    
    rgbbw_node = sketch_group.nodes.new(type= 'CompositorNodeRGBToBW')
    rgbbw_node.location = 200,-100
    rgbbw_node.hide = True
    
    inv_node = sketch_group.nodes.new(type= 'CompositorNodeInvert')
    inv_node.location = 400,-250
    inv_node.hide = True
    
    blur1_node = sketch_group.nodes.new(type= 'CompositorNodeBlur')
    blur1_node.location = 650,-250
    blur1_node.size_x = 1
    blur1_node.size_y = 1
    blur1_node.hide = True
    blur1_node.filter_type = 'FAST_GAUSS'

    
    rgb_node = sketch_group.nodes.new(type= 'CompositorNodeCurveRGB')
    rgb_node.location = 900,-250
        
    mix1_node = sketch_group.nodes.new(type= 'CompositorNodeMixRGB')
    mix1_node.location = 400,-20
    mix1_node.blend_type = 'SATURATION'
    mix1_node.use_clamp = True
    mix1_node.hide = True
    
    mix2_node = sketch_group.nodes.new(type= 'CompositorNodeMixRGB')
    mix2_node.location = 1200,-20
    mix2_node.blend_type = 'DODGE'
    mix2_node.use_clamp = True
    mix2_node.hide = True
    
    mix3_node = sketch_group.nodes.new(type= 'CompositorNodeMixRGB')
    mix3_node.location = 1600,-20
    mix3_node.blend_type = 'MULTIPLY'
    mix3_node.use_clamp = True
    mix3_node.hide = True
    
    mix4_node = sketch_group.nodes.new(type= 'CompositorNodeMixRGB')
    mix4_node.location = 1900,-20
    mix4_node.blend_type = 'MULTIPLY'
    mix4_node.use_clamp = True
    mix4_node.label = "Mix4 col"
    
    
    
     #link nodes together
     
    sketch_group.links.new(rerout1_node.outputs[0], rgbbw_node.inputs[0]) 
    
    sketch_group.links.new(scale1_node.outputs[0], mix3_node.inputs[2])
    
    sketch_group.links.new(rerout1_node.outputs[0], mix1_node.inputs[1]) 

    
    sketch_group.links.new(rgbbw_node.outputs[0], inv_node.inputs[1])
    
    sketch_group.links.new(mix1_node.outputs[0], mix2_node.inputs[1])
    
    sketch_group.links.new(inv_node.outputs[0], blur1_node.inputs[0])
    
    sketch_group.links.new(blur1_node.outputs[0], rgb_node.inputs[1])
    
    sketch_group.links.new(rgb_node.outputs[0], mix2_node.inputs[2])
    
    sketch_group.links.new(mix2_node.outputs[0], mix3_node.inputs[1])
    
    sketch_group.links.new(mix3_node.outputs[0], mix4_node.inputs[1])
    
    sketch_group.links.new(scale2_node.outputs[0], mix4_node.inputs[2])
    
    
    # link inputs
    
    sketch_group.links.new(group_inputs.outputs['Movie Clip'], rerout1_node.inputs[0])
    
    sketch_group.links.new(group_inputs.outputs['Paper Image'], scale1_node.inputs[0])
    
    sketch_group.links.new(group_inputs.outputs['Sketch Amount'], blur1_node.inputs[1])
    
    sketch_group.links.new(group_inputs.outputs['Paper Color'], scale2_node.inputs[0])
    
    
        #link output
    sketch_group.links.new(mix4_node.outputs[0], group_outputs.inputs['Output'])

    # return the group
    return sketch_group


# Create compositor group vignette
def create_vig_group(context, operator, group_name):
    
    #set render res to 100
    bpy.context.scene.render.resolution_percentage = 100
    
    # Create a group
    create_vig_group = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')
    
     # create group inputs
    group_inputs = create_vig_group.nodes.new('NodeGroupInput')
    group_inputs.location = (-200,0)
    
    create_vig_group.inputs.new('NodeSocketColor','Movie Clip')
    create_vig_group.inputs.new('NodeSocketFloat','Position X')
    create_vig_group.inputs.new('NodeSocketFloat','Position Y')
    create_vig_group.inputs.new('NodeSocketFloat','Rotation')
    create_vig_group.inputs.new('NodeSocketFloat','Scale')
    create_vig_group.inputs.new('NodeSocketColor','Opacity')
    create_vig_group.inputs.new('NodeSocketFloat','Feather')
    create_vig_group.inputs.new('NodeSocketFloat','Perspective X')
    create_vig_group.inputs.new('NodeSocketFloat','Perspective Y')
    create_vig_group.inputs[1].default_value = 0
    create_vig_group.inputs[2].default_value = 0
    create_vig_group.inputs[5].default_value = (0, 0, 0, 0.5)
    create_vig_group.inputs[2].default_value = 0
    create_vig_group.inputs[4].default_value = 1
    create_vig_group.inputs[6].default_value = 0
    create_vig_group.inputs[7].default_value = 1
    create_vig_group.inputs[8].default_value = 1
    
    # create group outputs
    group_outputs = create_vig_group.nodes.new('NodeGroupOutput')
    group_outputs.location = (1000,0)
    create_vig_group.outputs.new('NodeSocketColor','Output')
    
        #nodes to be added to group
        
    elip_node = create_vig_group.nodes.new(type= 'CompositorNodeEllipseMask')
    elip_node.location = -100,400
    elip_node.width = 0.960076
    elip_node.height = 0.520152
    elip_node.hide = True
    
    scale_node = create_vig_group.nodes.new(type= 'CompositorNodeScale')
    scale_node.location = 0,0
    scale_node.hide = True
    

    
    transf_node = create_vig_group.nodes.new(type= 'CompositorNodeTransform')
    transf_node.location = 200,0
    transf_node.hide = True
    
    
    inv_node = create_vig_group.nodes.new(type= 'CompositorNodeInvert')
    inv_node.location = 400,0
    inv_node.hide = True
    
    
    blur_node = create_vig_group.nodes.new(type= 'CompositorNodeBlur')
    blur_node.location = 600,0
    blur_node.size_x = 1
    blur_node.size_y = 1
    blur_node.filter_type = 'FAST_GAUSS'
    blur_node.hide = True

    
    alp_node = create_vig_group.nodes.new(type= 'CompositorNodeAlphaOver')
    alp_node.location = 800,0
    alp_node.use_premultiply = True
    alp_node.hide = True
    
    
    
       
    
        #link nodes together
     
    create_vig_group.links.new(elip_node.outputs[0], scale_node.inputs[0])
    create_vig_group.links.new(scale_node.outputs[0], transf_node.inputs[0])
    create_vig_group.links.new(transf_node.outputs[0], inv_node.inputs[1])
    create_vig_group.links.new(inv_node.outputs[0], blur_node.inputs[0])
    
    create_vig_group.links.new(blur_node.outputs[0], alp_node.inputs[0])
    
    
        
        # link inputs
    
    create_vig_group.links.new(group_inputs.outputs['Movie Clip'], alp_node.inputs[1])
    create_vig_group.links.new(group_inputs.outputs['Position X'], transf_node.inputs[1])
    create_vig_group.links.new(group_inputs.outputs['Position Y'], transf_node.inputs[2])
    create_vig_group.links.new(group_inputs.outputs['Rotation'], transf_node.inputs[3])
    create_vig_group.links.new(group_inputs.outputs['Scale'], transf_node.inputs[4])
    create_vig_group.links.new(group_inputs.outputs['Opacity'], alp_node.inputs[2])
    create_vig_group.links.new(group_inputs.outputs['Feather'], blur_node.inputs[1])
    create_vig_group.links.new(group_inputs.outputs['Perspective X'], scale_node.inputs[1])
    create_vig_group.links.new(group_inputs.outputs['Perspective Y'], scale_node.inputs[2])
    
    
        #link output
    create_vig_group.links.new(alp_node.outputs[0], group_outputs.inputs['Output'])

    # return the group
    return create_vig_group















 #context for addition1 (eye col change)
def addition1(context):
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    
    bpy.context.scene.render.resolution_percentage = 100 
    
    
    #outside group nodes
    mov_node = tree.nodes.new(type= 'CompositorNodeMovieClip')
    mov_node.location = -200,0
    mov_node.select = False

    eyemask_node = tree.nodes.new(type= 'CompositorNodeMask')
    eyemask_node.location = -400,0
    eyemask_node.label = "Eye Mask"
    eyemask_node.select = False
    
    eyelidmask_node = tree.nodes.new(type= 'CompositorNodeMask')
    eyelidmask_node.location = -400,-110
    eyelidmask_node.label = "Eyelid Mask"
    eyelidmask_node.select = False
    
    garbmask_node = tree.nodes.new(type= 'CompositorNodeMask')
    garbmask_node.location = -400,-220
    garbmask_node.label = "Garbage Mask"
    garbmask_node.select = False   
    
                
    comp_node = tree.nodes.new(type= 'CompositorNodeComposite')
    comp_node.location = 500,-200
    comp_node.select = False
    
    view_node = tree.nodes.new(type= 'CompositorNodeViewer')
    view_node.location = 500,0
    view_node.select = False
         
    #connections bewteen nodes
    links = tree.links
    
    link = links.new(mov_node.outputs[0], comp_node.inputs[0])
    
    link = links.new(mov_node.outputs[0], view_node.inputs[0])
    
    
#context for addition2 (scifi eyes)
def addition2(context):
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree    
    
    bpy.context.scene.render.resolution_percentage = 100 


    #nodes outside group    
    mov_node = tree.nodes.new(type= 'CompositorNodeMovieClip')
    mov_node.location = -200,0
    mov_node.select = False
    mov_node.label = "Background Movie Clip"
    
    img_node = tree.nodes.new(type= 'CompositorNodeImage')
    img_node.location = 0,-200
    img_node.select = False
    img_node.label = "Sci fi Eye Image"
    
    trackpos_node = tree.nodes.new(type= 'CompositorNodeTrackPos')
    trackpos_node.location = -200,-400
    trackpos_node.select = False
    trackpos_node.label = "Left Eye Track Position"
    
    trackpos2_node = tree.nodes.new(type= 'CompositorNodeTrackPos')
    trackpos2_node.location = -200,-500
    trackpos2_node.select = False
    trackpos2_node.label = "Right Eye Track Position"
    
    mask1_node = tree.nodes.new(type= 'CompositorNodeMask')
    mask1_node.location = -400,100
    mask1_node.label = "Eye Lids Mask"
    mask1_node.select = False
    
    mask2_node = tree.nodes.new(type= 'CompositorNodeMask')
    mask2_node.location = -400,-120
    mask2_node.label = "Shadow Mask"
    mask2_node.select = False
        
    comp_node = tree.nodes.new(type= 'CompositorNodeComposite')
    comp_node.location = 1000,-100
    comp_node.select = False
    
    view_node = tree.nodes.new(type= 'CompositorNodeViewer')
    view_node.location = 1000,100
    view_node.select = False
    
    
    #connections bewteen nodes
    
    links = tree.links
    
    link = links.new(mov_node.outputs[0], comp_node.inputs[0])
    
    link = links.new(mov_node.outputs[0], view_node.inputs[0])



    #context for addition3 (Patch)
def addition3(context):
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree 
    
    bpy.context.scene.render.resolution_percentage = 100 

     #nodes to be added outside group
    mov1_node = tree.nodes.new(type= 'CompositorNodeMovieClip')
    mov1_node.location = 0,100
    mov1_node.select = False
    mov1_node.label = "Background Movie Clip"   
    
    mov2_node = tree.nodes.new(type= 'CompositorNodeMovieClip')
    mov2_node.location = 200,-100
    mov2_node.select = False 
    mov2_node.label = "Patch Movie Clip"  
    
    mask1_node = tree.nodes.new(type= 'CompositorNodeMask')
    mask1_node.location = -200,100
    mask1_node.select = False 
    mask1_node.label = "Patch Mask"
    
    trackpos1_node = tree.nodes.new(type= 'CompositorNodeTrackPos')
    trackpos1_node.location = -200,-90
    trackpos1_node.select = False
    trackpos1_node.label = "Track Position"
    
    
    comp_node = tree.nodes.new(type= 'CompositorNodeComposite')
    comp_node.location = 1000,-100
    comp_node.select = False
    
    view_node = tree.nodes.new(type= 'CompositorNodeViewer')
    view_node.location = 1000,100
    view_node.select = False
    
    
    
    #connections bewteen nodes
    links = tree.links
    
    link = links.new(mov1_node.outputs[0], comp_node.inputs[0])
    
    link = links.new(mov1_node.outputs[0], view_node.inputs[0])



    #context for addition4 (Clone)
def addition4(context):
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree 
    
    bpy.context.scene.render.resolution_percentage = 100 
    
     #nodes to be added outside group
    mov1_node = tree.nodes.new(type= 'CompositorNodeMovieClip')
    mov1_node.location = 400,100
    mov1_node.select = False
    mov1_node.label = "Background Movie Clip"   
    
       
    mask1_node = tree.nodes.new(type= 'CompositorNodeMask')
    mask1_node.location = 200,100
    mask1_node.select = False 
    mask1_node.label = "Clone Mask"
    
        
    comp_node = tree.nodes.new(type= 'CompositorNodeComposite')
    comp_node.location = 1000,-100
    comp_node.select = False
    
    view_node = tree.nodes.new(type= 'CompositorNodeViewer')
    view_node.location = 1000,100
    view_node.select = False
    
    
    
    #connections bewteen nodes
    links = tree.links
    
    link = links.new(mov1_node.outputs[0], comp_node.inputs[0])
    
    link = links.new(mov1_node.outputs[0], view_node.inputs[0])



    #context for addition5 (glitch)
def addition5(context):
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree 
    
    bpy.context.scene.render.resolution_percentage = 100 
    
    #nodes to be added outside of group
    mov1_node = tree.nodes.new(type= 'CompositorNodeMovieClip')
    mov1_node.location = -200,400
    mov1_node.select = False
    
    img1_node = tree.nodes.new(type= 'CompositorNodeImage')
    img1_node.location = -400,400
    img1_node.select = False
    img1_node.label = "Glitch Image"
    
    comp_node = tree.nodes.new(type= 'CompositorNodeComposite')
    comp_node.location = 700,300
    comp_node.select = False
    
    view_node = tree.nodes.new(type= 'CompositorNodeViewer')
    view_node.location = 700,400
    view_node.select = False
    
    #connections bewteen nodes
    links = tree.links
    
    link = links.new(mov1_node.outputs[0], comp_node.inputs[0])
    link = links.new(mov1_node.outputs[0], view_node.inputs[0])



    #context for addition6 (sketch)
def addition6(context):
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree 
    
    bpy.context.scene.render.resolution_percentage = 100 
    
    #nodes to be added outisde of the group 
    mov1_node = tree.nodes.new(type= 'CompositorNodeMovieClip')
    mov1_node.location = -100,400
    mov1_node.select = False 
    
    img1_node = tree.nodes.new(type= 'CompositorNodeImage')
    img1_node.location = -300,400
    img1_node.select = False
    img1_node.label = "Paper Image"    
       
    
         
    comp_node = tree.nodes.new(type= 'CompositorNodeComposite')
    comp_node.location = 900,200
    comp_node.select = False
    
    view_node = tree.nodes.new(type= 'CompositorNodeViewer')
    view_node.location = 900,400
    view_node.select = False
    
    #connections bewteen nodes
    links = tree.links
    
    link = links.new(mov1_node.outputs[0], comp_node.inputs[0])
    
    link = links.new(mov1_node.outputs[0], view_node.inputs[0])
    
    
    
    
    
    #context for addition7 (post)
def addition7(context):
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree 
    
    bpy.context.scene.render.resolution_percentage = 100 
    
    
    #nodes to be added 
    mov1_node = tree.nodes.new(type= 'CompositorNodeMovieClip')
    mov1_node.location = 0,400
    mov1_node.select = False 
        
    comp_node = tree.nodes.new(type= 'CompositorNodeComposite')
    comp_node.location = 1200,200
    comp_node.select = False
    
    view_node = tree.nodes.new(type= 'CompositorNodeViewer')
    view_node.location = 1200,400
    view_node.select = False
    
    links = tree.links
    
    
    link = links.new(mov1_node.outputs[0], comp_node.inputs[0])
    
    link = links.new(mov1_node.outputs[0], view_node.inputs[0])
    
    
    
    #context for addition8 (ink drop)
def addition8(context):
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree 
    
    bpy.context.scene.render.resolution_percentage = 100 
    
    
    #nodes to be added outside of group
    mov1_node = tree.nodes.new(type= 'CompositorNodeMovieClip')
    mov1_node.location = 400,400
    mov1_node.select = False 
    mov1_node.label = "Smoke Movie Clip"
    
    img1_node = tree.nodes.new(type= 'CompositorNodeImage')
    img1_node.location = 200,400
    img1_node.select = False 
    img1_node.label = "Black and White Image (Your Text)"
    
    comp_node = tree.nodes.new(type= 'CompositorNodeComposite')
    comp_node.location = 1000,300
    comp_node.select = False
    
    view_node = tree.nodes.new(type= 'CompositorNodeViewer')
    view_node.location = 1000,400
    view_node.select = False



    links = tree.links
    
    
    link = links.new(mov1_node.outputs[0], comp_node.inputs[0])
  
    link = links.new(mov1_node.outputs[0], view_node.inputs[0])
    
    

#context for addition9 (Marker Removal)
def addition9(context):
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree 
    
    bpy.context.scene.render.resolution_percentage = 100 
    
    
    #nodes to be added outside of group
    mov1_node = tree.nodes.new(type= 'CompositorNodeMovieClip')
    mov1_node.location = 300,-500
    mov1_node.select = False 
    mov1_node.label = "Movie Clip"
    
    mask1_node = tree.nodes.new(type= 'CompositorNodeMask')
    mask1_node.location = 100,-500
    mask1_node.select = False 
    mask1_node.label = "Marker Removal Mask"
    
    comp_node = tree.nodes.new(type= 'CompositorNodeComposite')
    comp_node.location = 800,-500
    comp_node.select = False
    
    view_node = tree.nodes.new(type= 'CompositorNodeViewer')
    view_node.location = 1000,-650
    view_node.select = False



    links = tree.links
    
    
    link = links.new(mov1_node.outputs[0], comp_node.inputs[0])
  
    link = links.new(mov1_node.outputs[0], view_node.inputs[0])    
    
    
    
    
    
    
    
    
    
    
    
    
    






 #Context for remove  nodes
def rem(context):
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree 
    
    
    #removes unwanted nodes
    for node in tree.nodes:
        tree.nodes.remove(node)
        
        
        
        
 #operation to add remove Nodes   
class RemOP(bpy.types.Operator):
    """Click this Button to remove the Nodes from the Compositor Window"""
    bl_idname = "rem.addnodes"
    bl_label = " Remove Nodes"

    def execute(self, context):
        rem(context)
        return {'FINISHED'}









    #operation to addition1 (eyecol)  
class Addition1OP(bpy.types.Operator):
    """Click this Button to add the Additional Nodes. Movie Clip, Masks and Output."""
    bl_idname = "addition1.addnodes"
    bl_label = " Additional Nodes"

    def execute(self, context):
        addition1(context)
        return {'FINISHED'}  
    
    
    #operation to addition2 (scifi eyes)  
class Addition2OP(bpy.types.Operator):
    """Click this Button to add the Additional Nodes. Movie Clip, Masks, Image and Output."""
    bl_idname = "addition2.addnodes"
    bl_label = " Additional Nodes"

    def execute(self, context):
        addition2(context)
        return {'FINISHED'} 
    
    #operation to addition3 (patch)  
class Addition3OP(bpy.types.Operator):
    """Click this Button to add the Additional Nodes. Movie Clips, Masks and Output."""
    bl_idname = "addition3.addnodes"
    bl_label = " Additional Nodes"

    def execute(self, context):
        addition3(context)
        return {'FINISHED'} 
    
    #operation to addition4 (clone)  
class Addition4OP(bpy.types.Operator):
    """Click this Button to add the Additional Nodes. Movie Clip, Masks and Output."""
    bl_idname = "addition4.addnodes"
    bl_label = " Additional Nodes"

    def execute(self, context):
        addition4(context)
        return {'FINISHED'} 
    
    #operation to addition5 (glitch)  
class Addition5OP(bpy.types.Operator):
    """Click this Button to add the Additional Nodes. Movie Clip, Image and Output."""
    bl_idname = "addition5.addnodes"
    bl_label = " Additional Nodes"

    def execute(self, context):
        addition5(context)
        return {'FINISHED'} 
    
    
    #operation to addition6 (sketch)  
class Addition6OP(bpy.types.Operator):
    """Click this Button to add the Additional Nodes. Movie Clip and Output."""
    bl_idname = "addition6.addnodes"
    bl_label = " Additional Nodes"

    def execute(self, context):
        addition6(context)
        return {'FINISHED'} 
    
    #operation to addition7 (post)  
class Addition7OP(bpy.types.Operator):
    """Click this Button to add the Additional Nodes. Movie Clip and Output."""
    bl_idname = "addition7.addnodes"
    bl_label = " Additional Nodes"

    def execute(self, context):
        addition7(context)
        return {'FINISHED'} 
    
    #operation to addition8 (ink drop)  
class Addition8OP(bpy.types.Operator):
    """Click this Button to add the Additional Nodes. Movie Clip and Output."""
    bl_idname = "addition8.addnodes"
    bl_label = " Additional Nodes"

    def execute(self, context):
        addition8(context)
        return {'FINISHED'} 



    #operation to addition9 (Marker Removal)  
class Addition9OP(bpy.types.Operator):
    """Click this Button to add the Additional Nodes. Movie Clip and Output."""
    bl_idname = "addition9.addnodes"
    bl_label = " Additional Nodes"

    def execute(self, context):
        addition9(context)
        return {'FINISHED'} 







        



# Operator Col Change
class NODE_OT_colchangeGroup(bpy.types.Operator):
    """Click this button to add the Eye Color Change Node Group"""
    bl_idname = "node.colchange_operator"
    bl_label = "Eye Color Change"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR'

    def execute(self, context):

        # Create the group
        custom_node_name = "Color Change Node"
        my_group = create_eyecol_group(self, context, custom_node_name)
        eyecol_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        eyecol_node.node_tree = bpy.data.node_groups[my_group.name]
        eyecol_node.location = 100,0
        eyecol_node.select = False
        eyecol_node.use_custom_color = True
        eyecol_node.color = (0.375501, 0.866654, 0.702325)
        eyecol_node.width= 200       

        
        return {'FINISHED'}
    
    
    
    
    
    
    # Operator Scifi Eyes
class NODE_OT_scifieyesGroup(bpy.types.Operator):
    """Click this button to add the Sci-fi Eyes Node Group"""
    bl_idname = "node.scifieyes_operator"
    bl_label = "Sci-fi Eyes"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR'

    def execute(self, context):

        # Create the group
        custom_node_name = "Sci-fi Eyes Node"
        my_group = create_scifieye_group(self, context, custom_node_name)
        scifieye_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        scifieye_node.node_tree = bpy.data.node_groups[my_group.name]
        scifieye_node.location = 300,-0
        scifieye_node.use_custom_color = True
        scifieye_node.color = (0.0754633, 0.73702, 0.0112345)
        scifieye_node.select = False
        scifieye_node.width= 230

        return {'FINISHED'}
    
    
    
# Operator Patch
class NODE_OT_patchGroup(bpy.types.Operator):
    """Click this button to add the Patch Node Group"""
    bl_idname = "node.patch_operator"
    bl_label = "Patch Node"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR'

    def execute(self, context):

        # Create the group
        custom_node_name = "Patch Node"
        my_group = create_patch_group(self, context, custom_node_name)
        patch_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        patch_node.node_tree = bpy.data.node_groups[my_group.name]
        patch_node.location = 500,-0
        patch_node.use_custom_color = True
        patch_node.color = (0.226723, 0.734245, 0.759009)
        patch_node.select = False
        patch_node.width= 210

        return {'FINISHED'}    
    





# Operator Planar tool
class NODE_OT_planarGroup(bpy.types.Operator):
    """Click this button to add the 2D Planar Node Group"""
    bl_idname = "node.planar_operator"
    bl_label = "2D Planar Tool"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR'

    def execute(self, context):

        # Create the group
        custom_node_name = "2D Planar Node"
        my_group = create_planar_group(self, context, custom_node_name)
        planar_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        planar_node.node_tree = bpy.data.node_groups[my_group.name]
        planar_node.location = 500,-0
        planar_node.use_custom_color = True
        planar_node.color = (0.608, 0.51478, 0.490594)
        planar_node.select = False
        planar_node.width= 210
        
        planartrack_node = context.scene.node_tree.nodes.new('CompositorNodePlaneTrackDeform')
        planartrack_node.location = 300,-100
        planartrack_node.select = False
        
        img_node = context.scene.node_tree.nodes.new('CompositorNodeImage')
        img_node.location = 100,-100
        img_node.select = False
        
        
        tree = bpy.context.scene.node_tree
        links = tree.links
        link = links.new(planartrack_node.outputs[0], planar_node.inputs[2])
        link = links.new(img_node.outputs[0], planartrack_node.inputs[0])

        return {'FINISHED'}  









# Operator subsurface node
class NODE_OT_subsurfaceGroup(bpy.types.Operator):
    """Click this button to add the Subsurface Node Group"""
    bl_idname = "node.subsurface_operator"
    bl_label = "Subsurface Skin Node"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR'

    def execute(self, context):

        # Create the group
        custom_node_name = "Subsurface Skin Node"
        my_group = create_subsurface_group(self, context, custom_node_name)
        subsurface_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        subsurface_node.node_tree = bpy.data.node_groups[my_group.name]
        subsurface_node.location = 500,-300
        subsurface_node.use_custom_color = True
        subsurface_node.color = (0.608, 0.389065, 0.329328)
        

        subsurface_node.select = False
        subsurface_node.width= 210
        
        planartrack_node = context.scene.node_tree.nodes.new('CompositorNodePlaneTrackDeform')
        planartrack_node.location = 300,-300
        planartrack_node.select = False
        
        material_node = context.scene.node_tree.nodes.new('CompositorNodeTexture')
        material_node.location = 100,-300
        material_node.select = False
        material_node.outputs[0].hide = True
        
        
        
        tree = bpy.context.scene.node_tree
        links = tree.links
        link = links.new(planartrack_node.outputs[0], subsurface_node.inputs[2])
        link = links.new(material_node.outputs[1], planartrack_node.inputs[0])
        
        
        
        
        
        
       

        # Create the texture
        my_texture = bpy.data.textures.new('SubsurfaceSkinTexture', 'IMAGE')

        # Enable use nodes
        my_texture.use_nodes = True

        # Get the tree
        tex_tree = my_texture.node_tree
        

        # Clear default nodes
        for node in tex_tree.nodes:
            tex_tree.nodes.remove(node)

        # Create Nodes
        out = tex_tree.nodes.new('TextureNodeOutput')
        out.location = (800,100)
        
        noise1 = tex_tree.nodes.new('TextureNodeTexMarble')
        noise1.location = (0,100)
        #noise1.noise_type = 'HARD_NOISE'
        #noise1.noise_basis = 'ORIGINAL_PERLIN'
        noise1.inputs[2].default_value = 0.95
        noise1.inputs[3].default_value = 13.8
        
        
        
        material_node.texture = my_texture
        
        
        
        # Enable use nodes in the compositor
        context.scene.use_nodes = True

        # Get the tree
        comp_tree = context.scene.node_tree

        
        
        # Link Group to Output
        
        tex_tree.links.new(noise1.outputs[0], out.inputs[0])

        return {'FINISHED'}













    



# Operator Marker removal
class NODE_OT_markerremGroup(bpy.types.Operator):
    """Click this button to add the Marker Removal Node Group"""
    bl_idname = "node.markerrem_operator"
    bl_label = "Marker Removal Node"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR'

    def execute(self, context):

        # Create the group
        custom_node_name = "Marker Removal Node"
        my_group = create_markerrem_group(self, context, custom_node_name)
        markerrem_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        markerrem_node.node_tree = bpy.data.node_groups[my_group.name]
        markerrem_node.location = 500,-500
        markerrem_node.use_custom_color = True
        markerrem_node.color = (0.0757802, 0.509969, 0.759009)

        markerrem_node.select = False
        markerrem_node.width= 200

        return {'FINISHED'} 


    
    
    
    
    
    
# Operator clone
class NODE_OT_cloneGroup(bpy.types.Operator):
    """Click this button to add the Clone Node Group"""
    bl_idname = "node.clone_operator"
    bl_label = "Clone Node"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR'

    def execute(self, context):

        # Create the group
        custom_node_name = "Clone Node"
        my_group = create_clone_group(self, context, custom_node_name)
        clone_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        clone_node.node_tree = bpy.data.node_groups[my_group.name]
        clone_node.location = 700,-0
        clone_node.use_custom_color = True
        clone_node.color = (0.0143871, 0.56356, 0.680215)
        clone_node.select = False
        clone_node.width= 210

        return {'FINISHED'}      
    
    
    


# Operator glitch
class NODE_OT_glitchGroup(bpy.types.Operator):
    """Click this button to add the Glitch Node Group"""
    bl_idname = "node.glitch_operator"
    bl_label = "Glitch Node"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR'

    def execute(self, context):
        sc = context.scene
        tree = sc.node_tree

        # Create the group
        custom_node_name = "Glitch Node"
        my_group = create_glitch_group(self, context, custom_node_name)
        glitch_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        glitch_node.node_tree = bpy.data.node_groups[my_group.name]
        glitch_node.location = 100,400
        glitch_node.use_custom_color = True
        
        
        glitch_node.color = (0.627484, 0.426714, 0.8195)
        
        glitch_node.width= 210
        
        
        glitch_node.inputs[6].default_value = 7
        glitch_node.inputs[6].keyframe_insert("default_value", frame= 30)
        glitch_node.select = True
        
        data_path = f'nodes["{glitch_node.name}"].inputs[6].default_value'
        fcurves = tree.animation_data.action.fcurves
        fc = fcurves.find(data_path)
        if fc:
            new_mod = fc.modifiers.new('NOISE')
            new_mod.strength = 200
        
        
        

        return {'FINISHED'}     
    
    
    
    
    
    
    
# Operator color presets
class NODE_OT_colpreGroup(bpy.types.Operator):
    """Click this button to add the Color Presets Node Group"""
    bl_idname = "node.colper_operator"
    bl_label = "Color Presets Node"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR'

    def execute(self, context):

        # Create the group
        custom_node_name = "Color Presets Node"
        my_group = create_colpre_group(self, context, custom_node_name)
        colpre_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        colpre_node.node_tree = bpy.data.node_groups[my_group.name]
        colpre_node.location = 300,200
        colpre_node.use_custom_color = True
        colpre_node.color = (0.560462, 0.680215, 0.56744)  
        colpre_node.select = False
        colpre_node.width= 150

        return {'FINISHED'}      
     

# Operator TransitionNode
class NODE_OT_transitionGroup(bpy.types.Operator):
    """Click this button to add the Transition Node"""
    bl_idname = "node.transition_operator"
    bl_label = "Transition Node"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR'

    def execute(self, context):

        # Create the group
        custom_node_name = "Transition Node"
        my_group = create_transition_group(self, context, custom_node_name)
        trans_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        trans_node.node_tree = bpy.data.node_groups[my_group.name]
        trans_node.location = 300,400
        trans_node.use_custom_color = True
        trans_node.color = (0.375223, 0.526236, 0.680215)
        trans_node.select = False
        trans_node.width= 200

        return {'FINISHED'} 
    
    
    
    
    
    
# Operator sketch
class NODE_OT_sketchGroup(bpy.types.Operator):
    """Click this button to add the Sketch Node Group"""
    bl_idname = "node.sketch_operator"
    bl_label = "Sketch Node"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR'

    def execute(self, context):

        # Create the group
        custom_node_name = "Sketch Node"
        my_group = create_sketch_group(self, context, custom_node_name)
        sketch_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        sketch_node.node_tree = bpy.data.node_groups[my_group.name]
        sketch_node.location = 300,400
        sketch_node.use_custom_color = True
        sketch_node.color = (0.560462, 0.680215, 0.56744)
        sketch_node.select = False
        sketch_node.width= 210

        return {'FINISHED'}      
    
    
# Operator post1
class NODE_OT_post1group(bpy.types.Operator):
    """Click this button to add the Posterize Node: Option 1"""
    bl_idname = "node.post1_operator"
    bl_label = "Option 1"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR'

    def execute(self, context):

        # Create the group
        custom_node_name = "Posterize Effect Option 1"
        my_group = create_post1_group(self, context, custom_node_name)
        post1_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        post1_node.node_tree = bpy.data.node_groups[my_group.name]
        post1_node.location = 500,400
        post1_node.use_custom_color = True
        post1_node.color = (0.451251, 0.191486, 0.374164)  
        post1_node.select = False
        post1_node.width= 170

        return {'FINISHED'}      
    
    # Operator post2
class NODE_OT_post2group(bpy.types.Operator):
    """Click this button to add the Posterize Node: Option 2"""
    bl_idname = "node.post2_operator"
    bl_label = "Option 2"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR'

    def execute(self, context):

        # Create the group
        custom_node_name = "Posterize Effect Option 2"
        my_group = create_post2_group(self, context, custom_node_name)
        post2_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        post2_node.node_tree = bpy.data.node_groups[my_group.name]
        post2_node.location = 500,300
        post2_node.use_custom_color = True
        post2_node.color = (0.715406, 0.387641, 0.577297)
        post2_node.select = False
        post2_node.width= 170

        return {'FINISHED'} 
    
    
    
# Operator post3
class NODE_OT_post3group(bpy.types.Operator):
    """Click this button to add the Posterize Node: Option 3"""
    bl_idname = "node.post3_operator"
    bl_label = "Option 3"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR'

    def execute(self, context):

        # Create the group
        custom_node_name = "Posterize Effect Option 3"
        my_group = create_post3_group(self, context, custom_node_name)
        post3_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        post3_node.node_tree = bpy.data.node_groups[my_group.name]
        post3_node.location = 500,200
        post3_node.use_custom_color = True
        post3_node.color = (0.632678, 0.273532, 0.389893)
        post3_node.select = False
        post3_node.width= 170

        return {'FINISHED'}     
    
    
    # Operator Ink drop
class NODE_OT_inkdropgroup(bpy.types.Operator):
    """Click this button to add the Ink drop Node Group"""
    bl_idname = "node.inkdrop_operator"
    bl_label = "Ink Drop Node"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR'

    def execute(self, context):

        # Create the group
        custom_node_name = "Ink Drop Effect Node"
        my_group = create_inkdrop_group(self, context, custom_node_name)
        inkdrop_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        inkdrop_node.node_tree = bpy.data.node_groups[my_group.name]
        inkdrop_node.location = 700,400
        inkdrop_node.use_custom_color = True
        inkdrop_node.color = (0.310401, 0.32662, 0.32662)
        inkdrop_node.select = False
        inkdrop_node.width= 210

        return {'FINISHED'}   
    
    
    








    # Operator Vignette effect
class NODE_OT_viggroup(bpy.types.Operator):
    """Click this button to add a Vignette Node Group"""
    bl_idname = "node.vig_operator"
    bl_label = "Vignette Node"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR'

    def execute(self, context):

        # Create the group
        custom_node_name = "Vignette Node"
        my_group = create_vig_group(self, context, custom_node_name)
        vig_node = context.scene.node_tree.nodes.new('CompositorNodeGroup')
        vig_node.node_tree = bpy.data.node_groups[my_group.name]
        vig_node.location = 900,400
        vig_node.use_custom_color = True
        vig_node.color = (0.102573, 0.116922, 0.152942)
        


        vig_node.select = False
        vig_node.width= 210

        return {'FINISHED'}   







    
    
    


# Main Panel
class NODE_PT_customPanel(bpy.types.Panel):
    bl_idname = "NODE_PT_customPanel"
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Darkfall VFX Nodes"
    bl_region_type = "UI"
    bl_category = "Darkfall VFX Nodes"

    

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.object
        
        #Welcome text
        
        layout.label(text="______________________________________")
        row = layout.row()
        row = layout.row()
        layout.label(text=" Select one of the VFX Panels, and")
        layout.label(text=" choose the effect you wish to create.")
        row = layout.row()
        row = layout.row()
        layout.label(text=" Visit our blog for more information.")
        layout.label(text="______________________________________")
        




#planar sub18 panel
class Sub18Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "planarpanel"
    bl_idname = "OBJECT_PT_planar"
    bl_space_type = 'NODE_EDITOR'
    bl_label = "2D Planar Tool"
    bl_region_type = "UI"
    bl_category = "Darkfall VFX Nodes"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'OBJECT_PT_toolseffect'

    def draw(self, context):
        layout = self.layout
        obj = context.object
        
            
        

        box = layout.box()

        row = box.row()
        row.prop(obj, "expanded",
            icon="TRIA_DOWN" if obj.expanded else "TRIA_RIGHT",
            icon_only=True, emboss=False
            
)
                    
                  
        row.label(text="Planar Info", icon= 'LIGHTPROBE_PLANAR')
        

        if obj.expanded:
            row = box.row()
            

            row = box.row()
        
            row = box.row()
            row.label(text=" The Planar Tool will take an area")
            row = box.row()
            row.label(text=" of your Movie clip and add an")
            row = box.row()
            row.label(text=" image or Movie Clip.")
            row = box.row()
            row.label(text=" You can also create a")
            row = box.row()
            row.label(text=" Drop Shadow, if needed.")
            row = box.row()
            row = box.row()
            row = box.row()
            row.label(text=" The Subsurface Skin Effect will.")
            row = box.row()
            row.label(text=" add a texture along with the.")
            row = box.row()
            row.label(text=" 2D Planar Tool.")
            row = box.row()
           
        row = layout.row()
        layout.operator(NODE_OT_planarGroup.bl_idname, icon= 'CHECKBOX_DEHLT')
        layout.operator(NODE_OT_subsurfaceGroup.bl_idname, icon= 'USER')
        
        row = layout.row()
        row.operator("addition4.addnodes", icon= 'NODE_SEL')
        row.operator("rem.addnodes", icon= 'CANCEL')
        row = layout.row()
                
        
        row = layout.row()
        
        row = layout.row()

















        

#clone sub1 panel
class Sub1Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "clonepanel"
    bl_idname = "OBJECT_PT_clone"
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Clone Node"
    bl_region_type = "UI"
    bl_category = "Darkfall VFX Nodes"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'OBJECT_PT_toolseffect'

    def draw(self, context):
        layout = self.layout
        obj = context.object
        
            
        

        box = layout.box()

        row = box.row()
        row.prop(obj, "expanded",
            icon="TRIA_DOWN" if obj.expanded else "TRIA_RIGHT",
            icon_only=True, emboss=False
            
)
                    
                  
        row.label(text="Clone Info", icon= 'ZOOM_PREVIOUS')
        

        if obj.expanded:
            row = box.row()
            

            row = box.row()
        
            row = box.row()
            row.label(text=" The Clone Node will take an area")
            row = box.row()
            row.label(text=" of your Movie clip and replace.")            
            row = box.row()
            row.label(text=" it with a diffrent section of our clip.")
            row = box.row()
            row = box.row()
            row.label(text=" With a Mask we can define the area we")
            row = box.row()
            row.label(text=" want to be replaced, cloning over")
            row = box.row()
            row.label(text=" any unwanted objects.")
            row = box.row()
           
        row = layout.row()
        layout.operator(NODE_OT_cloneGroup.bl_idname, icon= 'ZOOM_SELECTED')
        
        row = layout.row()
        row.operator("addition4.addnodes", icon= 'NODE_SEL')
        row.operator("rem.addnodes", icon= 'CANCEL')
        row = layout.row()
                
        
        row = layout.row()
        
        row = layout.row()
        
        
        
        
        
#eye color sub panel 4
class Sub4Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "eyecolpanel"
    bl_idname = "OBJECT_PT_eyecol"
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Eye Color Change"
    bl_region_type = "UI"
    bl_category = "Darkfall VFX Nodes"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'OBJECT_PT_eyeeffect'
    

    def draw(self, context):
        layout = self.layout
        obj = context.object
        
        
        
            
        

        box = layout.box()

        row = box.row()
        row.prop(obj, "expanded",
            icon="TRIA_DOWN" if obj.expanded else "TRIA_RIGHT",
            icon_only=True, emboss=False
            
)
                    
                  
        row.label(text="Eye Color Change Info", icon= 'VIS_SEL_11')
        

        if obj.expanded:
            row = box.row()
            

            row = box.row()
        
            row.label(text=" The Eye Color Change, will change")
            row = box.row()
            row.label(text=" the Color of your subject's eyes")
            row = box.row()
            
            row = box.row()
            row.label(text=" You will need a Mask for the Eyes,")
            row = box.row()
            row.label(text=" another for the Eyelids, and one")
            row = box.row()
            row.label(text=" (though not compulsory) for the")
            row = box.row()
            row.label(text=" Garbage.")
            row = box.row()
                    
        
            
        row = layout.row(align=True)
        layout.operator(NODE_OT_colchangeGroup.bl_idname, icon= 'VIS_SEL_11')
        
        
        row = layout.row()
        row.operator("addition1.addnodes", icon= 'NODE_SEL')
        row.operator("rem.addnodes", icon= 'CANCEL')
        row = layout.row()
        row = layout.row()
        row = layout.row()





#glitch sub5 panel
class Sub5Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "glitchpanel"
    bl_idname = "OBJECT_PT_glitch"
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Glitch Node"
    bl_region_type = "UI"
    bl_category = "Darkfall VFX Nodes"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'OBJECT_PT_artisticeffect'
    
   

    def draw(self, context):
        layout = self.layout
        obj = context.object
        
            
        

        box = layout.box()

        row = box.row()
        row.prop(obj, "expanded",
            icon="TRIA_DOWN" if obj.expanded else "TRIA_RIGHT",
            icon_only=True, emboss=False
            
)
                    
                  
        row.label(text="Glitch Info", icon= 'HAND')
        

        if obj.expanded:
            row = box.row()
            

            row = box.row()
        
            row = box.row()
            row.label(text=" The Glitch Effect will take a Movie")
            row = box.row()
            row.label(text=" clip and add a Glitch Effect.")            
            row = box.row()
            row = box.row()
            row.label(text=" You will need an Image for the")
            row = box.row()
            row.label(text=" Glitch Pattern movement or you")
            row = box.row()
            row.label(text=" use the Scan line Generator button.")
            row = box.row()
            row = box.row()
        
          
        row = layout.row()
        row.operator(NODE_OT_glitchGroup.bl_idname, icon= 'HAND')
        row = layout.row()
        
        
        
        row.operator("node.scanline_operator", icon= 'LINENUMBERS_OFF')
        row = layout.row()
        row.operator("addition5.addnodes", icon= 'NODE_SEL')
        
        row.operator("rem.addnodes", icon= 'CANCEL')
        row = layout.row()
        row = layout.row()
        
        row = layout.row()
















#props  panel
class NODE_PT_active_node_properties(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "props"
    bl_idname = "OBJECT_PT_propert"
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Properties"
    bl_region_type = "UI"
    bl_category = "Darkfall VFX Nodes"
    bl_options = {'DEFAULT_CLOSED'}
        
    @classmethod
    def poll(cls, context):
        return context.active_node is not None

    def draw(self, context):
        layout = self.layout
        node = context.active_node
        
        layout.context_pointer_set("node", node)

        if hasattr(node, "draw_buttons_ext"):
            node.draw_buttons_ext(context, layout)
        elif hasattr(node, "draw_buttons"):
            node.draw_buttons(context, layout)

        
        value_inputs = [socket for socket in node.inputs if socket.enabled and not socket.is_linked]
        if value_inputs:
            layout.separator()
            layout.label(text="Inputs:")
            for socket in value_inputs:
                row = layout.row()
                socket.draw(context, row, node, iface_(socket.name, socket.bl_rna.translation_context))













#Gradient sub10 panel
class Sub10Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "gradpanel"
    bl_idname = "OBJECT_PT_grad"
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Gradient Node"
    bl_region_type = "UI"
    bl_category = "Darkfall VFX Nodes"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'OBJECT_PT_toolseffect'
    
    

    def draw(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        strip = scene.render
        
        
        

        
        row = layout.row()
        
       
        

        box = layout.box()

        row = box.row()
        row.prop(obj, "expanded",
            icon="TRIA_DOWN" if obj.expanded else "TRIA_RIGHT",
            icon_only=True, emboss=False
            
)
                    
                  
        row.label(text="Gradient Info", icon= 'RIGID_BODY')
        

        if obj.expanded:
            row = box.row()
            

            row = box.row()
        
            row = box.row()
            row.label(text=" Add a simple Gradient effect to")
            row = box.row()
            row.label(text=" your videos.")           
            row = box.row()
            row = box.row()
            row.label(text=" You can move and scale the Effect") 
            row = box.row()
            row.label(text=" to suit your needs.") 
            row = box.row()
        
        row = layout.row()
        
        row.operator("node.gradient_operator", icon= 'RIGID_BODY')
        row = layout.row()
        row.operator("rem.addnodes", icon= 'CANCEL')
        row = layout.row()
        
        
        
        
        
        
        
        row = layout.row()






#Scanline sub15 panel
class Sub15Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "scanpanel"
    bl_idname = "OBJECT_PT_scan"
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Scan line Generator"
    bl_region_type = "UI"
    bl_category = "Darkfall VFX Nodes"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'OBJECT_PT_toolseffect'
    
    

    def draw(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        strip = scene.render
        
        
        

        
        row = layout.row()
        
       
        

        box = layout.box()

        row = box.row()
        row.prop(obj, "expanded",
            icon="TRIA_DOWN" if obj.expanded else "TRIA_RIGHT",
            icon_only=True, emboss=False
            
)
                    
                  
        row.label(text="Scan line Info", icon= 'LINENUMBERS_OFF')
        

        if obj.expanded:
            row = box.row()
            

            row = box.row()
        
            row = box.row()
            row.label(text=" Add a Scan line to your videos")
            row = box.row()
            row.label(text=" with the help of this node.")           
            row = box.row()
            row = box.row()
            row = box.row()
        
        row = layout.row()
        
        row.operator("node.scanline_operator", icon= 'LINENUMBERS_OFF')
        row = layout.row()
        row.operator("rem.addnodes", icon= 'CANCEL')
        row = layout.row()
        
        
        
        
        
        
        
        row = layout.row()












#Transition sub20 panel
class Sub20Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "transitionpanel"
    bl_idname = "OBJECT_PT_transition"
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Transition Node"
    bl_region_type = "UI"
    bl_category = "Darkfall VFX Nodes"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'OBJECT_PT_toolseffect'
    
    

    def draw(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene
        strip = scene.render
        
        
        

        
        row = layout.row()
        
       
        

        box = layout.box()

        row = box.row()
        row.prop(obj, "expanded",
            icon="TRIA_DOWN" if obj.expanded else "TRIA_RIGHT",
            icon_only=True, emboss=False
            
)
                    
                  
        row.label(text="Transition Node Info", icon= 'ANIM_DATA')
        

        if obj.expanded:
            row = box.row()
            

            row = box.row()
        
            row = box.row()
            row.label(text=" Transition between your Original")
            row = box.row()
            row.label(text=" and Edited Video Clip.")  
            row = box.row()
            row.label(text=" You could use a Black and")
            row = box.row()
            row.label(text=" white video as a transition.")                     
            row = box.row()
            row = box.row()
            row = box.row()
        
        row = layout.row()
        
        row.prop(scene, "frame_current", text="Frame")
        row = layout.row()
        row.operator("node.transition_operator", icon= 'ANIM_DATA')
        row = layout.row()
        row.operator("rem.addnodes", icon= 'CANCEL')
        row = layout.row()
        
        
        
        
        
        
        
        row = layout.row()































#Ink drop sub8 panel
class Sub8Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "inkpanel"
    bl_idname = "OBJECT_PT_ink"
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Ink Drop Node"
    bl_region_type = "UI"
    bl_category = "Darkfall VFX Nodes"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'OBJECT_PT_artisticeffect'

    def draw(self, context):
        layout = self.layout
        obj = context.object
        
            
        

        box = layout.box()

        row = box.row()
        row.prop(obj, "expanded",
            icon="TRIA_DOWN" if obj.expanded else "TRIA_RIGHT",
            icon_only=True, emboss=False
            
)
                    
                  
        row.label(text="Ink Drop Info", icon= 'MOD_FLUIDSIM')
        

        if obj.expanded:
            row = box.row()
            

            row = box.row()
        
            row = box.row()
            row.label(text=" The Ink Drop Effect will take a")
            row = box.row()
            row.label(text=" Smoke asset and a black and white")           
            row = box.row()
            row.label(text=" Image to create this effect.") 
            row = box.row()
            row = box.row()
        
        row = layout.row()
        layout.operator(NODE_OT_inkdropgroup.bl_idname, icon= 'PMARKER_SEL')
        
        row = layout.row()
        row.operator("addition8.addnodes", icon= 'NODE_SEL')
        row.operator("rem.addnodes", icon= 'CANCEL')
        row = layout.row()
        row = layout.row()
        
        row = layout.row()
        

#patch sub3 panel
class Sub3Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "patchpanel"
    bl_idname = "OBJECT_PT_patch"
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Patch Node"
    bl_region_type = "UI"
    bl_category = "Darkfall VFX Nodes"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'OBJECT_PT_toolseffect'

    def draw(self, context):
        layout = self.layout
        obj = context.object
        
            
        

        box = layout.box()

        row = box.row()
        row.prop(obj, "expanded",
            icon="TRIA_DOWN" if obj.expanded else "TRIA_RIGHT",
            icon_only=True, emboss=False
            
)
                    
                  
        row.label(text="Patch Info", icon= 'SEQ_PREVIEW')
        

        if obj.expanded:
            row = box.row()
            

            row = box.row()
        
            row = box.row()
            row.label(text=" The Patch Node, will take a Movie,")
            row = box.row()
            row.label(text=" clip and add (or patch) it on top")
            row = box.row()
            row.label(text=" of your Background Movie clip.")            
            row = box.row()
            row = box.row()
            row = box.row()
            row.label(text=" You will Need to Mask around your,")
            row = box.row()
            row.label(text=" patch object.")
            row = box.row()
            row = box.row()
            row.label(text=" If your camera is moving, you will")
            row = box.row()
            row.label(text=" also need to Track your shot.")
            row = box.row()
           
        row = layout.row()
        layout.operator(NODE_OT_patchGroup.bl_idname, icon= 'SEQ_PREVIEW')
        
        row = layout.row()
        row.operator("addition3.addnodes", icon= 'NODE_SEL')
        row.operator("rem.addnodes", icon= 'CANCEL')
        row = layout.row()
        row = layout.row()
        
        row = layout.row()
        
        
        
#Posterize sub7 panel
class Sub7Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "postpanel"
    bl_idname = "OBJECT_PT_post"
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Posterize Node"
    bl_region_type = "UI"
    bl_category = "Darkfall VFX Nodes"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'OBJECT_PT_artisticeffect'

    def draw(self, context):
        layout = self.layout
        obj = context.object
        
            
        

        box = layout.box()

        row = box.row()
        row.prop(obj, "expanded",
            icon="TRIA_DOWN" if obj.expanded else "TRIA_RIGHT",
            icon_only=True, emboss=False
            
)
                    
                  
        row.label(text="Posterize Info", icon= 'FCURVE_SNAPSHOT')
        

        if obj.expanded:
            row = box.row()
            

            row = box.row()
        
            row = box.row()
            row.label(text=" The Posterize Effect will take a")
            row = box.row()
            row.label(text=" Movie clip and add a Posterize")   
            row = box.row()
            row.label(text=" Effect which you can modify.")          
            row = box.row()
            row = box.row()
            row.label(text=" Playing around with the Values")
            row = box.row()
            row.label(text=" and the blend mode can give many")
            row = box.row()
            row.label(text=" different variations of this effect.")
            row = box.row()
        
        layout.label(text=" Select from the presets below.")   
        row = layout.row()
        layout.operator(NODE_OT_post1group.bl_idname, icon= 'KEYTYPE_BREAKDOWN_VEC')
        layout.operator(NODE_OT_post2group.bl_idname, icon= 'KEYTYPE_MOVING_HOLD_VEC')
        layout.operator(NODE_OT_post3group.bl_idname, icon= 'KEYTYPE_JITTER_VEC')
        
        row = layout.row()
        row.operator("addition7.addnodes", icon= 'NODE_SEL')
        row.operator("rem.addnodes", icon= 'CANCEL')
        row = layout.row()
        row = layout.row()
        
        row = layout.row()






#scifi sub2 panel
class Sub2Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "scifieyepanel"
    bl_idname = "OBJECT_PT_scifieye"
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Sci-fi Eyes"
    bl_region_type = "UI"
    bl_category = "Darkfall VFX Nodes"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'OBJECT_PT_eyeeffect'
    
    
    
    def draw(self, context):
        layout = self.layout
        obj = context.object
       

        box = layout.box()
        row = box.row()
        row.prop(obj, "expanded",
            icon="TRIA_DOWN" if obj.expanded else "TRIA_RIGHT",
            icon_only=True, emboss=False
            
)
                    
                  
        row.label(text="Sci-fi Eyes Info", icon= 'HIDE_OFF')
        

        if obj.expanded:
            row = box.row()
            row = box.row()
            row.label(text=" Sci-fi Eyes, will add a Texture to")
            row = box.row()
            row.label(text=" your subject's eyes.")
            row = box.row()
            row = box.row()
            row = box.row()
            row.label(text=" You need a Mask for the Eyelids,")
            row = box.row()
            row.label(text=" an Image Texture for the Eye.")
            row = box.row()
            row.label(text=" You can download an Image from")
            row = box.row()
            row.label(text=" our blog or use one of your own.")
            row = box.row()
                    
            
        row = layout.row(align=True)
        layout.operator(NODE_OT_scifieyesGroup.bl_idname, icon= 'HIDE_OFF')
        row = layout.row()
        row.operator("addition2.addnodes", icon= 'NODE_SEL')
        row.operator("rem.addnodes", icon= 'CANCEL')
        row = layout.row()
        row = layout.row()
        row = layout.row()






#sketch sub6 panel
class Sub6Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "sketchpanel"
    bl_idname = "OBJECT_PT_sketch"
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Sketch Node"
    bl_region_type = "UI"
    bl_category = "Darkfall VFX Nodes"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'OBJECT_PT_artisticeffect'

    def draw(self, context):
        layout = self.layout
        obj = context.object
        
        box = layout.box()
        row = box.row()
        row.prop(obj, "expanded",
            icon="TRIA_DOWN" if obj.expanded else "TRIA_RIGHT",
            icon_only=True, emboss=False
            
)
                    
                  
        row.label(text="Sketch Info", icon= 'GPBRUSH_MARKER')
        

        if obj.expanded:
            row = box.row()
            row = box.row()
            row = box.row()
            row.label(text=" The Sketch Effect will take a Movie")
            row = box.row()
            row.label(text=" clip abd add a Sketch Effect which")
            row = box.row()
            row.label(text=" you can modify.")              
            row = box.row()
            row = box.row()
            row.label(text=" You can also add the Paper Color")
            row = box.row()
            row.label(text="  Presets Node, which contains")
            row = box.row()
            row.label(text=" some, Paper Color Presets.")
            row = box.row()
           
        row = layout.row()
        layout.operator(NODE_OT_sketchGroup.bl_idname, icon= 'GREASEPENCIL')
        layout.operator(NODE_OT_colpreGroup.bl_idname, icon= 'PRESET')
        row = layout.row()
        row.operator("addition6.addnodes", icon= 'NODE_SEL')
        row.operator("rem.addnodes", icon= 'CANCEL')
        row = layout.row()
        row = layout.row()
        row = layout.row()




#Vignette sub9 panel
class Sub9Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "vigpanel"
    bl_idname = "OBJECT_PT_vig"
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Vignette Node"
    bl_region_type = "UI"
    bl_category = "Darkfall VFX Nodes"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'OBJECT_PT_toolseffect'

    def draw(self, context):
        layout = self.layout
        obj = context.object

        box = layout.box()

        row = box.row()
        row.prop(obj, "expanded",
            icon="TRIA_DOWN" if obj.expanded else "TRIA_RIGHT",
            icon_only=True, emboss=False
            
)
                    
                  
        row.label(text="Vignette Info", icon= 'SURFACE_NCURVE')
        

        if obj.expanded:
            row = box.row()
            row = box.row()
            row = box.row()
            row.label(text=" Add a simple Vignette effect to")
            row = box.row()
            row.label(text=" your videos.")           
            row = box.row()
            row = box.row()
            row.label(text=" You can move and scale the Effect") 
            row = box.row()
            row.label(text=" to suit your needs.") 
            row = box.row()
        
        row = layout.row()
        layout.operator(NODE_OT_viggroup.bl_idname, icon= 'SURFACE_NCURVE')
        row = layout.row()
        row.operator("rem.addnodes", icon= 'CANCEL')
        row = layout.row()
        row = layout.row()
        row = layout.row()  





#Filmgrain sub16 panel
class Sub16Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "filmgrainpanel"
    bl_idname = "OBJECT_PT_filmgrain"
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Film Grain Node"
    bl_region_type = "UI"
    bl_category = "Darkfall VFX Nodes"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'OBJECT_PT_toolseffect'

    def draw(self, context):
        layout = self.layout
        obj = context.object

        box = layout.box()

        row = box.row()
        row.prop(obj, "expanded",
            icon="TRIA_DOWN" if obj.expanded else "TRIA_RIGHT",
            icon_only=True, emboss=False
            
)
                    
                  
        row.label(text="Film Grain Info", icon= 'SCENE')
        

        if obj.expanded:
            row = box.row()
            row = box.row()
            row = box.row()
            row.label(text=" Add some film grain to your videos.")
            row = box.row()
            row.label(text=" You can choose either the Color")           
            row = box.row()
            row = box.row()
            row.label(text=" or the black and white option,") 
            row = box.row()
            row.label(text=" to suit your needs.") 
            row = box.row()
        
        row = layout.row()
        row.operator("node.filmgrain1_operator", icon= 'KEYTYPE_MOVING_HOLD_VEC')
        row.operator("node.filmgrain2_operator", icon= 'HANDLETYPE_FREE_VEC')
        row = layout.row()
        row.operator("rem.addnodes", icon= 'CANCEL')
        row = layout.row()
        row = layout.row()
        row = layout.row()




#Marker Removal sub17 panel
class Sub17Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "markerremovalpanel"
    bl_idname = "OBJECT_PT_markerremoval"
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Marker Removal Node"
    bl_region_type = "UI"
    bl_category = "Darkfall VFX Nodes"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = 'OBJECT_PT_toolseffect'

    def draw(self, context):
        layout = self.layout
        obj = context.object

        box = layout.box()

        row = box.row()
        row.prop(obj, "expanded",
            icon="TRIA_DOWN" if obj.expanded else "TRIA_RIGHT",
            icon_only=True, emboss=False
            
)
                    
                  
        row.label(text="Marker Removal Info", icon= 'TRACKER')
        

        if obj.expanded:
            row = box.row()
            row = box.row()
            row = box.row()
            row.label(text=" We can remove Tracking Markers")
            row = box.row()
            row.label(text=" by using a mask and the Marker")           
            row = box.row()
            row.label(text=" Removal Node.") 
            row = box.row()
            
        
        row = layout.row()
        row.operator("node.markerrem_operator", icon= 'CON_FOLLOWTRACK')
        row = layout.row()
        row.operator("addition9.addnodes", icon= 'NODE_SEL')
        row.operator("rem.addnodes", icon= 'CANCEL')
        row = layout.row()
        row = layout.row()
        row = layout.row()










  


# Artistic cat sub12 panel
class Sub12Panel(bpy.types.Panel):
    bl_label = "artisticeffectpanel"
    bl_idname = "OBJECT_PT_artisticeffect"
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Artistic Effects"
    bl_region_type = "UI"
    bl_category = "Darkfall VFX Nodes"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout


# Eyes cat sub13 panel
class Sub13Panel(bpy.types.Panel):
    bl_label = "eyeeffectpanel"
    bl_idname = "OBJECT_PT_eyeeffect"
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Eye Effects"
    bl_region_type = "UI"
    bl_category = "Darkfall VFX Nodes"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout


# Tools cat sub14 panel
class Sub14Panel(bpy.types.Panel):
    bl_label = "toolseffectpanel"
    bl_idname = "OBJECT_PT_toolseffect"
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Tools"
    bl_region_type = "UI"
    bl_category = "Darkfall VFX Nodes"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout





#Render sub11 panel
class Sub11Panel(bpy.types.Panel):
    bl_label = "renpanel"
    bl_idname = "OBJECT_PT_ren"
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Render Settings"
    bl_region_type = "UI"
    bl_category = "Darkfall VFX Nodes"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        strip = context.scene.render
        scene = context.scene
        view = scene.view_settings
        image_settings = strip.image_settings

        row = layout.row()
        row = layout.row()
        row = layout.row()
        row = layout.row()
        row = layout.row()
        row.scale_y = 1.2
        row.operator("render.render", text= " Render Video", icon= 'RENDER_ANIMATION').animation = True
        row = layout.row()
        row = layout.row()
        row.scale_y = 2        
        row.label(text=" Video Resolution", icon= 'RESTRICT_VIEW_ON')
        row = layout.row(align=True)
        row.scale_y = 1.1
        row.prop(strip, "resolution_x", text="X")
        row.prop(strip, "resolution_y", text="Y")
        row = layout.row()       
        row.prop(strip, "resolution_percentage", text="")
        row = layout.row() 
        row = layout.row()
        row = layout.row()
        row.scale_y = 2   
        row.label(text=" Frames", icon= 'ARROW_LEFTRIGHT')
        row = layout.row(align=True)
        row.scale_y = 1.1
        row.prop(scene, "frame_start", text="Start")
        row.prop(scene, "frame_end", text="End")
        row = layout.row(align=True)
        row.label(text=" Frame Rate:")
        row.prop(scene.render, "fps", text="fps")
        row = layout.row()
        row = layout.row()
        row = layout.row()
        row.scale_y = 2   
        row.label(text=" Output", icon= 'FILEBROWSER')
        row = layout.row()
        layout.prop(strip, "filepath", text="Filepath")
        row = layout.row()
        layout.template_image_settings(image_settings, color_management=False)
        row = layout.row()
        row = layout.row()
        row.active = strip.is_movie_format
        row.prop(strip.ffmpeg, "format")
        row = layout.row()
        row = layout.row()
        row.label(text=" Color Management", icon= 'COLORSET_13_VEC')
        row.scale_y = 2 
        row = layout.row()
        layout.prop(view, "view_transform", expand=False)
        row = layout.row()
        row = layout.row()
        row = layout.row()
        row = layout.row()
        
        
        
        
        











        

# Register
def register():
    bpy.utils.register_class(NODE_PT_customPanel)
    bpy.utils.register_class(Sub11Panel)
    bpy.utils.register_class(Sub12Panel)
    bpy.utils.register_class(Sub13Panel)
    bpy.utils.register_class(Sub14Panel)
    
    bpy.utils.register_class(NODE_PT_active_node_properties)
    bpy.utils.register_class(NODE_OT_planarGroup)
    bpy.utils.register_class(NODE_OT_subsurfaceGroup)
    bpy.utils.register_class(NODE_OT_cloneGroup)
    bpy.utils.register_class(NODE_OT_colchangeGroup)
    bpy.utils.register_class(NODE_OT_scifieyesGroup)
    bpy.utils.register_class(NODE_OT_patchGroup)
    bpy.utils.register_class(NODE_OT_glitchGroup)
    bpy.utils.register_class(NODE_OT_transitionGroup)
    bpy.utils.register_class(NODE_OT_colpreGroup)
    bpy.utils.register_class(NODE_OT_sketchGroup)
    bpy.utils.register_class(NODE_OT_post1group)
    bpy.utils.register_class(NODE_OT_post2group)
    bpy.utils.register_class(NODE_OT_post3group)
    bpy.utils.register_class(NODE_OT_inkdropgroup)
    bpy.utils.register_class(NODE_OT_viggroup)  
    bpy.utils.register_class(RemOP)
    bpy.utils.register_class(NODE_OT_texGroupGradient)
    bpy.utils.register_class(NODE_OT_texGroupScanlines)
    bpy.utils.register_class(NODE_OT_texGroupFilmGrain)
    bpy.utils.register_class(NODE_OT_texGroupFilmGrain2)
    bpy.utils.register_class(NODE_OT_markerremGroup)
    bpy.utils.register_class(Addition1OP)
    bpy.utils.register_class(Addition2OP)
    bpy.utils.register_class(Addition3OP)
    bpy.utils.register_class(Addition4OP)
    bpy.utils.register_class(Addition5OP)
    bpy.utils.register_class(Addition6OP)
    bpy.utils.register_class(Addition7OP)
    bpy.utils.register_class(Addition8OP)
    bpy.utils.register_class(Addition9OP)
    
    
    bpy.utils.register_class(Sub4Panel)
    bpy.types.Object.expanded = bpy.props.BoolProperty(default=False)
    bpy.utils.register_class(Sub2Panel)
    bpy.types.Object.expanded = bpy.props.BoolProperty(default=False)
    
    
    bpy.utils.register_class(Sub18Panel)
    bpy.types.Object.expanded = bpy.props.BoolProperty(default=False)
    bpy.utils.register_class(Sub1Panel)
    bpy.types.Object.expanded = bpy.props.BoolProperty(default=False)
    bpy.utils.register_class(Sub16Panel)
    bpy.types.Object.expanded = bpy.props.BoolProperty(default=False)
    bpy.utils.register_class(Sub10Panel)
    bpy.utils.register_class(Sub17Panel)
    bpy.types.Object.expanded = bpy.props.BoolProperty(default=False)
    bpy.utils.register_class(Sub3Panel)
    bpy.types.Object.expanded = bpy.props.BoolProperty(default=False)
    bpy.utils.register_class(Sub15Panel)
    bpy.utils.register_class(Sub20Panel)
    bpy.utils.register_class(Sub9Panel)
    bpy.types.Object.expanded = bpy.props.BoolProperty(default=False)
    
    

    bpy.utils.register_class(Sub5Panel)
    bpy.types.Object.expanded = bpy.props.BoolProperty(default=False)
    bpy.utils.register_class(Sub8Panel)
    bpy.types.Object.expanded = bpy.props.BoolProperty(default=False)
    bpy.utils.register_class(Sub7Panel)
    bpy.types.Object.expanded = bpy.props.BoolProperty(default=False)
    bpy.utils.register_class(Sub6Panel)
    bpy.types.Object.expanded = bpy.props.BoolProperty(default=False)
    
    
    
    
    
    
    
    
    





def unregister():
    bpy.utils.unregister_class(NODE_PT_customPanel)
    bpy.utils.unregister_class(Sub11Panel)
    bpy.utils.unregister_class(Sub12Panel)
    bpy.utils.unregister_class(Sub13Panel)
    bpy.utils.unregister_class(Sub14Panel)
    bpy.utils.unregister_class(NODE_PT_active_node_properties)
    bpy.utils.unregister_class(NODE_OT_planarGroup)
    bpy.utils.unregister_class(NODE_OT_subsurfaceGroup)
    bpy.utils.unregister_class(NODE_OT_cloneGroup)
    bpy.utils.unregister_class(NODE_OT_colchangeGroup)
    bpy.utils.unregister_class(NODE_OT_scifieyesGroup)
    bpy.utils.unregister_class(NODE_OT_patchGroup)
    bpy.utils.unregister_class(NODE_OT_glitchGroup)
    bpy.utils.unregister_class(NODE_OT_transitionGroup)
    bpy.utils.unregister_class(NODE_OT_colpreGroup)
    bpy.utils.unregister_class(NODE_OT_sketchGroup)
    bpy.utils.unregister_class(NODE_OT_post1group)
    bpy.utils.unregister_class(NODE_OT_post2group)
    bpy.utils.unregister_class(NODE_OT_post3group)
    bpy.utils.unregister_class(NODE_OT_inkdropgroup)
    bpy.utils.unregister_class(NODE_OT_viggroup)
    bpy.utils.unregister_class(RemOP)
    bpy.utils.unregister_class(NODE_OT_texGroupGradient)
    bpy.utils.unregister_class(NODE_OT_texGroupScanlines)
    bpy.utils.unregister_class(NODE_OT_texGroupFilmGrain)
    bpy.utils.unregister_class(NODE_OT_texGroupFilmGrain2)
    bpy.utils.unregister_class(NODE_OT_markerremGroup)
    bpy.utils.unregister_class(Addition1OP)
    bpy.utils.unregister_class(Addition2OP)
    bpy.utils.unregister_class(Addition3OP)
    bpy.utils.unregister_class(Addition4OP)
    bpy.utils.unregister_class(Addition5OP)
    bpy.utils.unregister_class(Addition6OP)
    bpy.utils.unregister_class(Addition7OP)
    bpy.utils.unregister_class(Addition8OP)
    bpy.utils.unregister_class(Addition9OP)
    bpy.utils.unregister_class(Sub18Panel)
    del bpy.types.Object.expanded
    bpy.utils.unregister_class(Sub1Panel)
    del bpy.types.Object.expanded
    bpy.utils.unregister_class(Sub2Panel)
    del bpy.types.Object.expanded
    bpy.utils.unregister_class(Sub3Panel)
    del bpy.types.Object.expanded
    bpy.utils.unregister_class(Sub4Panel)
    del bpy.types.Object.expanded
    bpy.utils.unregister_class(Sub5Panel)
    del bpy.types.Object.expanded
    bpy.utils.unregister_class(Sub6Panel)
    del bpy.types.Object.expanded
    bpy.utils.unregister_class(Sub7Panel)
    del bpy.types.Object.expanded
    bpy.utils.unregister_class(Sub8Panel)
    del bpy.types.Object.expanded
    bpy.utils.unregister_class(Sub15Panel)
    del bpy.types.Object.expanded
    bpy.utils.unregister_class(Sub20Panel)
    bpy.utils.unregister_class(Sub9Panel)
    del bpy.types.Object.expanded
    bpy.utils.unregister_class(Sub16Panel)
    bpy.utils.unregister_class(Sub10Panel)
    del bpy.types.Object.expanded
    bpy.utils.unregister_class(Sub17Panel)
    
    
        


if __name__ == "__main__":
    register()