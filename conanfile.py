#!/usr/bin/env python
# -*- coding: utf-8 -*-
from conans import ConanFile, tools, CMake
import os

class LibRaptorConan(ConanFile):

    name = "raptor"
    version = "1.4.19"
    url = "http://github.com/fbergmann/conan-raptor"
    homepage = "https://github.com/copasi/copasi-dependencies/tree/master/src/raptor"
    author = "Frank Bergmann"
    license = "MIT"

    description = ("Raptor is a free software / Open Source C library that provides a set"
   " of parsers and serializers that generate Resource Description Framework"
   " (RDF) triples by parsing syntaxes or serialize the triples into a"
   " syntax. The supported parsing syntaxes are RDF/XML, N-Triples, TRiG,"
   " Turtle, RSS tag soup including all versions of RSS, Atom 1.0 and 0.3,"
   " GRDDL and microformats for HTML, XHTML and XML and RDFa. The"
   " serializing syntaxes are RDF/XML (regular, and abbreviated), Atom 1.0,"
   " GraphViz, JSON, N-Triples, RSS 1.0 and XMP.")

    settings = "os", "arch", "compiler", "build_type"

    options = {
        "fPIC": [True, False]
    }

    default_options = (
        "fPIC=True"
    )

    generators = "cmake"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

        if self.settings.os == "Linux":
            del self.options.fPIC

        self.requires("Expat/2.2.7@pix4d/stable")
        self.options['Expat'].shared = False


    def source(self):
        tools.get('https://github.com/copasi/copasi-dependencies/releases/download/v4.26.213/raptor-1.4.19-Source.zip')
        os.rename("raptor-1.4.19-Source", "src") 
        tools.replace_in_file('src/CMakeLists.txt', "project (raptor)", '''project(raptor)

include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
conan_basic_setup()''')

    def _configure(self, cmake):
        args = []
        if self.settings.compiler == 'Visual Studio' and 'MT' in self.settings.compiler.runtime:
            args.append('-DWITH_STATIC_RUNTIME=ON')

        cmake.configure(build_folder="build", args=args, source_folder="src")

    def build(self):
        cmake = CMake(self)
        self._configure(cmake)
        cmake.build()

    def package(self):
        cmake = CMake(self)
        self._configure(cmake)
        cmake.install()
        self.copy("*.lib", dst="lib", keep_path=False)
        if self.settings.os == "Windows":
            self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):

        libfile = "raptor"

        if not self.settings.os == "Windows":
            libfile = "lib" + libfile + ".a"
        else:
            libfile += ".lib"

        self.cpp_info.libs = [libfile]

        self.cpp_info.defines = ["RAPTOR_STATIC"]
