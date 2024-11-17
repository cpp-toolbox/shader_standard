from enum import Enum, auto
from dataclasses import dataclass
from typing import List

"""
Whenever you add a new shader you need to register any new information used in here


The identifiers used for the enums here should be the same as the 
variables used for them in the shaders in lower case eg)

XYZ_POSITION -> xyz_position

"""

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

    # texture packer
    PASSTHROUGH_PACKED_TEXTURE_INDEX = auto()
    PACKED_TEXTURE_INDEX = auto()
    

class ShaderType(Enum):
    TEXTURE_PACKER_RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_WITH_TEXTURES = auto()
    RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_WITH_TEXTURES = auto()
    CWL_V_TRANSFORMATION_WITH_SOLID_COLOR = auto()
    CWL_V_TRANSFORMATION_USING_UBOS_WITH_SOLID_COLOR = auto()
    CWL_V_TRANSFORMATION_WITH_TEXTURES = auto()
    TRANSFORM_V_WITH_TEXTURES = auto()
    CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_LIGHTING = auto()
    CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_AND_DIFFUSE_LIGHTING = auto()
    SKYBOX = auto()
    ABSOLUTE_POSITION_WITH_SOLID_COLOR = auto()
    TEXT = auto()
    ABSOLUTE_POSITION_WITH_COLORED_VERTEX = auto()
    TRANSFORM_V_WITH_SIGNED_DISTANCE_FIELD_TEXT = auto()


class ShaderUniformVariable(Enum):
    # Transformations
    CAMERA_TO_CLIP = auto()
    WORLD_TO_CAMERA = auto()
    LOCAL_TO_WORLD = auto()
    TRANSFORM = auto()
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
    # Text
    CHARACTER_WIDTH = auto()      
    EDGE_TRANSITION_WIDTH = auto()
    # Animation
    ID_OF_BONE_TO_VISUALIZE  = auto() 
    BONE_ANIMATION_TRANSFORMS = auto()
    # Texture Packer
    PACKED_TEXTURES = auto()


@dataclass
class ShaderUniformVariableData:
    glsl_type: str


shader_uniform_variable_to_data = {
    ShaderUniformVariable.CAMERA_TO_CLIP: ShaderUniformVariableData("mat4"),
    ShaderUniformVariable.WORLD_TO_CAMERA: ShaderUniformVariableData("mat4"),
    ShaderUniformVariable.LOCAL_TO_WORLD: ShaderUniformVariableData("mat4"),
    ShaderUniformVariable.TRANSFORM: ShaderUniformVariableData("mat4"),
    ShaderUniformVariable.TEXTURE_SAMPLER: ShaderUniformVariableData("sampler2D"),
    ShaderUniformVariable.SKYBOX_TEXTURE_UNIT: ShaderUniformVariableData("samplerCube"),
    ShaderUniformVariable.TEXT_TEXTURE_UNIT: ShaderUniformVariableData("sampler2D"),
    ShaderUniformVariable.RGB_COLOR: ShaderUniformVariableData("vec3"),
    ShaderUniformVariable.RGBA_COLOR: ShaderUniformVariableData("vec4"),
    ShaderUniformVariable.AMBIENT_LIGHT_STRENGTH: ShaderUniformVariableData("float"),
    ShaderUniformVariable.AMBIENT_LIGHT_COLOR: ShaderUniformVariableData("vec3"),
    ShaderUniformVariable.DIFFUSE_LIGHT_POSITION: ShaderUniformVariableData("vec3"),
    ShaderUniformVariable.CHARACTER_WIDTH: ShaderUniformVariableData("float"),
    ShaderUniformVariable.EDGE_TRANSITION_WIDTH: ShaderUniformVariableData("float"),
    ShaderUniformVariable.ID_OF_BONE_TO_VISUALIZE: ShaderUniformVariableData("int"),
    # note that the below is actually an array of them, still works
    ShaderUniformVariable.BONE_ANIMATION_TRANSFORMS: ShaderUniformVariableData("mat4"), 
    ShaderUniformVariable.PACKED_TEXTURES: ShaderUniformVariableData("sampler2DArray"), 
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

# only things in the vertex shader need a binding to opengl and thus only need a configuration
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
    ShaderVertexAttributeVariable.LOCAL_TO_WORLD_INDEX: GLVertexAttributeConfiguration("1", " GL_UNSIGNED_INT", "GL_FALSE", "0", "(void *)0")
}

shader_catalog = {
    ShaderType.TEXTURE_PACKER_RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_WITH_TEXTURES : ShaderProgram(
        "texture_packer/bone_and_CWL_v_transformation_with_texture_coordinate_and_bone_data_passthrough.vert",
        "texture_packer/textured_with_single_bone_visualization.frag",
    ),
    ShaderType.RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_WITH_TEXTURES : ShaderProgram(
        "bone_and_CWL_v_transformation_with_texture_coordinate_and_bone_data_passthrough.vert",
        "textured_with_single_bone_visualization.frag",
    ),
    ShaderType.CWL_V_TRANSFORMATION_WITH_SOLID_COLOR: ShaderProgram(
        "CWL_v_transformation.vert",
        "solid_color.frag",
    ),
    ShaderType.CWL_V_TRANSFORMATION_USING_UBOS_WITH_SOLID_COLOR: ShaderProgram(
        "CWL_v_transformation_ubos.vert",
        "solid_color.frag",
    ),
    ShaderType.CWL_V_TRANSFORMATION_WITH_TEXTURES: ShaderProgram(
        "CWL_v_transformation_with_texture_coordinate_passthrough.vert",
        "textured.frag",
    ),
    ShaderType.TRANSFORM_V_WITH_TEXTURES: ShaderProgram(
        "transform_v_with_texture_coordinate_passthrough.vert",
        "textured.frag",
    ),
    ShaderType.CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_LIGHTING: ShaderProgram(
        "CWL_v_transformation_with_texture_coordinate_passthrough.vert",
        "textured_with_ambient_lighting.frag",
    ),
    ShaderType.CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_AND_DIFFUSE_LIGHTING: ShaderProgram(
        "CWL_v_transformation_with_texture_coordinate_and_normal_passthrough.vert",
        "textured_with_ambient_and_diffuse_lighting.frag",
    ),
    ShaderType.SKYBOX: ShaderProgram(
        "cubemap.vert", 
        "cubemap.frag"
    ),
    ShaderType.ABSOLUTE_POSITION_WITH_SOLID_COLOR: ShaderProgram(
        "absolute_position.vert",
        "solid_color.frag",
    ),
    ShaderType.TEXT: ShaderProgram(
        "text.vert", 
        "text.frag"
    ),
    ShaderType.ABSOLUTE_POSITION_WITH_COLORED_VERTEX: ShaderProgram(
        "colored_vertices.vert",
        "colored_vertices.frag",
    ),
    ShaderType.TRANSFORM_V_WITH_SIGNED_DISTANCE_FIELD_TEXT: ShaderProgram(
        "transform_v_with_texture_coordinate_passthrough.vert",
        "signed_distance_field_text.frag"
    )
}

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
    # Things that are not used in the vertex shader, the blanked out data is not used
    # we pass the glsl type for type verification 
    ShaderVertexAttributeVariable.LOCAL_TO_WORLD_INDEX: VertexAttributeData(
        "local_to_world_indices", "local_to_world_index", "unsigned int", "uint"
    ),
    # Things that are not used in the vertex shader
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
    # BONE_WEIGHTS = auto()
}
