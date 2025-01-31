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
    hpp_output = []

    hpp_output.append("#ifndef SHADER_STANDARD_HPP")
    hpp_output.append("#define SHADER_STANDARD_HPP")
    hpp_output.append("#include <unordered_map>")
    hpp_output.append("#include <string>")
    hpp_output.append("#include <vector>")
    hpp_output.append("#include <glad/glad.h>")

    hpp_output.append("")

    hpp_output.append("enum class ShaderType {")
    for shader_type in ShaderType:
        hpp_output.append(f"    {shader_type.name},")
    hpp_output.append("};")

    hpp_output.append("")
    hpp_output.append("std::string shader_type_to_string(ShaderType shader_type);")
    hpp_output.append("")


    # ShaderVertexAttributeVariable enum
    hpp_output.append("enum class ShaderVertexAttributeVariable {")
    for attribute in ShaderVertexAttributeVariable:
        if attribute != ShaderVertexAttributeVariable.INDEX:  # Exclude INDEX
            hpp_output.append(f"    {attribute.name},")
    hpp_output.append("};")
    hpp_output.append("")

    # ShaderUniformVariable enum
    hpp_output.append("enum class ShaderUniformVariable {")
    for uniform in ShaderUniformVariable:
        hpp_output.append(f"    {uniform.name},")
    hpp_output.append("};")
    hpp_output.append("")

    # ShaderCreationInfo struct
    hpp_output.append("struct ShaderCreationInfo {")
    hpp_output.append("    std::string vertex_path;")
    hpp_output.append("    std::string fragment_path;")
    hpp_output.append("    std::string geometry_path;")
    hpp_output.append("};")
    hpp_output.append("")

    # ShaderProgramInfo struct
    hpp_output.append("struct ShaderProgramInfo {")
    hpp_output.append("    GLuint id;")
    hpp_output.append("};")
    hpp_output.append("")

    # GLVertexAttributeConfiguration struct
    hpp_output.append("struct GLVertexAttributeConfiguration {")
    hpp_output.append("    GLint components_per_vertex;")
    hpp_output.append("    GLenum data_type_of_component;")
    hpp_output.append("    GLboolean normalize;")
    hpp_output.append("    GLsizei stride;")
    hpp_output.append("    GLvoid *pointer_to_start_of_data;")
    hpp_output.append("};")
    hpp_output.append("")

    # Start class definition
    hpp_output.append("class ShaderStandard {")
    hpp_output.append("public:")
    hpp_output.append("    std::unordered_map<ShaderVertexAttributeVariable, GLVertexAttributeConfiguration> shader_vertex_attribute_to_glva_configuration;")
    hpp_output.append("    std::unordered_map<ShaderUniformVariable, std::string> shader_uniform_variable_to_name;")
    hpp_output.append("    std::unordered_map<ShaderVertexAttributeVariable, std::string> shader_vertex_attribute_variable_to_name;")
    hpp_output.append("    std::unordered_map<ShaderType, std::string> shader_type_to_name;")
    hpp_output.append("    std::unordered_map<ShaderType, ShaderCreationInfo> shader_catalog;")
    
    # New variables for used vertex attributes and uniforms
    hpp_output.append("    std::unordered_map<ShaderType, std::vector<ShaderVertexAttributeVariable>> shader_to_used_vertex_attribute_variables;")
    hpp_output.append("    std::unordered_map<ShaderType, std::vector<ShaderUniformVariable>> shader_to_used_uniform_variable;")
    hpp_output.append("")

    hpp_output.append("    ShaderStandard() {")
    hpp_output.append("        shader_vertex_attribute_to_glva_configuration = {")
    for attribute, config in vertex_attribute_to_configuration.items():
        if attribute != ShaderVertexAttributeVariable.INDEX:  # Exclude INDEX
            hpp_output.append(f"            {{ShaderVertexAttributeVariable::{attribute.name}, GLVertexAttributeConfiguration{{{config.components_per_vertex}, {config.data_type_of_component}, {config.normalize}, {config.stride}, {config.pointer_to_start_of_data}}}}},")
    hpp_output.append("        };")

    hpp_output.append("        shader_uniform_variable_to_name = {")
    for uniform in ShaderUniformVariable:
        hpp_output.append(f"            {{ShaderUniformVariable::{uniform.name}, \"{uniform.name.lower()}\"}},")
    hpp_output.append("        };")

    hpp_output.append("        shader_vertex_attribute_variable_to_name = {")
    for attribute in ShaderVertexAttributeVariable:
        if attribute in vertex_attribute_to_configuration.keys():
            hpp_output.append(f"            {{ShaderVertexAttributeVariable::{attribute.name}, \"{attribute.name.lower()}\"}},")
    hpp_output.append("        };")

    hpp_output.append("        shader_type_to_name = {")
    for shader_type in ShaderType:
        hpp_output.append(f"            {{ShaderType::{shader_type.name}, \"{shader_type.name.lower()}\"}},")
    hpp_output.append("        };")
 

    hpp_output.append("        shader_catalog = {")
    for shader_type, prog in shader_catalog.items():
        hpp_output.append(f"            {{ShaderType::{shader_type.name}, {{\"assets/shaders/{prog.vertex_shader_filename}\", \"assets/shaders/{prog.fragment_shader_filename}\"}}}},")
    hpp_output.append("        };")

    # Generate shader_to_used_vertex_attribute_variables
    hpp_output.append("        shader_to_used_vertex_attribute_variables = {")
    for shader_type, variables in shader_info.items():
        attributes = ', '.join(f"ShaderVertexAttributeVariable::{attr}" for attr in variables['valid_attributes'])
        hpp_output.append(f"            {{ShaderType::{shader_type.name}, {{{attributes}}}}},")
    hpp_output.append("        };")

    # Generate shader_to_used_uniform_variable
    hpp_output.append("        shader_to_used_uniform_variable = {")
    for shader_type, variables in shader_info.items():
        uniforms = ', '.join(f"ShaderUniformVariable::{uniform}" for uniform in variables['valid_uniforms'])
        hpp_output.append(f"            {{ShaderType::{shader_type.name}, {{{uniforms}}}}},")
    hpp_output.append("        };")

    hpp_output.append("    }")

    # End class definition
    hpp_output.append("};")

    hpp_output.append("#endif // SHADER_STANDARD_HPP")

    # Define the output directory (script directory)
    output_directory = os.path.dirname(os.path.abspath(__file__))

    # Write to output header file
    header_file_path = os.path.join(output_directory, "shader_standard.hpp")
    with open(header_file_path, "w") as hpp_file:
        hpp_file.write("\n".join(hpp_output))

    cpp_output = []
    cpp_output.append('#include "shader_standard.hpp"')
    cpp_output.append("#include <stdexcept>")
    cpp_output.append("")
    cpp_output.append("std::string shader_type_to_string(ShaderType shader_type) {")
    cpp_output.append("    static const std::unordered_map<ShaderType, std::string> shader_type_map = {")
    for shader_type in ShaderType:
        cpp_output.append(f'        {{ShaderType::{shader_type.name}, "{shader_type.name.lower()}"}},')
    cpp_output.append("    };")
    cpp_output.append("")
    cpp_output.append("    auto it = shader_type_map.find(shader_type);")
    cpp_output.append("    if (it != shader_type_map.end()) {")
    cpp_output.append("        return it->second;")
    cpp_output.append("    } else {")
    cpp_output.append('        throw std::invalid_argument("Invalid ShaderType enum value.");')
    cpp_output.append("    }")
    cpp_output.append("}")

    # Define the output directory (script directory)
    output_directory = os.path.dirname(os.path.abspath(__file__))

    # Write to output header file
    source_file_path = os.path.join(output_directory, "shader_standard.cpp")
    with open(source_file_path, "w") as cpp_file:
        cpp_file.write("\n".join(cpp_output))

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

    # Define the output directory (script directory)
    output_directory = os.path.dirname(os.path.abspath(__file__))

    # Write all accumulated lines to the file
    summary_file_path = os.path.join(output_directory, "shader_summary.py")
    with open(summary_file_path, 'w') as f:
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
        "-sd",
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


