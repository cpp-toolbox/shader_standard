from standard import *
shader_to_used_vertex_attribute_variables = {
    ShaderType.CWL_V_TRANSFORMATION_WITH_SOLID_COLOR: [ShaderVertexAttributeVariable.XYZ_POSITION],
    ShaderType.CWL_V_TRANSFORMATION_WITH_TEXTURES: [ShaderVertexAttributeVariable.XYZ_POSITION, ShaderVertexAttributeVariable.PASSTHROUGH_TEXTURE_COORDINATE],
    ShaderType.TRANSFORM_V_WITH_TEXTURES: [ShaderVertexAttributeVariable.XYZ_POSITION, ShaderVertexAttributeVariable.PASSTHROUGH_TEXTURE_COORDINATE],
    ShaderType.CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_LIGHTING: [ShaderVertexAttributeVariable.XYZ_POSITION, ShaderVertexAttributeVariable.PASSTHROUGH_TEXTURE_COORDINATE],
    ShaderType.CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_AND_DIFFUSE_LIGHTING: [ShaderVertexAttributeVariable.XYZ_POSITION, ShaderVertexAttributeVariable.PASSTHROUGH_NORMAL, ShaderVertexAttributeVariable.PASSTHROUGH_TEXTURE_COORDINATE],
    ShaderType.SKYBOX: [ShaderVertexAttributeVariable.XYZ_POSITION],
    ShaderType.ABSOLUTE_POSITION_WITH_SOLID_COLOR: [ShaderVertexAttributeVariable.XYZ_POSITION],
    ShaderType.TEXT: [ShaderVertexAttributeVariable.PASSTHROUGH_TEXTURE_COORDINATE, ShaderVertexAttributeVariable.XY_POSITION],
    ShaderType.ABSOLUTE_POSITION_WITH_COLORED_VERTEX: [ShaderVertexAttributeVariable.XYZ_POSITION, ShaderVertexAttributeVariable.PASSTHROUGH_RGB_COLOR],
    ShaderType.TRANSFORM_V_WITH_SIGNED_DISTANCE_FIELD_TEXT: [ShaderVertexAttributeVariable.XYZ_POSITION, ShaderVertexAttributeVariable.PASSTHROUGH_TEXTURE_COORDINATE],
}

