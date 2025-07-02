from enum import Enum, auto
from dataclasses import dataclass
from typing import List

"""
Whenever you add a new shader you need to register any new information used in here

1. add it to the ShaderType enum
2. set up the files in shader_catalog

The identifiers used for the enums here should be the same as the 
variables used for them in the shaders in lower case eg)

XYZ_POSITION -> xyz_position
"""

# from what I can tell we only need to list the vertex shader ones here
class ShaderVertexAttributeVariable(Enum):
    # vertex shader ones
    INDEX = auto()
    XYZ_POSITION = auto()
    XY_POSITION = auto()
    PASSTHROUGH_TEXTURE_COORDINATE = auto()
    PASSTHROUGH_RGB_COLOR = auto()
    PASSTHROUGH_NORMAL = auto()
    PASSTHROUGH_BONE_IDS = auto()
    PASSTHROUGH_BONE_WEIGHTS = auto()
    PASSTHROUGH_OBJECT_ID = auto()

    # fragment shader ones
    TEXTURE_COORDINATE = auto() # these are really in's into the fragment shader
    TEXTURE_COORDINATE_3D = auto() # these are really in's into the fragment shader
    RGB_COLOR = auto()
    WORLD_SPACE_POSITION = auto()
    NORMAL = auto()
    # ubos
    LOCAL_TO_WORLD_INDEX = auto()

    BONE_IDS = auto()
    BONE_WEIGHTS = auto()

    OBJECT_ID = auto()

    # texture packer
    PASSTHROUGH_PACKED_TEXTURE_INDEX = auto()
    PACKED_TEXTURE_INDEX = auto()
    PASSTHROUGH_PACKED_TEXTURE_BOUNDING_BOX_INDEX = auto()
    PACKED_TEXTURE_BOUNDING_BOX_INDEX = auto()
    

class ShaderType(Enum):
    # basic
    RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_WITH_TEXTURES = auto()
    CWL_V_TRANSFORMATION_WITH_SOLID_COLOR = auto()
    CWL_V_TRANSFORMATION_WITH_COLORED_VERTEX = auto()
    CW_V_TRANSFORMATION_WITH_COLORED_VERTEX = auto()

    CWL_V_TRANSFORMATION_UBOS_1024_WITH_SOLID_COLOR = auto()
    CWL_V_TRANSFORMATION_UBOS_1024_WITH_COLORED_VERTEX = auto()
    CWL_V_TRANSFORMATION_UBOS_1024_WITH_OBJECT_ID = auto()

    CWL_V_TRANSFORMATION_WITH_TEXTURES = auto()
    TRANSFORM_V_WITH_TEXTURES = auto()
    CWL_V_TRANSFORMATION_WITH_OBJECT_ID = auto()

    CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_LIGHTING = auto()
    CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_AND_DIFFUSE_LIGHTING = auto()

    SKYBOX = auto()
    TEXT = auto()
    # these are actual 2d shaders and I should rename this in the future
    ABSOLUTE_POSITION_WITH_SOLID_COLOR = auto()
    ABSOLUTE_POSITION_WITH_COLORED_VERTEX = auto()
    ABSOLUTE_POSITION_TEXTURED = auto()
    TRANSFORM_V_WITH_SIGNED_DISTANCE_FIELD_TEXT = auto()
    ABSOLUTE_POSITION_WITH_SIGNED_DISTANCE_FIELD_TEXT = auto()

    # deferred lighting
    CWL_V_TRANSFORMATION_UBOS_1024_WITH_COLORED_VERTEX_DEFERED_LIGHTING_FRAMEBUFFERS = auto()
    DEFERRED_LIGHTING = auto()

    # texture packer
    CWL_V_TRANSFORMATION_TEXTURE_PACKED = auto()
    TEXTURE_PACKER_RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_WITH_TEXTURES = auto()
    TEXTURE_PACKER_RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_UBOS_1024_WITH_TEXTURES_AND_MULTIPLE_LIGHTS = auto()
    TEXTURE_PACKER_RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_UBOS_1024_WITH_TEXTURES = auto()
    TEXTURE_PACKER_RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_UBOS_4096_WITH_TEXTURES_AND_MULTIPLE_LIGHTS = auto()
    TEXTURE_PACKER_CWL_V_TRANSFORMATION_UBOS_1024 = auto()
    TEXTURE_PACKER_CWL_V_TRANSFORMATION_UBOS_1024_AMBIENT_AND_DIFFUSE_LIGHTING = auto()
    TEXTURE_PACKER_CWL_V_TRANSFORMATION_UBOS_1024_MULTIPLE_LIGHTS = auto()


class ShaderUniformVariable(Enum):
    # Transformations
    CAMERA_TO_CLIP = auto()
    WORLD_TO_CAMERA = auto()
    LOCAL_TO_WORLD = auto()
    TRANSFORM = auto()
    ASPECT_RATIO = auto()
    # Textures
    TEXTURE_SAMPLER = auto()
    SKYBOX_TEXTURE_UNIT = auto()
    TEXT_TEXTURE_UNIT = auto()
    COLOR = auto()
    RGB_COLOR = auto()
    RGBA_COLOR = auto()

    # Lighting

    AMBIENT_LIGHT_STRENGTH = auto()
    AMBIENT_LIGHT_COLOR = auto()
    DIFFUSE_LIGHT_POSITION = auto()

    # - deferred
    POSITION_TEXTURE = auto()
    NORMAL_TEXTURE = auto()
    COLOR_TEXTURE = auto()


    # Multiple Lights

    CAMERA_POSITION = auto()
    DIR_LIGHT = auto()
    POINT_LIGHTS = auto()
    SPOT_LIGHT = auto()

    # spotlight
    SPOTLIGHT_STRUCT_POSITION = auto()
    SPOTLIGHT_STRUCT_DIRECTION = auto()
    SPOTLIGHT_STRUCT_CUTOFF = auto()
    SPOTLIGHT_STRUCT_OUTER_CUTOFF = auto()
    SPOTLIGHT_STRUCT_CONSTANT = auto()
    SPOTLIGHT_STRUCT_LINEAR = auto()
    SPOTLIGHT_STRUCT_QUADRATIC = auto()
    SPOTLIGHT_STRUCT_AMBIENT = auto()
    SPOTLIGHT_STRUCT_DIFFUSE = auto()
    SPOTLIGHT_STRUCT_SPECULAR = auto()

    # pointlight
    POINTLIGHT_STRUCT_POSITION = auto()
    POINTLIGHT_STRUCT_CONSTANT = auto()
    POINTLIGHT_STRUCT_LINEAR = auto()
    POINTLIGHT_STRUCT_QUADRATIC = auto()
    POINTLIGHT_STRUCT_AMBIENT = auto()
    POINTLIGHT_STRUCT_DIFFUSE = auto()
    POINTLIGHT_STRUCT_SPECULAR = auto()

    # directional light
    DIRLIGHT_STRUCT_DIRECTION = auto()
    DIRLIGHT_STRUCT_CONSTANT = auto()
    DIRLIGHT_STRUCT_LINEAR = auto()
    DIRLIGHT_STRUCT_QUADRATIC = auto()
    DIRLIGHT_STRUCT_AMBIENT = auto()
    DIRLIGHT_STRUCT_DIFFUSE = auto()
    DIRLIGHT_STRUCT_SPECULAR = auto()

    # Text
    CHARACTER_WIDTH = auto()
    EDGE_TRANSITION_WIDTH = auto()
    # Animation
    ID_OF_BONE_TO_VISUALIZE  = auto() 
    BONE_ANIMATION_TRANSFORMS = auto()
    # Texture Packer
    PACKED_TEXTURES = auto()
    PACKED_TEXTURE_BOUNDING_BOXES = auto()


@dataclass
class ShaderUniformVariableData:
    glsl_type: str


shader_uniform_variable_to_data = {
    ShaderUniformVariable.CAMERA_TO_CLIP: ShaderUniformVariableData("mat4"),
    ShaderUniformVariable.WORLD_TO_CAMERA: ShaderUniformVariableData("mat4"),
    ShaderUniformVariable.LOCAL_TO_WORLD: ShaderUniformVariableData("mat4"),
    ShaderUniformVariable.TRANSFORM: ShaderUniformVariableData("mat4"),
    ShaderUniformVariable.ASPECT_RATIO: ShaderUniformVariableData("vec2"),
    ShaderUniformVariable.TEXTURE_SAMPLER: ShaderUniformVariableData("sampler2D"),
    ShaderUniformVariable.SKYBOX_TEXTURE_UNIT: ShaderUniformVariableData("samplerCube"),
    ShaderUniformVariable.TEXT_TEXTURE_UNIT: ShaderUniformVariableData("sampler2D"),
    ShaderUniformVariable.RGB_COLOR: ShaderUniformVariableData("vec3"),
    ShaderUniformVariable.RGB_COLOR: ShaderUniformVariableData("vec3"),
    ShaderUniformVariable.RGBA_COLOR: ShaderUniformVariableData("vec4"),


    ShaderUniformVariable.POSITION_TEXTURE: ShaderUniformVariableData("sampler2D"),
    ShaderUniformVariable.NORMAL_TEXTURE: ShaderUniformVariableData("sampler2D"),
    ShaderUniformVariable.COLOR_TEXTURE : ShaderUniformVariableData("sampler2D"),


    ShaderUniformVariable.AMBIENT_LIGHT_STRENGTH: ShaderUniformVariableData("float"),
    ShaderUniformVariable.AMBIENT_LIGHT_COLOR: ShaderUniformVariableData("vec3"),
    ShaderUniformVariable.DIFFUSE_LIGHT_POSITION: ShaderUniformVariableData("vec3"),
    ShaderUniformVariable.CHARACTER_WIDTH: ShaderUniformVariableData("float"),
    ShaderUniformVariable.EDGE_TRANSITION_WIDTH: ShaderUniformVariableData("float"),
    ShaderUniformVariable.ID_OF_BONE_TO_VISUALIZE: ShaderUniformVariableData("int"),
    # note that the below is actually an array of them, still works
    ShaderUniformVariable.BONE_ANIMATION_TRANSFORMS: ShaderUniformVariableData("mat4"), 
    ShaderUniformVariable.PACKED_TEXTURES: ShaderUniformVariableData("sampler2DArray"), 

    # this is actually an array
    # ShaderUniformVariable.PACKED_TEXTURE_BOUNDING_BOXES: ShaderUniformVariableData("vec4"),  
    ShaderUniformVariable.PACKED_TEXTURE_BOUNDING_BOXES: ShaderUniformVariableData("sampler1D"),  

    # lighting
    ShaderUniformVariable.CAMERA_POSITION: ShaderUniformVariableData("vec3"),
    ShaderUniformVariable.DIR_LIGHT: ShaderUniformVariableData("DirLight"),
    ShaderUniformVariable.POINT_LIGHTS: ShaderUniformVariableData("PointLight"),
    ShaderUniformVariable.SPOT_LIGHT: ShaderUniformVariableData("SpotLight"),

    # spotlight
    ShaderUniformVariable.SPOTLIGHT_STRUCT_POSITION: ShaderUniformVariableData("vec3"),
    ShaderUniformVariable.SPOTLIGHT_STRUCT_DIRECTION: ShaderUniformVariableData("vec3"),
    ShaderUniformVariable.SPOTLIGHT_STRUCT_CUTOFF: ShaderUniformVariableData("float"),
    ShaderUniformVariable.SPOTLIGHT_STRUCT_OUTER_CUTOFF: ShaderUniformVariableData("float"),
    ShaderUniformVariable.SPOTLIGHT_STRUCT_CONSTANT: ShaderUniformVariableData("float"),
    ShaderUniformVariable.SPOTLIGHT_STRUCT_LINEAR: ShaderUniformVariableData("float"),
    ShaderUniformVariable.SPOTLIGHT_STRUCT_QUADRATIC: ShaderUniformVariableData("float"),
    ShaderUniformVariable.SPOTLIGHT_STRUCT_AMBIENT: ShaderUniformVariableData("vec3"),
    ShaderUniformVariable.SPOTLIGHT_STRUCT_DIFFUSE: ShaderUniformVariableData("vec3"),
    ShaderUniformVariable.SPOTLIGHT_STRUCT_SPECULAR: ShaderUniformVariableData("vec3"),

    # pointlight
    ShaderUniformVariable.POINTLIGHT_STRUCT_POSITION: ShaderUniformVariableData("vec3"),
    ShaderUniformVariable.POINTLIGHT_STRUCT_CONSTANT: ShaderUniformVariableData("float"),
    ShaderUniformVariable.POINTLIGHT_STRUCT_LINEAR: ShaderUniformVariableData("float"),
    ShaderUniformVariable.POINTLIGHT_STRUCT_QUADRATIC: ShaderUniformVariableData("float"),
    ShaderUniformVariable.POINTLIGHT_STRUCT_AMBIENT: ShaderUniformVariableData("vec3"),
    ShaderUniformVariable.POINTLIGHT_STRUCT_DIFFUSE: ShaderUniformVariableData("vec3"),
    ShaderUniformVariable.POINTLIGHT_STRUCT_SPECULAR: ShaderUniformVariableData("vec3"),

    # directional light
    ShaderUniformVariable.DIRLIGHT_STRUCT_DIRECTION: ShaderUniformVariableData("vec3"),
    ShaderUniformVariable.DIRLIGHT_STRUCT_CONSTANT: ShaderUniformVariableData("float"),
    ShaderUniformVariable.DIRLIGHT_STRUCT_LINEAR: ShaderUniformVariableData("float"),
    ShaderUniformVariable.DIRLIGHT_STRUCT_QUADRATIC: ShaderUniformVariableData("float"),
    ShaderUniformVariable.DIRLIGHT_STRUCT_AMBIENT: ShaderUniformVariableData("vec3"),
    ShaderUniformVariable.DIRLIGHT_STRUCT_DIFFUSE: ShaderUniformVariableData("vec3"),
    ShaderUniformVariable.DIRLIGHT_STRUCT_SPECULAR: ShaderUniformVariableData("vec3"),

}


@dataclass
class ShaderProgram:
    vertex_shader_filename: str
    fragment_shader_filename: str


@dataclass
class VertexAttributeData:
    singular_name: str
    plural_name: str
    attrib_type: str
    glsl_type: str


@dataclass
class GLVertexAttributeConfiguration:
    components_per_vertex: str
    data_type_of_component: str
    normalize: str
    stride: str
    pointer_to_start_of_data: str


# NOTE: only things in the vertex shader need a binding to opengl and thus only need a configuration
vertex_attribute_to_configuration = {
    ShaderVertexAttributeVariable.XYZ_POSITION: GLVertexAttributeConfiguration("3", "GL_FLOAT", "GL_FALSE", "0", "(void *)0"),
    ShaderVertexAttributeVariable.XY_POSITION: GLVertexAttributeConfiguration("2", "GL_FLOAT", "GL_FALSE", "0", "(void *)0"),
    ShaderVertexAttributeVariable.PASSTHROUGH_NORMAL: GLVertexAttributeConfiguration("3", "GL_FLOAT", "GL_FALSE", "0", "(void *)0"),
    ShaderVertexAttributeVariable.PASSTHROUGH_TEXTURE_COORDINATE: GLVertexAttributeConfiguration("2", "GL_FLOAT", "GL_FALSE", "0", "(void *)0"),
    ShaderVertexAttributeVariable.PASSTHROUGH_RGB_COLOR: GLVertexAttributeConfiguration("3", "GL_FLOAT", "GL_FALSE", "0", "(void *)0"),
    ShaderVertexAttributeVariable.PASSTHROUGH_NORMAL: GLVertexAttributeConfiguration("3", "GL_FLOAT", "GL_FALSE", "0", "(void *)0"),
    # note that here we only allow for 4 bone ids per vertex, this is an arbitrary choice.
    ShaderVertexAttributeVariable.PASSTHROUGH_BONE_IDS: GLVertexAttributeConfiguration("4", "GL_INT", "GL_FALSE", "0", "(void *)0"),
    ShaderVertexAttributeVariable.PASSTHROUGH_BONE_WEIGHTS: GLVertexAttributeConfiguration("4", "GL_FLOAT", "GL_FALSE", "0", "(void *)0"),
    ShaderVertexAttributeVariable.PASSTHROUGH_PACKED_TEXTURE_INDEX: GLVertexAttributeConfiguration("1", "GL_INT", "GL_FALSE", "0", "(void *)0"),
    ShaderVertexAttributeVariable.PASSTHROUGH_PACKED_TEXTURE_BOUNDING_BOX_INDEX: GLVertexAttributeConfiguration("1", "GL_INT", "GL_FALSE", "0", "(void *)0"),
    ShaderVertexAttributeVariable.LOCAL_TO_WORLD_INDEX: GLVertexAttributeConfiguration("1", " GL_UNSIGNED_INT", "GL_FALSE", "0", "(void *)0"),
    ShaderVertexAttributeVariable.PASSTHROUGH_OBJECT_ID: GLVertexAttributeConfiguration("1", " GL_UNSIGNED_INT", "GL_FALSE", "0", "(void *)0")
}

shader_catalog = {
    ShaderType.TEXTURE_PACKER_RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_UBOS_1024_WITH_TEXTURES_AND_MULTIPLE_LIGHTS : ShaderProgram("out/texture_packer/bone_and_CWL_v_transformation_ubos_1024_with_lighting_data_passthrough.vert", "out/texture_packer/textured_with_multiple_lights.frag"),
    ShaderType.TEXTURE_PACKER_RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_UBOS_1024_WITH_TEXTURES : ShaderProgram("out/texture_packer/bone_and_CWL_v_transformation_ubos_1024.vert", "out/texture_packer/textured.frag"),
    ShaderType.TEXTURE_PACKER_RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_UBOS_4096_WITH_TEXTURES_AND_MULTIPLE_LIGHTS : ShaderProgram("out/texture_packer/bone_and_CWL_v_transformation_ubos_4096_with_lighting_data_passthrough.vert", "out/texture_packer/textured_with_multiple_lights.frag"),
    ShaderType.CWL_V_TRANSFORMATION_TEXTURE_PACKED : ShaderProgram(
        "out/texture_packer/CWL_v_transformation_texture_packed_passthrough.vert",
        "out/texture_packer/textured.frag",
    ),
    ShaderType.TEXTURE_PACKER_RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_WITH_TEXTURES : ShaderProgram(
        "out/texture_packer/bone_and_CWL_v_transformation_with_texture_coordinate_and_bone_data_passthrough.vert",
        "out/texture_packer/textured_with_single_bone_visualization.frag",
    ),
    ShaderType.TEXTURE_PACKER_CWL_V_TRANSFORMATION_UBOS_1024_AMBIENT_AND_DIFFUSE_LIGHTING  : ShaderProgram(
        "out/texture_packer/CWL_v_transformation_with_texture_coordinate_and_normal_passthrough.vert",
        "out/texture_packer/textured_with_ambient_and_diffuse_lighting.frag",
    ),
    ShaderType.TEXTURE_PACKER_CWL_V_TRANSFORMATION_UBOS_1024_MULTIPLE_LIGHTS  : ShaderProgram(
        "out/texture_packer/CWL_v_transformation_with_texture_coordinate_and_normal_passthrough.vert",
        "out/texture_packer/textured_with_multiple_lights.frag",
    ),
    ShaderType.TEXTURE_PACKER_CWL_V_TRANSFORMATION_UBOS_1024 : ShaderProgram(
        "out/texture_packer/CWL_v_transformation_ubos_1024.vert",
        "out/texture_packer/textured.frag",
    ),
    ShaderType.RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_WITH_TEXTURES : ShaderProgram(
        "out/bone_and_CWL_v_transformation_with_texture_coordinate_and_bone_data_passthrough.vert",
        "out/textured_with_single_bone_visualization.frag",
    ),
    ShaderType.CWL_V_TRANSFORMATION_WITH_SOLID_COLOR: ShaderProgram(
        "out/CWL_v_transformation.vert",
        "out/solid_color.frag",
    ),
    ShaderType.CWL_V_TRANSFORMATION_WITH_COLORED_VERTEX: ShaderProgram(
        "out/CWL_v_transformation_with_colored_vertices.vert",
        "out/colored_vertices.frag",
    ),
    ShaderType.CW_V_TRANSFORMATION_WITH_COLORED_VERTEX: ShaderProgram(
        "out/CW_v_transformation_with_colored_vertices.vert",
        "out/colored_vertices.frag",
    ),
    ShaderType.CWL_V_TRANSFORMATION_UBOS_1024_WITH_SOLID_COLOR: ShaderProgram(
        "out/CWL_v_transformation_ubos.vert",
        "out/solid_color.frag",
    ),
    ShaderType.CWL_V_TRANSFORMATION_UBOS_1024_WITH_COLORED_VERTEX: ShaderProgram(
        "out/CWL_v_transformation_ubos_1024_with_colored_vertex.vert",
        "out/colored_vertices.frag",
    ),
    ShaderType.CWL_V_TRANSFORMATION_UBOS_1024_WITH_COLORED_VERTEX_DEFERED_LIGHTING_FRAMEBUFFERS : ShaderProgram(
        "out/lighting/CWL_v_ubos_1024_colors_and_normals.vert",
        "out/lighting/deferred/position_normal_color.frag",
    ),
    ShaderType.DEFERRED_LIGHTING : ShaderProgram(
        "out/absolute_position_textured.vert",
        "out/lighting/deferred/deferred_lighting.frag",
    ),
    ShaderType.CWL_V_TRANSFORMATION_UBOS_1024_WITH_OBJECT_ID: ShaderProgram(
        "out/CWL_v_transformation_ubos_1024_with_object_id_passthrough.vert",
        "out/object_id.frag",
    ),
    ShaderType.CWL_V_TRANSFORMATION_WITH_TEXTURES: ShaderProgram(
        "out/CWL_v_transformation_with_texture_coordinate_passthrough.vert",
        "out/textured.frag",
    ),
    ShaderType.TRANSFORM_V_WITH_TEXTURES: ShaderProgram(
        "out/transform_v_with_texture_coordinate_passthrough.vert",
        "out/textured.frag",
    ),
    ShaderType.CWL_V_TRANSFORMATION_WITH_OBJECT_ID: ShaderProgram(
        "out/CWL_v_transformation_with_object_id_passthrough.vert",
        "out/object_id.frag",
    ),
    ShaderType.CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_LIGHTING: ShaderProgram(
        "out/CWL_v_transformation_with_texture_coordinate_passthrough.vert",
        "out/textured_with_ambient_lighting.frag",
    ),
    ShaderType.CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_AND_DIFFUSE_LIGHTING: ShaderProgram(
        "out/CWL_v_transformation_with_texture_coordinate_and_normal_passthrough.vert",
        "out/textured_with_ambient_and_diffuse_lighting.frag",
    ),
    ShaderType.SKYBOX: ShaderProgram(
        "out/cubemap.vert", 
        "out/cubemap.frag"
    ),
    ShaderType.ABSOLUTE_POSITION_WITH_SOLID_COLOR: ShaderProgram(
        "out/absolute_position.vert",
        "out/solid_color.frag",
    ),
    ShaderType.TEXT: ShaderProgram(
        "out/text.vert", 
        "out/text.frag"
    ),
    ShaderType.ABSOLUTE_POSITION_WITH_COLORED_VERTEX: ShaderProgram(
        "out/colored_vertices.vert",
        "out/colored_vertices.frag",
    ),
    ShaderType.ABSOLUTE_POSITION_TEXTURED: ShaderProgram(
        "out/absolute_position_textured.vert",
        "out/textured.frag",
    ),
    ShaderType.TRANSFORM_V_WITH_SIGNED_DISTANCE_FIELD_TEXT: ShaderProgram(
        "out/transform_v_with_texture_coordinate_passthrough.vert",
        "out/signed_distance_field_text.frag"
    ),
    ShaderType.ABSOLUTE_POSITION_WITH_SIGNED_DISTANCE_FIELD_TEXT: ShaderProgram(
        "out/absolute_position_textured.vert",
        "out/signed_distance_field_text.frag"
    )
}


# NOTE: this information is used for variables in the batcher
shader_vertex_attribute_to_data = {
    # note that index is never going to be in a GLSL program so we don't specify the glsl type
    ShaderVertexAttributeVariable.INDEX: VertexAttributeData(
        "index", "indices", "unsigned int", ""
    ),
    ShaderVertexAttributeVariable.XYZ_POSITION: VertexAttributeData(
        "position", "positions", "glm::vec3", "vec3"
    ),
    ShaderVertexAttributeVariable.XY_POSITION: VertexAttributeData(
        "xy_position", "xy_positions", "glm::vec2", "vec2"
    ),
    ShaderVertexAttributeVariable.PASSTHROUGH_TEXTURE_COORDINATE: VertexAttributeData(
        "texture_coordinate", "texture_coordinates", "glm::vec2", "vec2"
    ),
    ShaderVertexAttributeVariable.TEXTURE_COORDINATE: VertexAttributeData(
        "texture_coordinate", "texture_coordinates", "glm::vec2", "vec2"
    ),
    ShaderVertexAttributeVariable.PASSTHROUGH_TEXTURE_COORDINATE: VertexAttributeData(
        "texture_coordinate", "texture_coordinates", "glm::vec2", "vec2"
    ),
    ShaderVertexAttributeVariable.PASSTHROUGH_NORMAL: VertexAttributeData(
        "normal", "normals", "glm::vec3", "vec3"
    ),
    ShaderVertexAttributeVariable.PASSTHROUGH_RGB_COLOR: VertexAttributeData(
        "rgb_color", "rgb_colors", "glm::vec3", "vec3"
    ),
    ShaderVertexAttributeVariable.RGB_COLOR: VertexAttributeData(
        "rgb_color", "rgb_colors", "glm::vec3", "vec3"
    ),
    ShaderVertexAttributeVariable.RGB_COLOR: VertexAttributeData(
        "rgb_color", "rgb_colors", "glm::vec3", "vec3"
    ),
    # all the bone stuff is 4 because we only allow 4 bones to inflience a vertex
    ShaderVertexAttributeVariable.PASSTHROUGH_BONE_IDS : VertexAttributeData(
        "bone_id", "bone_ids", "glm::ivec4", "ivec4"
    ),
    ShaderVertexAttributeVariable.PASSTHROUGH_BONE_WEIGHTS : VertexAttributeData(
        "bone_weight", "bone_weights", "glm::vec4", "vec4"
    ),
    ShaderVertexAttributeVariable.PASSTHROUGH_PACKED_TEXTURE_INDEX : VertexAttributeData(
        "packed_texture_index", "packed_texture_indices", "int", "int"
    ),
    ShaderVertexAttributeVariable.PASSTHROUGH_PACKED_TEXTURE_BOUNDING_BOX_INDEX : VertexAttributeData(
        "packed_texture_bounding_box_index", "packed_texture_bounding_box_indices", "int", "int"
    ),
    ShaderVertexAttributeVariable.PASSTHROUGH_OBJECT_ID: VertexAttributeData(
        "object_id", "object_ids", "unsigned int", "uint"
    ),
    # Things that are not used in the vertex shader, the blanked out data is not used
    # we pass the glsl type for type verification 
    ShaderVertexAttributeVariable.LOCAL_TO_WORLD_INDEX: VertexAttributeData(
        "local_to_world_indices", "local_to_world_index", "unsigned int", "uint"
    ),
    # NOTE: we are registering these varaibles here because these are usually the varaibles
    # that get passed the data from a passthrough and are only in the fragment shader
    # since they don't require a direct connection to opengl we may omit everying except the
    # glsl type which allows for verification in the standard
    ShaderVertexAttributeVariable.OBJECT_ID: VertexAttributeData(
        "", "", "", "uint"
    ),
    ShaderVertexAttributeVariable.NORMAL: VertexAttributeData(
        "", "", "", "vec3"
    ),
    ShaderVertexAttributeVariable.WORLD_SPACE_POSITION: VertexAttributeData(
        "", "", "", "vec3"
    ),

    ShaderVertexAttributeVariable.TEXTURE_COORDINATE_3D: VertexAttributeData(
        "", "", "", "vec3"
    ),
    ShaderVertexAttributeVariable.BONE_IDS : VertexAttributeData(
        "", "", "", "ivec4"
    ),
    ShaderVertexAttributeVariable.BONE_WEIGHTS : VertexAttributeData(
        "", "", "", "vec4"
    ),
    ShaderVertexAttributeVariable.PACKED_TEXTURE_INDEX : VertexAttributeData(
        "", "", "", "int"
    ),
    ShaderVertexAttributeVariable.PACKED_TEXTURE_BOUNDING_BOX_INDEX : VertexAttributeData(
        "", "", "", "int"
    ),
    # BONE_WEIGHTS = auto()
}
