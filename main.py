from standard import *
from colored_print import *
import argparse
from enum import Enum
from typing import Tuple
import re
import os


def extract_variables_from_shader(shader_code: str):
    """
    Extracts uniforms and attributes from the shader code.
    Returns a dictionary with uniforms and vertex attributes along with their types.
    """
    uniform_pattern = r"uniform\s+(\w+)\s+(\w+);"
    attribute_pattern = r"in\s+(\w+)\s+(\w+);"  # GLSL version 330 core uses 'in' for attributes

    uniforms = re.findall(uniform_pattern, shader_code)
    attributes = re.findall(attribute_pattern, shader_code)

    return {
        "uniforms": {name: v_type for v_type, name in uniforms},
        "attributes": {name: v_type for v_type, name in attributes},
    }

def validate_types(shader_variables, verbose):
    """
    Validates the types of uniforms and attributes against expected types from dictionaries.
    """
    valid_uniforms = []
    valid_attributes = []
    # Check uniforms
    for name, v_type in shader_variables['uniforms'].items():
        # Get the expected type based on the key from shader_uniform_variable_to_data
        expected_type = None
        for uniform_var in shader_uniform_variable_to_data.keys():
            if uniform_var.name == name.upper():  # Compare enum names to shader variable names
                expected_type = shader_uniform_variable_to_data[uniform_var]
                break

        if expected_type:
            if expected_type.glsl_type != v_type:
                colored_print(f"    Error: Uniform '{name}' expected type '{expected_type.glsl_type}' but found '{v_type}', fix the type in the shader.", TextColor.RED)
            else:
                valid_uniforms.append(name.upper())
                if verbose:
                    colored_print(f"    Verified uniform '{name}' with type '{v_type}'.", TextColor.WHITE)
        else:
            colored_print(f"    ERROR: Uniform '{name}' is not recognized, you either have a typo or you need to register the new attribute in the standard.", TextColor.RED)

    # Check attributes
    for name, v_type in shader_variables['attributes'].items():
        expected_data = None
        for attrib_var in shader_vertex_attribute_to_data.keys():
            if attrib_var.name == name.upper():  # Compare enum names to shader variable names
                expected_data = shader_vertex_attribute_to_data[attrib_var]
                break

        if expected_data:
            if expected_data.glsl_type != v_type:
                colored_print(f"    Error: Attribute '{name}' expected type '{expected_data.glsl_type}' but found '{v_type}', fix the type in the shader.", TextColor.RED)
            else: 
                valid_attributes.append(name.upper())
                if verbose:
                    colored_print(f"    Verified attribute '{name}' with type '{v_type}'", TextColor.GRAY)
        else:
            colored_print(f"    ERROR: Attribute '{name}' is not recognized, you either have a typo or you need to register the new attribute in the standard.", TextColor.RED)

    return valid_attributes, valid_uniforms

def validate_shader(shader_code: str, shader_program: ShaderProgram, verbose: bool) -> Tuple:
    """
    Validates a shader file by logging issues if found.
    """
    shader_variables = extract_variables_from_shader(shader_code)

    # Validate types
    valid_attrib_unifs = validate_types(shader_variables, verbose)

    return shader_variables, valid_attrib_unifs  # Return the variables for later use

def validate_all_shaders(shader_catalog, shader_directory, verbose: bool, output_info: bool):
    """
    Iterates over all shaders in the shader catalog and validates them.
    :param shader_catalog: Dictionary mapping ShaderType to ShaderProgram instances.
    :param shader_directory: The directory where shader files are located.
    :param output_info: Whether to output shader variable information.
    """
    shader_info = {}

    for shader_type, shader_program in shader_catalog.items():
        # Construct the full file paths
        vertex_shader_path = os.path.join(shader_directory, shader_program.vertex_shader_filename)
        fragment_shader_path = os.path.join(shader_directory, shader_program.fragment_shader_filename)

        # Load shader files from disk
        try:
            with open(vertex_shader_path, 'r') as vertex_shader_file:
                vertex_shader_code = vertex_shader_file.read()
        except FileNotFoundError:
            colored_print(f"Error: Vertex shader file '{vertex_shader_path}' not found.", TextColor.RED)
            continue

        try:
            with open(fragment_shader_path, 'r') as fragment_shader_file:
                fragment_shader_code = fragment_shader_file.read()
        except FileNotFoundError:
            colored_print(f"Error: Fragment shader file '{fragment_shader_path}' not found.", TextColor.RED)
            continue

        colored_print(f"Validating shaders for {shader_type}:", TextColor.GREEN)
        
        # Validate shaders
        colored_print(f"  Validating vertex shader: {shader_program.vertex_shader_filename}", TextColor.GREEN)
        vertex_variables, valid_attrib_unifs = validate_shader(vertex_shader_code, shader_program, verbose)
        
        colored_print(f"  Validating fragment shader: {shader_program.fragment_shader_filename}", TextColor.GREEN)
        fragment_variables, valid_frag_attrib_unifs = validate_shader(fragment_shader_code, shader_program, verbose)


        all_valid_uniforms = valid_attrib_unifs[1] + valid_frag_attrib_unifs[1]


        # Store shader info
        shader_info[shader_type] = {
            "attributes": vertex_variables['attributes'],
            "uniforms": vertex_variables['uniforms'],
            "valid_attributes": valid_attrib_unifs[0],
            "valid_uniforms": all_valid_uniforms,
        }

    if output_info:
        # Print shader information
        colored_print("Shader Information:", TextColor.BRIGHT_BLUE)
        for shader_type, info in shader_info.items():
            colored_print(f"Shader Type: {shader_type.name}", TextColor.GREEN)
            colored_print("  Vertex Attributes:", TextColor.MAGENTA)
            for attr, attr_type in info["attributes"].items():
                colored_print(f"    {attr}: {attr_type}", TextColor.GRAY)
            colored_print("  Uniforms:", TextColor.MAGENTA)
            for uniform, uniform_type in info["uniforms"].items():
                colored_print(f"    {uniform}: {uniform_type}", TextColor.GRAY)

    return shader_info

def generate_cpp(shader_info):
    cpp_output = []

    cpp_output.append("#ifndef SHADER_STANDARD_HPP")
    cpp_output.append("#define SHADER_STANDARD_HPP")
    cpp_output.append("#include <unordered_map>")
    cpp_output.append("#include <string>")
    cpp_output.append("#include <vector>")
    cpp_output.append("#include <glad/glad.h>")
    cpp_output.append("")

    cpp_output.append("enum class ShaderType {")
    for shader_type in ShaderType:
        cpp_output.append(f"    {shader_type.name},")
    cpp_output.append("};")
    cpp_output.append("")

    # ShaderVertexAttributeVariable enum
    cpp_output.append("enum class ShaderVertexAttributeVariable {")
    for attribute in ShaderVertexAttributeVariable:
        if attribute != ShaderVertexAttributeVariable.INDEX:  # Exclude INDEX
            cpp_output.append(f"    {attribute.name},")
    cpp_output.append("};")
    cpp_output.append("")

    # ShaderUniformVariable enum
    cpp_output.append("enum class ShaderUniformVariable {")
    for uniform in ShaderUniformVariable:
        cpp_output.append(f"    {uniform.name},")
    cpp_output.append("};")
    cpp_output.append("")

    # ShaderCreationInfo struct
    cpp_output.append("struct ShaderCreationInfo {")
    cpp_output.append("    std::string vertex_path;")
    cpp_output.append("    std::string fragment_path;")
    cpp_output.append("    std::string geometry_path;")
    cpp_output.append("};")
    cpp_output.append("")

    # ShaderProgramInfo struct
    cpp_output.append("struct ShaderProgramInfo {")
    cpp_output.append("    GLuint id;")
    cpp_output.append("};")
    cpp_output.append("")

    # GLVertexAttributeConfiguration struct
    cpp_output.append("struct GLVertexAttributeConfiguration {")
    cpp_output.append("    GLint components_per_vertex;")
    cpp_output.append("    GLenum data_type_of_component;")
    cpp_output.append("    GLboolean normalize;")
    cpp_output.append("    GLsizei stride;")
    cpp_output.append("    GLvoid *pointer_to_start_of_data;")
    cpp_output.append("};")
    cpp_output.append("")

    # Start class definition
    cpp_output.append("class ShaderStandard {")
    cpp_output.append("public:")
    cpp_output.append("    std::unordered_map<ShaderVertexAttributeVariable, GLVertexAttributeConfiguration> shader_vertex_attribute_to_glva_configuration;")
    cpp_output.append("    std::unordered_map<ShaderUniformVariable, std::string> shader_uniform_variable_to_name;")
    cpp_output.append("    std::unordered_map<ShaderVertexAttributeVariable, std::string> shader_vertex_attribute_variable_to_name;")
    cpp_output.append("    std::unordered_map<ShaderType, std::string> shader_type_to_name;")
    cpp_output.append("    std::unordered_map<ShaderType, ShaderCreationInfo> shader_catalog;")
    
    # New variables for used vertex attributes and uniforms
    cpp_output.append("    std::unordered_map<ShaderType, std::vector<ShaderVertexAttributeVariable>> shader_to_used_vertex_attribute_variables;")
    cpp_output.append("    std::unordered_map<ShaderType, std::vector<ShaderUniformVariable>> shader_to_used_uniform_variable;")
    cpp_output.append("")

    cpp_output.append("    ShaderStandard() {")
    cpp_output.append("        shader_vertex_attribute_to_glva_configuration = {")
    for attribute, config in vertex_attribute_to_configuration.items():
        if attribute != ShaderVertexAttributeVariable.INDEX:  # Exclude INDEX
            cpp_output.append(f"            {{ShaderVertexAttributeVariable::{attribute.name}, GLVertexAttributeConfiguration{{{config.components_per_vertex}, {config.data_type_of_component}, {config.normalize}, {config.stride}, {config.pointer_to_start_of_data}}}}},")
    cpp_output.append("        };")

    cpp_output.append("        shader_uniform_variable_to_name = {")
    for uniform in ShaderUniformVariable:
        cpp_output.append(f"            {{ShaderUniformVariable::{uniform.name}, \"{uniform.name.lower()}\"}},")
    cpp_output.append("        };")

    cpp_output.append("        shader_vertex_attribute_variable_to_name = {")
    for attribute in ShaderVertexAttributeVariable:
        if attribute in vertex_attribute_to_configuration.keys():
            cpp_output.append(f"            {{ShaderVertexAttributeVariable::{attribute.name}, \"{attribute.name.lower()}\"}},")
    cpp_output.append("        };")

    cpp_output.append("        shader_type_to_name = {")
    for shader_type in ShaderType:
        cpp_output.append(f"            {{ShaderType::{shader_type.name}, \"{shader_type.name.lower()}\"}},")
    cpp_output.append("        };")
 

    cpp_output.append("        shader_catalog = {")
    for shader_type, prog in shader_catalog.items():
        cpp_output.append(f"            {{ShaderType::{shader_type.name}, {{\"assets/shaders/{prog.vertex_shader_filename}\", \"assets/shaders/{prog.fragment_shader_filename}\"}}}},")
    cpp_output.append("        };")

    # Generate shader_to_used_vertex_attribute_variables
    cpp_output.append("        shader_to_used_vertex_attribute_variables = {")
    for shader_type, variables in shader_info.items():
        attributes = ', '.join(f"ShaderVertexAttributeVariable::{attr}" for attr in variables['valid_attributes'])
        cpp_output.append(f"            {{ShaderType::{shader_type.name}, {{{attributes}}}}},")
    cpp_output.append("        };")

    # Generate shader_to_used_uniform_variable
    cpp_output.append("        shader_to_used_uniform_variable = {")
    for shader_type, variables in shader_info.items():
        uniforms = ', '.join(f"ShaderUniformVariable::{uniform}" for uniform in variables['valid_uniforms'])
        cpp_output.append(f"            {{ShaderType::{shader_type.name}, {{{uniforms}}}}},")
    cpp_output.append("        };")

    cpp_output.append("    }")

    # End class definition
    cpp_output.append("};")

    cpp_output.append("#endif // SHADER_STANDARD_HPP")

    # Write to output header file
    with open("shader_standard.hpp", "w") as hpp_file:
        hpp_file.write("\n".join(cpp_output))

def generate_py_shader_summary(shader_info):
    py_output = []  # List to accumulate output lines

    # Generate shader_to_used_vertex_attribute_variables
    py_output.append("from standard import *\n")
    py_output.append("shader_to_used_vertex_attribute_variables = {\n")
    for shader_type, variables in shader_info.items():
        attributes = ', '.join(f"ShaderVertexAttributeVariable.{attr}" for attr in variables['valid_attributes'])
        py_output.append(f"    ShaderType.{shader_type.name}: [{attributes}],\n")
    py_output.append("}\n\n")

    # # Generate shader_to_used_uniform_variable
    # py_output.append("shader_to_used_uniform_variable = {\n")
    # for shader_type, variables in shader_info.items():
    #     uniforms = ', '.join(f"ShaderUniformVariable.{uniform}" for uniform in variables['valid_uniforms'])
    #     py_output.append(f"    ShaderType.{shader_type.name}: {{{uniforms}}},\n")
    # py_output.append("}\n")

    # Write all accumulated lines to the file
    with open("shader_summary.py", 'w') as f:
        f.writelines(py_output)



if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Shader Standard Manager")
    parser.add_argument(
        "--verbose", 
        "-v",
        action="store_true", 
        help="Enable verbose output for successful verifications"
    )
    parser.add_argument(
        "--shader-directory", 
        type=str, 
        default="../../assets/shaders/",
        help="Path to the directory containing shader files"
    )
    parser.add_argument(
        "--summary", 
        "-s",
        action="store_true", 
        help="Output shader variable information for each shader"
    )
    parser.add_argument(
        "--gen-cpp", 
        "-gc",
        action="store_true", 
        help="Generates the required cpp file to integrate with the shader cache"
    )
    parser.add_argument('--gen-py-shader-summary', '-gp', action="store_true", help="Generate Python shader summary file")

    args = parser.parse_args()

    # Validate all shaders
    shader_info = validate_all_shaders(shader_catalog, args.shader_directory, args.verbose, args.summary)
    if args.gen_cpp:
        generate_cpp(shader_info)

    if args.gen_py_shader_summary:
        generate_py_shader_summary(shader_info)


