#ifndef SHADER_STANDARD_HPP
#define SHADER_STANDARD_HPP
#include <unordered_map>
#include <string>
#include <vector>
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
    PASSTHROUGH_RGB_COLOR,
    PASSTHROUGH_NORMAL,
    TEXTURE_COORDINATE,
    TEXTURE_COORDINATE_3D,
    RGB_COLOR,
    WORLD_SPACE_POSITION,
    NORMAL,
};

enum class ShaderUniformVariable {
    CAMERA_TO_CLIP,
    WORLD_TO_CAMERA,
    LOCAL_TO_WORLD,
    TRANSFORM,
    TEXTURE_SAMPLER,
    SKYBOX_TEXTURE_UNIT,
    TEXT_TEXTURE_UNIT,
    COLOR,
    RGB_COLOR,
    RGBA_COLOR,
    AMBIENT_LIGHT_STRENGTH,
    AMBIENT_LIGHT_COLOR,
    DIFFUSE_LIGHT_POSITION,
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

class ShaderStandard {
public:
    std::unordered_map<ShaderVertexAttributeVariable, GLVertexAttributeConfiguration> shader_vertex_attribute_to_glva_configuration;
    std::unordered_map<ShaderUniformVariable, std::string> shader_uniform_variable_to_name;
    std::unordered_map<ShaderVertexAttributeVariable, std::string> shader_vertex_attribute_variable_to_name;
    std::unordered_map<ShaderType, std::string> shader_type_to_name;
    std::unordered_map<ShaderType, ShaderCreationInfo> shader_catalog;
    std::unordered_map<ShaderType, std::vector<ShaderVertexAttributeVariable>> shader_to_used_vertex_attribute_variables;
    std::unordered_map<ShaderType, std::vector<ShaderUniformVariable>> shader_to_used_uniform_variable;

    ShaderStandard() {
        shader_vertex_attribute_to_glva_configuration = {
            {ShaderVertexAttributeVariable::XYZ_POSITION, GLVertexAttributeConfiguration{3, GL_FLOAT, GL_FALSE, 0, (void *)0}},
            {ShaderVertexAttributeVariable::XY_POSITION, GLVertexAttributeConfiguration{2, GL_FLOAT, GL_FALSE, 0, (void *)0}},
            {ShaderVertexAttributeVariable::PASSTHROUGH_NORMAL, GLVertexAttributeConfiguration{3, GL_FLOAT, GL_FALSE, 0, (void *)0}},
            {ShaderVertexAttributeVariable::PASSTHROUGH_TEXTURE_COORDINATE, GLVertexAttributeConfiguration{2, GL_FLOAT, GL_FALSE, 0, (void *)0}},
            {ShaderVertexAttributeVariable::PASSTHROUGH_RGB_COLOR, GLVertexAttributeConfiguration{3, GL_FLOAT, GL_FALSE, 0, (void *)0}},
        };
        shader_uniform_variable_to_name = {
            {ShaderUniformVariable::CAMERA_TO_CLIP, "camera_to_clip"},
            {ShaderUniformVariable::WORLD_TO_CAMERA, "world_to_camera"},
            {ShaderUniformVariable::LOCAL_TO_WORLD, "local_to_world"},
            {ShaderUniformVariable::TRANSFORM, "transform"},
            {ShaderUniformVariable::TEXTURE_SAMPLER, "texture_sampler"},
            {ShaderUniformVariable::SKYBOX_TEXTURE_UNIT, "skybox_texture_unit"},
            {ShaderUniformVariable::TEXT_TEXTURE_UNIT, "text_texture_unit"},
            {ShaderUniformVariable::COLOR, "color"},
            {ShaderUniformVariable::RGB_COLOR, "rgb_color"},
            {ShaderUniformVariable::RGBA_COLOR, "rgba_color"},
            {ShaderUniformVariable::AMBIENT_LIGHT_STRENGTH, "ambient_light_strength"},
            {ShaderUniformVariable::AMBIENT_LIGHT_COLOR, "ambient_light_color"},
            {ShaderUniformVariable::DIFFUSE_LIGHT_POSITION, "diffuse_light_position"},
        };
        shader_vertex_attribute_variable_to_name = {
            {ShaderVertexAttributeVariable::XYZ_POSITION, "xyz_position"},
            {ShaderVertexAttributeVariable::XY_POSITION, "xy_position"},
            {ShaderVertexAttributeVariable::PASSTHROUGH_TEXTURE_COORDINATE, "passthrough_texture_coordinate"},
            {ShaderVertexAttributeVariable::PASSTHROUGH_RGB_COLOR, "passthrough_rgb_color"},
            {ShaderVertexAttributeVariable::PASSTHROUGH_NORMAL, "passthrough_normal"},
        };
        shader_type_to_name = {
            {ShaderType::CWL_V_TRANSFORMATION_WITH_SOLID_COLOR, "cwl_v_transformation_with_solid_color"},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES, "cwl_v_transformation_with_textures"},
            {ShaderType::TRANSFORM_V_WITH_TEXTURES, "transform_v_with_textures"},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_LIGHTING, "cwl_v_transformation_with_textures_ambient_lighting"},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_AND_DIFFUSE_LIGHTING, "cwl_v_transformation_with_textures_ambient_and_diffuse_lighting"},
            {ShaderType::SKYBOX, "skybox"},
            {ShaderType::ABSOLUTE_POSITION_WITH_SOLID_COLOR, "absolute_position_with_solid_color"},
            {ShaderType::TEXT, "text"},
            {ShaderType::ABSOLUTE_POSITION_WITH_COLORED_VERTEX, "absolute_position_with_colored_vertex"},
        };
        shader_catalog = {
            {ShaderType::CWL_V_TRANSFORMATION_WITH_SOLID_COLOR, {"assets/shaders/CWL_v_transformation.vert", "assets/shaders/solid_color.frag"}},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES, {"assets/shaders/CWL_v_transformation_with_texture_coordinate_passthrough.vert", "assets/shaders/textured.frag"}},
            {ShaderType::TRANSFORM_V_WITH_TEXTURES, {"assets/shaders/transform_v_with_texture_coordinate_passthrough.vert", "assets/shaders/textured.frag"}},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_LIGHTING, {"assets/shaders/CWL_v_transformation_with_texture_coordinate_passthrough.vert", "assets/shaders/textured_with_ambient_lighting.frag"}},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_AND_DIFFUSE_LIGHTING, {"assets/shaders/CWL_v_transformation_with_texture_coordinate_and_normal_passthrough.vert", "assets/shaders/textured_with_ambient_and_diffuse_lighting.frag"}},
            {ShaderType::SKYBOX, {"assets/shaders/cubemap.vert", "assets/shaders/cubemap.frag"}},
            {ShaderType::ABSOLUTE_POSITION_WITH_SOLID_COLOR, {"assets/shaders/absolute_position.vert", "assets/shaders/solid_color.frag"}},
            {ShaderType::TEXT, {"assets/shaders/text.vert", "assets/shaders/text.frag"}},
            {ShaderType::ABSOLUTE_POSITION_WITH_COLORED_VERTEX, {"assets/shaders/colored_vertices.vert", "assets/shaders/colored_vertices.frag"}},
        };
        shader_to_used_vertex_attribute_variables = {
            {ShaderType::CWL_V_TRANSFORMATION_WITH_SOLID_COLOR, {ShaderVertexAttributeVariable::XYZ_POSITION}},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES, {ShaderVertexAttributeVariable::XYZ_POSITION, ShaderVertexAttributeVariable::PASSTHROUGH_TEXTURE_COORDINATE}},
            {ShaderType::TRANSFORM_V_WITH_TEXTURES, {ShaderVertexAttributeVariable::XYZ_POSITION, ShaderVertexAttributeVariable::PASSTHROUGH_TEXTURE_COORDINATE}},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_LIGHTING, {ShaderVertexAttributeVariable::XYZ_POSITION, ShaderVertexAttributeVariable::PASSTHROUGH_TEXTURE_COORDINATE}},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_AND_DIFFUSE_LIGHTING, {ShaderVertexAttributeVariable::XYZ_POSITION, ShaderVertexAttributeVariable::PASSTHROUGH_NORMAL, ShaderVertexAttributeVariable::PASSTHROUGH_TEXTURE_COORDINATE}},
            {ShaderType::SKYBOX, {ShaderVertexAttributeVariable::XYZ_POSITION}},
            {ShaderType::ABSOLUTE_POSITION_WITH_SOLID_COLOR, {ShaderVertexAttributeVariable::XYZ_POSITION}},
            {ShaderType::TEXT, {ShaderVertexAttributeVariable::PASSTHROUGH_TEXTURE_COORDINATE, ShaderVertexAttributeVariable::XY_POSITION}},
            {ShaderType::ABSOLUTE_POSITION_WITH_COLORED_VERTEX, {ShaderVertexAttributeVariable::XYZ_POSITION, ShaderVertexAttributeVariable::PASSTHROUGH_RGB_COLOR}},
        };
        shader_to_used_uniform_variable = {
            {ShaderType::CWL_V_TRANSFORMATION_WITH_SOLID_COLOR, {ShaderUniformVariable::LOCAL_TO_WORLD, ShaderUniformVariable::WORLD_TO_CAMERA, ShaderUniformVariable::CAMERA_TO_CLIP, ShaderUniformVariable::RGBA_COLOR}},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES, {ShaderUniformVariable::LOCAL_TO_WORLD, ShaderUniformVariable::WORLD_TO_CAMERA, ShaderUniformVariable::CAMERA_TO_CLIP, ShaderUniformVariable::TEXTURE_SAMPLER}},
            {ShaderType::TRANSFORM_V_WITH_TEXTURES, {ShaderUniformVariable::TRANSFORM, ShaderUniformVariable::TEXTURE_SAMPLER}},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_LIGHTING, {ShaderUniformVariable::LOCAL_TO_WORLD, ShaderUniformVariable::WORLD_TO_CAMERA, ShaderUniformVariable::CAMERA_TO_CLIP, ShaderUniformVariable::TEXTURE_SAMPLER, ShaderUniformVariable::AMBIENT_LIGHT_STRENGTH, ShaderUniformVariable::AMBIENT_LIGHT_COLOR}},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_AND_DIFFUSE_LIGHTING, {ShaderUniformVariable::LOCAL_TO_WORLD, ShaderUniformVariable::WORLD_TO_CAMERA, ShaderUniformVariable::CAMERA_TO_CLIP, ShaderUniformVariable::TEXTURE_SAMPLER, ShaderUniformVariable::AMBIENT_LIGHT_STRENGTH, ShaderUniformVariable::AMBIENT_LIGHT_COLOR, ShaderUniformVariable::DIFFUSE_LIGHT_POSITION}},
            {ShaderType::SKYBOX, {ShaderUniformVariable::WORLD_TO_CAMERA, ShaderUniformVariable::CAMERA_TO_CLIP, ShaderUniformVariable::SKYBOX_TEXTURE_UNIT}},
            {ShaderType::ABSOLUTE_POSITION_WITH_SOLID_COLOR, {ShaderUniformVariable::RGBA_COLOR}},
            {ShaderType::TEXT, {ShaderUniformVariable::CAMERA_TO_CLIP, ShaderUniformVariable::TEXT_TEXTURE_UNIT, ShaderUniformVariable::RGB_COLOR}},
            {ShaderType::ABSOLUTE_POSITION_WITH_COLORED_VERTEX, {}},
        };
    }
};
#endif // SHADER_STANDARD_HPP