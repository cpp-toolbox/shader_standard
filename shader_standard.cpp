#include <unordered_map>
#include <string>
#include <glad/glad.h>
enum class ShaderType {
    CWL_V_TRANSFORMATION_WITH_SOLID_COLOR,
    CWL_V_TRANSFORMATION_WITH_TEXTURES,
    TRANSFORM_V_WITH_TEXTURES,
    CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_LIGHTING,
    CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_AND_DIFFUSE_LIGHTING,
    SKYBOX,
    ABSOLUTE_POSITION_WITH_SOLID_COLOR,
    TEXT,
    ABSOLUTE_POSITION_WITH_COLORED_VERTEX,
};

enum class ShaderVertexAttributeVariable {
    XYZ_POSITION,
    XY_POSITION,
    PASSTHROUGH_TEXTURE_COORDINATE,
    TEXTURE_COORDINATE,
    PASSTHROUGH_RGB_COLOR,
    RGB_COLOR,
    PASSTHROUGH_NORMAL,
    NORMAL,
};

enum class ShaderUniformVariable {
    // Transformations
    CAMERA_TO_CLIP,  // mat4
    WORLD_TO_CAMERA,  // mat4
    LOCAL_TO_WORLD,  // mat4
    TRANSFORM,  // mat4
    SKYBOX_TEXTURE_UNIT,  // samplerCube
    TEXT_TEXTURE_UNIT,  // sampler2D
    COLOR,  // 
    RGB_COLOR,  // vec3
    RGBA_COLOR,  // vec4
    AMBIENT_LIGHT_STRENGTH,  // float
    AMBIENT_LIGHT_COLOR,  // vec3
    DIFFUSE_LIGHT_POSITION,  // vec3
};

struct ShaderCreationInfo {
    std::string vertex_path;
    std::string fragment_path;
    std::string geometry_path;
};

struct ShaderProgramInfo {
    GLuint id;
};

struct GLVertexAttributeConfiguration {
    GLint components_per_vertex;
    GLenum data_type_of_component;
    GLboolean normalize;
    GLsizei stride;
    GLvoid *pointer_to_start_of_data;
};

const std::unordered_map<ShaderVertexAttributeVariable, GLVertexAttributeConfiguration> shader_vertex_attribute_to_glva_configuration = {
    {ShaderVertexAttributeVariable::XYZ_POSITION, {3, GL_FLOAT, GL_FALSE, 0, (void *)0}},
    {ShaderVertexAttributeVariable::XY_POSITION, {3, GL_FLOAT, GL_FALSE, 0, (void *)0}},
    {ShaderVertexAttributeVariable::PASSTHROUGH_TEXTURE_COORDINATE, {3, GL_FLOAT, GL_FALSE, 0, (void *)0}},
    {ShaderVertexAttributeVariable::TEXTURE_COORDINATE, {3, GL_FLOAT, GL_FALSE, 0, (void *)0}},
    {ShaderVertexAttributeVariable::PASSTHROUGH_RGB_COLOR, {3, GL_FLOAT, GL_FALSE, 0, (void *)0}},
    {ShaderVertexAttributeVariable::RGB_COLOR, {3, GL_FLOAT, GL_FALSE, 0, (void *)0}},
    {ShaderVertexAttributeVariable::PASSTHROUGH_NORMAL, {3, GL_FLOAT, GL_FALSE, 0, (void *)0}},
    {ShaderVertexAttributeVariable::NORMAL, {3, GL_FLOAT, GL_FALSE, 0, (void *)0}},
};

const std::unordered_map<ShaderUniformVariable, std::string> shader_uniform_variable_to_name = {
    {ShaderUniformVariable::CAMERA_TO_CLIP, "camera_to_clip"},
    {ShaderUniformVariable::WORLD_TO_CAMERA, "world_to_camera"},
    {ShaderUniformVariable::LOCAL_TO_WORLD, "local_to_world"},
    {ShaderUniformVariable::TRANSFORM, "transform"},
    {ShaderUniformVariable::SKYBOX_TEXTURE_UNIT, "skybox_texture_unit"},
    {ShaderUniformVariable::TEXT_TEXTURE_UNIT, "text_texture_unit"},
    {ShaderUniformVariable::COLOR, "color"},
    {ShaderUniformVariable::RGB_COLOR, "rgb_color"},
    {ShaderUniformVariable::RGBA_COLOR, "rgba_color"},
    {ShaderUniformVariable::AMBIENT_LIGHT_STRENGTH, "ambient_light_strength"},
    {ShaderUniformVariable::AMBIENT_LIGHT_COLOR, "ambient_light_color"},
    {ShaderUniformVariable::DIFFUSE_LIGHT_POSITION, "diffuse_light_position"},
};

std::unordered_map<ShaderType, ShaderCreationInfo> shader_catalog = {
    {ShaderType::CWL_V_TRANSFORMATION_WITH_SOLID_COLOR, {"assets/shaders/solid_color.frag", "assets/shaders/solid_color.frag"}},
    {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES, {"assets/shaders/textured.frag", "assets/shaders/textured.frag"}},
    {ShaderType::TRANSFORM_V_WITH_TEXTURES, {"assets/shaders/textured.frag", "assets/shaders/textured.frag"}},
    {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_LIGHTING, {"assets/shaders/textured_with_ambient_lighting.frag", "assets/shaders/textured_with_ambient_lighting.frag"}},
    {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_AND_DIFFUSE_LIGHTING, {"assets/shaders/textured_with_ambient_and_diffuse_lighting.frag", "assets/shaders/textured_with_ambient_and_diffuse_lighting.frag"}},
    {ShaderType::SKYBOX, {"assets/shaders/cubemap.frag", "assets/shaders/cubemap.frag"}},
    {ShaderType::ABSOLUTE_POSITION_WITH_SOLID_COLOR, {"assets/shaders/solid_color.frag", "assets/shaders/solid_color.frag"}},
    {ShaderType::TEXT, {"assets/shaders/text.frag", "assets/shaders/text.frag"}},
    {ShaderType::ABSOLUTE_POSITION_WITH_COLORED_VERTEX, {"assets/shaders/colored_vertices.frag", "assets/shaders/colored_vertices.frag"}},
};