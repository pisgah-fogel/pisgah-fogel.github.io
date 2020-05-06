cmake_minimum_required(VERSION 3.11)

project(3d_map_ogre)

#set(OGRE_DIR "/usr/share/OGRE/")

# specify which version and components you need
find_package(OGRE 1.11 REQUIRED COMPONENTS Bites RTShaderSystem)

# copy resource.cfg next to our binaries where OGRE looks for it
file(COPY ${OGRE_CONFIG_DIR}/resources.cfg DESTINATION ${CMAKE_CURRENT_BINARY_DIR})

# add the source files as usual
add_executable(0_Bootstrap Bootstrap.cpp)

# this also sets the includes and pulls third party dependencies
target_link_libraries(0_Bootstrap ${OGRE_LIBRARIES})