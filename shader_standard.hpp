#ifndef SHADER_STANDARD_HPP
#define SHADER_STANDARD_HPP
#include <unordered_map>
#include <string>
#include <vector>
#include <glad/glad.h>

enum class ShaderType {
    TEXTURE_PACKER_RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_WITH_TEXTURES,
    RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_WITH_TEXTURES,
    CWL_V_TRANSFORMATION_WITH_SOLID_COLOR,
    CWL_V_TRANSFORMATION_WITH_TEXTURES,
    TRANSFORM_V_WITH_TEXTURES,
    CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_LIGHTING,
    CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_AND_DIFFUSE_LIGHTING,
    SKYBOX,
    ABSOLUTE_POSITION_WITH_SOLID_COLOR,
    TEXT,
    ABSOLUTE_POSITION_WITH_COLORED_VERTEX,
    TRANSFORM_V_WITH_SIGNED_DISTANCE_FIELD_TEXT,
};

enum class ShaderVertexAttributeVariable {
    XYZ_POSITION,
    XY_POSITION,
    PASSTHROUGH_TEXTURE_COORDINATE,
    PASSTHROUGH_RGB_COLOR,
    PASSTHROUGH_NORMAL,
    PASSTHROUGH_BONE_IDS,
    PASSTHROUGH_BONE_WEIGHTS,
    TEXTURE_COORDINATE,
    TEXTURE_COORDINATE_3D,
    RGB_COLOR,
    WORLD_SPACE_POSITION,
    NORMAL,
    BONE_IDS,
    BONE_WEIGHTS,
    PASSTHROUGH_PACKED_TEXTURE_INDEX,
    PACKED_TEXTURE_INDEX,
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
    CHARACTER_WIDTH,
    EDGE_TRANSITION_WIDTH,
    ID_OF_BONE_TO_VISUALIZE,
    BONE_ANIMATION_TRANSFORMS,
    PACKED_TEXTURES,
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
            {ShaderVertexAttributeVariable::PASSTHROUGH_BONE_IDS, GLVertexAttributeConfiguration{4, GL_INT, GL_FALSE, 0, (void *)0}},
            {ShaderVertexAttributeVariable::PASSTHROUGH_BONE_WEIGHTS, GLVertexAttributeConfiguration{4, GL_FLOAT, GL_FALSE, 0, (void *)0}},
            {ShaderVertexAttributeVariable::PASSTHROUGH_PACKED_TEXTURE_INDEX, GLVertexAttributeConfiguration{1, GL_INT, GL_FALSE, 0, (void *)0}},
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
            {ShaderUniformVariable::CHARACTER_WIDTH, "character_width"},
            {ShaderUniformVariable::EDGE_TRANSITION_WIDTH, "edge_transition_width"},
            {ShaderUniformVariable::ID_OF_BONE_TO_VISUALIZE, "id_of_bone_to_visualize"},
            {ShaderUniformVariable::BONE_ANIMATION_TRANSFORMS, "bone_animation_transforms"},
            {ShaderUniformVariable::PACKED_TEXTURES, "packed_textures"},
        };
        shader_vertex_attribute_variable_to_name = {
            {ShaderVertexAttributeVariable::XYZ_POSITION, "xyz_position"},
            {ShaderVertexAttributeVariable::XY_POSITION, "xy_position"},
            {ShaderVertexAttributeVariable::PASSTHROUGH_TEXTURE_COORDINATE, "passthrough_texture_coordinate"},
            {ShaderVertexAttributeVariable::PASSTHROUGH_RGB_COLOR, "passthrough_rgb_color"},
            {ShaderVertexAttributeVariable::PASSTHROUGH_NORMAL, "passthrough_normal"},
            {ShaderVertexAttributeVariable::PASSTHROUGH_BONE_IDS, "passthrough_bone_ids"},
            {ShaderVertexAttributeVariable::PASSTHROUGH_BONE_WEIGHTS, "passthrough_bone_weights"},
            {ShaderVertexAttributeVariable::PASSTHROUGH_PACKED_TEXTURE_INDEX, "passthrough_packed_texture_index"},
        };
        shader_type_to_name = {
            {ShaderType::TEXTURE_PACKER_RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_WITH_TEXTURES, "texture_packer_rigged_and_animated_cwl_v_transformation_with_textures"},
            {ShaderType::RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_WITH_TEXTURES, "rigged_and_animated_cwl_v_transformation_with_textures"},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_SOLID_COLOR, "cwl_v_transformation_with_solid_color"},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES, "cwl_v_transformation_with_textures"},
            {ShaderType::TRANSFORM_V_WITH_TEXTURES, "transform_v_with_textures"},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_LIGHTING, "cwl_v_transformation_with_textures_ambient_lighting"},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_AND_DIFFUSE_LIGHTING, "cwl_v_transformation_with_textures_ambient_and_diffuse_lighting"},
            {ShaderType::SKYBOX, "skybox"},
            {ShaderType::ABSOLUTE_POSITION_WITH_SOLID_COLOR, "absolute_position_with_solid_color"},
            {ShaderType::TEXT, "text"},
            {ShaderType::ABSOLUTE_POSITION_WITH_COLORED_VERTEX, "absolute_position_with_colored_vertex"},
            {ShaderType::TRANSFORM_V_WITH_SIGNED_DISTANCE_FIELD_TEXT, "transform_v_with_signed_distance_field_text"},
        };
        shader_catalog = {
            {ShaderType::TEXTURE_PACKER_RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_WITH_TEXTURES, {"assets/shaders/texture_packer/bone_and_CWL_v_transformation_with_texture_coordinate_and_bone_data_passthrough.vert", "assets/shaders/texture_packer/textured_with_single_bone_visualization.frag"}},
            {ShaderType::RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_WITH_TEXTURES, {"assets/shaders/bone_and_CWL_v_transformation_with_texture_coordinate_and_bone_data_passthrough.vert", "assets/shaders/textured_with_single_bone_visualization.frag"}},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_SOLID_COLOR, {"assets/shaders/CWL_v_transformation.vert", "assets/shaders/solid_color.frag"}},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES, {"assets/shaders/CWL_v_transformation_with_texture_coordinate_passthrough.vert", "assets/shaders/textured.frag"}},
            {ShaderType::TRANSFORM_V_WITH_TEXTURES, {"assets/shaders/transform_v_with_texture_coordinate_passthrough.vert", "assets/shaders/textured.frag"}},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_LIGHTING, {"assets/shaders/CWL_v_transformation_with_texture_coordinate_passthrough.vert", "assets/shaders/textured_with_ambient_lighting.frag"}},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_AND_DIFFUSE_LIGHTING, {"assets/shaders/CWL_v_transformation_with_texture_coordinate_and_normal_passthrough.vert", "assets/shaders/textured_with_ambient_and_diffuse_lighting.frag"}},
            {ShaderType::SKYBOX, {"assets/shaders/cubemap.vert", "assets/shaders/cubemap.frag"}},
            {ShaderType::ABSOLUTE_POSITION_WITH_SOLID_COLOR, {"assets/shaders/absolute_position.vert", "assets/shaders/solid_color.frag"}},
            {ShaderType::TEXT, {"assets/shaders/text.vert", "assets/shaders/text.frag"}},
            {ShaderType::ABSOLUTE_POSITION_WITH_COLORED_VERTEX, {"assets/shaders/colored_vertices.vert", "assets/shaders/colored_vertices.frag"}},
            {ShaderType::TRANSFORM_V_WITH_SIGNED_DISTANCE_FIELD_TEXT, {"assets/shaders/transform_v_with_texture_coordinate_passthrough.vert", "assets/shaders/signed_distance_field_text.frag"}},
        };
        shader_to_used_vertex_attribute_variables = {
            {ShaderType::TEXTURE_PACKER_RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_WITH_TEXTURES, {ShaderVertexAttributeVariable::XYZ_POSITION, ShaderVertexAttributeVariable::PASSTHROUGH_TEXTURE_COORDINATE, ShaderVertexAttributeVariable::PASSTHROUGH_BONE_IDS, ShaderVertexAttributeVariable::PASSTHROUGH_BONE_WEIGHTS, ShaderVertexAttributeVariable::PASSTHROUGH_PACKED_TEXTURE_INDEX}},
            {ShaderType::RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_WITH_TEXTURES, {ShaderVertexAttributeVariable::XYZ_POSITION, ShaderVertexAttributeVariable::PASSTHROUGH_TEXTURE_COORDINATE, ShaderVertexAttributeVariable::PASSTHROUGH_BONE_IDS, ShaderVertexAttributeVariable::PASSTHROUGH_BONE_WEIGHTS}},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_SOLID_COLOR, {ShaderVertexAttributeVariable::XYZ_POSITION}},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES, {ShaderVertexAttributeVariable::XYZ_POSITION, ShaderVertexAttributeVariable::PASSTHROUGH_TEXTURE_COORDINATE}},
            {ShaderType::TRANSFORM_V_WITH_TEXTURES, {ShaderVertexAttributeVariable::XYZ_POSITION, ShaderVertexAttributeVariable::PASSTHROUGH_TEXTURE_COORDINATE}},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_LIGHTING, {ShaderVertexAttributeVariable::XYZ_POSITION, ShaderVertexAttributeVariable::PASSTHROUGH_TEXTURE_COORDINATE}},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_AND_DIFFUSE_LIGHTING, {ShaderVertexAttributeVariable::XYZ_POSITION, ShaderVertexAttributeVariable::PASSTHROUGH_NORMAL, ShaderVertexAttributeVariable::PASSTHROUGH_TEXTURE_COORDINATE}},
            {ShaderType::SKYBOX, {ShaderVertexAttributeVariable::XYZ_POSITION}},
            {ShaderType::ABSOLUTE_POSITION_WITH_SOLID_COLOR, {ShaderVertexAttributeVariable::XYZ_POSITION}},
            {ShaderType::TEXT, {ShaderVertexAttributeVariable::PASSTHROUGH_TEXTURE_COORDINATE, ShaderVertexAttributeVariable::XY_POSITION}},
            {ShaderType::ABSOLUTE_POSITION_WITH_COLORED_VERTEX, {ShaderVertexAttributeVariable::XYZ_POSITION, ShaderVertexAttributeVariable::PASSTHROUGH_RGB_COLOR}},
            {ShaderType::TRANSFORM_V_WITH_SIGNED_DISTANCE_FIELD_TEXT, {ShaderVertexAttributeVariable::XYZ_POSITION, ShaderVertexAttributeVariable::PASSTHROUGH_TEXTURE_COORDINATE}},
        };
        shader_to_used_uniform_variable = {
            {ShaderType::TEXTURE_PACKER_RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_WITH_TEXTURES, {ShaderUniformVariable::LOCAL_TO_WORLD, ShaderUniformVariable::WORLD_TO_CAMERA, ShaderUniformVariable::CAMERA_TO_CLIP, ShaderUniformVariable::ID_OF_BONE_TO_VISUALIZE, ShaderUniformVariable::PACKED_TEXTURES}},
            {ShaderType::RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_WITH_TEXTURES, {ShaderUniformVariable::LOCAL_TO_WORLD, ShaderUniformVariable::WORLD_TO_CAMERA, ShaderUniformVariable::CAMERA_TO_CLIP, ShaderUniformVariable::ID_OF_BONE_TO_VISUALIZE, ShaderUniformVariable::TEXTURE_SAMPLER}},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_SOLID_COLOR, {ShaderUniformVariable::LOCAL_TO_WORLD, ShaderUniformVariable::WORLD_TO_CAMERA, ShaderUniformVariable::CAMERA_TO_CLIP, ShaderUniformVariable::RGBA_COLOR}},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES, {ShaderUniformVariable::LOCAL_TO_WORLD, ShaderUniformVariable::WORLD_TO_CAMERA, ShaderUniformVariable::CAMERA_TO_CLIP, ShaderUniformVariable::TEXTURE_SAMPLER}},
            {ShaderType::TRANSFORM_V_WITH_TEXTURES, {ShaderUniformVariable::TRANSFORM, ShaderUniformVariable::TEXTURE_SAMPLER}},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_LIGHTING, {ShaderUniformVariable::LOCAL_TO_WORLD, ShaderUniformVariable::WORLD_TO_CAMERA, ShaderUniformVariable::CAMERA_TO_CLIP, ShaderUniformVariable::TEXTURE_SAMPLER, ShaderUniformVariable::AMBIENT_LIGHT_STRENGTH, ShaderUniformVariable::AMBIENT_LIGHT_COLOR}},
            {ShaderType::CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_AND_DIFFUSE_LIGHTING, {ShaderUniformVariable::LOCAL_TO_WORLD, ShaderUniformVariable::WORLD_TO_CAMERA, ShaderUniformVariable::CAMERA_TO_CLIP, ShaderUniformVariable::TEXTURE_SAMPLER, ShaderUniformVariable::AMBIENT_LIGHT_STRENGTH, ShaderUniformVariable::AMBIENT_LIGHT_COLOR, ShaderUniformVariable::DIFFUSE_LIGHT_POSITION}},
            {ShaderType::SKYBOX, {ShaderUniformVariable::WORLD_TO_CAMERA, ShaderUniformVariable::CAMERA_TO_CLIP, ShaderUniformVariable::SKYBOX_TEXTURE_UNIT}},
            {ShaderType::ABSOLUTE_POSITION_WITH_SOLID_COLOR, {ShaderUniformVariable::RGBA_COLOR}},
            {ShaderType::TEXT, {ShaderUniformVariable::CAMERA_TO_CLIP, ShaderUniformVariable::TEXT_TEXTURE_UNIT, ShaderUniformVariable::RGB_COLOR}},
            {ShaderType::ABSOLUTE_POSITION_WITH_COLORED_VERTEX, {}},
            {ShaderType::TRANSFORM_V_WITH_SIGNED_DISTANCE_FIELD_TEXT, {ShaderUniformVariable::TRANSFORM, ShaderUniformVariable::TEXTURE_SAMPLER, ShaderUniformVariable::CHARACTER_WIDTH, ShaderUniformVariable::EDGE_TRANSITION_WIDTH, ShaderUniformVariable::RGB_COLOR}},
        };
    }
};
#endif // SHADER_STANDARD_HPP