PROJECT(RaptorPackageTest)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()


file(GLOB TEST_SOURCES
  ${CMAKE_CURRENT_SOURCE_DIR}/*.c
)

ADD_EXECUTABLE(raptor_Test ${TEST_SOURCES})
TARGET_LINK_LIBRARIES(raptor_Test ${CONAN_LIBS})
