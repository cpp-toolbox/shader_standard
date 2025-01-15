# shader_standard
a system which enforces a standard for naming variables in shaders, this is so that we can have systems such as the shader cache, and it can integrate much easier with more assumptions.

## catalog

Note that for each shader program listed here you can explore `standard.py` to specifically to see what shader files are used to build it.

## terminology
- `TEXTURE`: the shader will use textures
- `LIGHTS`: the shader employs lighting
- `UBOS`: the shader use uniform buffer objects to store data (UBOS 1024) means that array has size 1024.
- `TEXTURE_PACKER`: the shader integrates with the texture packer architecture
- `CWL_V_TRANSFORMATION`: the shader uses the matrices `camera_to_clip`, `world_to_camera` and `local_to_world` in the form `CVL v` where `v` is a position in space and `CWL` is the product of the matrices.
  - `camera_to_clip`: the transformation which takes the world as seen from the camera and applies effects like perspective to the view, since this is the last applied transform the resulting points are interepreted in clip space
  - `world_to_camera`: the transformation which positions the world to make the camera be at the origin
  - `local_to_world`: usually objects have thieir origin set to the center of the object, ie, when imported they will be at the origin, this matrix positions the model in the right place and correct orientiation
- `RIGGED_AND_ANIMATED`: the shader uses skeletal animation and requires bone weights along with animation matrices to operate correctly

## stuff that applies to many shaders

### TEXTURE PACKERS

For every texture packer you need to at least assign the bounding boxes: 

```cpp
    TexturePacker texture_packer(textures_directory, output_dir, container_side_length);

    shader_cache.set_uniform(ShaderType::CWL_V_TRANSFORMATION_TEXTURE_PACKED,
                             ShaderUniformVariable::PACKED_TEXTURE_BOUNDING_BOXES,
                             texture_packer.texture_index_to_bounding_box);
```

the texture packer allows you to add new textures dynamically when you do a call to regenerate, you will have to refresh all existing geometry though, see how observatory does this until this is better documented.

### CWL_V SHADERS

You'll want to update their uniforms one time per frame like this: 

```cpp
shader_cache.set_uniform(ShaderType::CWL_V_TRANSFORMATION_TEXTURE_PACKED, ShaderUniformVariable::CAMERA_TO_CLIP, projection);
shader_cache.set_uniform(ShaderType::CWL_V_TRANSFORMATION_TEXTURE_PACKED, ShaderUniformVariable::WORLD_TO_CAMERA, origin_view); shader_cache.set_uniform(ShaderType::CWL_V_TRANSFORMATION_TEXTURE_PACKED, ShaderUniformVariable::LOCAL_TO_WORLD, local_to_world);
```

### UBO SHADERS

First assign all your matrices like this as a uniform buffer object
```cpp
GLuint ltw_matrices_gl_name;
glm::mat4 ltw_matrices[1024];

// initialize all matrices to identity matrices
for (int i = 0; i < 1024; ++i) {
    ltw_matrices[i] = glm::mat4(1.0f);
}

glGenBuffers(1, &ltw_matrices_gl_name);
glBindBuffer(GL_UNIFORM_BUFFER, ltw_matrices_gl_name);
glBufferData(GL_UNIFORM_BUFFER, sizeof(ltw_matrices), ltw_matrices, GL_STATIC_DRAW);
glBindBufferBase(GL_UNIFORM_BUFFER, 0, ltw_matrices_gl_name);
```

Then feel free to modify the `ltw_matrices` variable, each object you draw will contain an index into this array, and thus all you have to do is be sure you put the transform matrix you want to apply to a specific object in the right place, and then one time per frame be sure to upload the new matrices: 

```cpp
glBindBuffer(GL_UNIFORM_BUFFER, ltw_matrices_gl_name);
glBufferSubData(GL_UNIFORM_BUFFER, 0, sizeof(ltw_matrices), ltw_matrices);
glBindBuffer(GL_UNIFORM_BUFFER, 0);
```

## notes for specific shaders

#### TRANSFORM_V_WITH_SIGNED_DISTANCE_FIELD_TEXT
To set up this shader be sure to do the following:
```cpp
auto text_color = glm::vec3(0.5, 0.5, 1);
float char_width = 0.5;
float edge_transition = 0.1;

shader_cache.use_shader_program(ShaderType::TRANSFORM_V_WITH_SIGNED_DISTANCE_FIELD_TEXT);

shader_cache.set_uniform(ShaderType::TRANSFORM_V_WITH_SIGNED_DISTANCE_FIELD_TEXT, ShaderUniformVariable::TRANSFORM,
                         glm::mat4(1.0f));

shader_cache.set_uniform(ShaderType::TRANSFORM_V_WITH_SIGNED_DISTANCE_FIELD_TEXT, ShaderUniformVariable::RGB_COLOR,
                         text_color);

shader_cache.set_uniform(ShaderType::TRANSFORM_V_WITH_SIGNED_DISTANCE_FIELD_TEXT,
                         ShaderUniformVariable::CHARACTER_WIDTH, char_width);

shader_cache.set_uniform(ShaderType::TRANSFORM_V_WITH_SIGNED_DISTANCE_FIELD_TEXT,
                         ShaderUniformVariable::EDGE_TRANSITION_WIDTH, edge_transition);
shader_cache.stop_using_shader_program();
```


###  TEXTURE_PACKER_RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_UBOS_1024_WITH_TEXTURES_AND_MULTIPLE_LIGHTS

### TEXTURE_PACKER_RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_UBOS_2048_WITH_TEXTURES_AND_MULTIPLE_LIGHTS 

### TEXTURE_PACKER_RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_UBOS_4096_WITH_TEXTURES_AND_MULTIPLE_LIGHTS 

### TEXTURE_PACKER_RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_WITH_TEXTURES 

### TEXTURE_PACKER_CWL_V_TRANSFORMATION_UBOS_1024_AMBIENT_AND_DIFFUSE_LIGHTING  

### TEXTURE_PACKER_CWL_V_TRANSFORMATION_UBOS_1024_MULTIPLE_LIGHTS  

### TEXTURE_PACKER_CWL_V_TRANSFORMATION_UBOS_1024 

### RIGGED_AND_ANIMATED_CWL_V_TRANSFORMATION_WITH_TEXTURES 

### CWL_V_TRANSFORMATION_WITH_SOLID_COLOR

### CWL_V_TRANSFORMATION_USING_UBOS_WITH_SOLID_COLOR

### CWL_V_TRANSFORMATION_WITH_TEXTURES

### TRANSFORM_V_WITH_TEXTURES

### CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_LIGHTING

### CWL_V_TRANSFORMATION_WITH_TEXTURES_AMBIENT_AND_DIFFUSE_LIGHTING

### SKYBOX

### ABSOLUTE_POSITION_WITH_SOLID_COLOR

### TEXT

### ABSOLUTE_POSITION_WITH_COLORED_VERTEX

### ABSOLUTE_POSITION_TEXTURED

