import logging
import shutil
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.scm import Git
from conan.tools.files import rmdir
import os

class FmtConan(ConanFile):
    name = "fmt"
    version = "11.1.4"
    #license = "<Put the package license here>"
    #author = "<Put your name here> <And your email here>"
    #url = "<Package recipe repository url here, for issues about the package>"
    #description = "<Description of Llvm here>"
    topics = ("string")
    settings = "os", "compiler", "build_type", "arch"
    
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    generators = "CMakeDeps"
    
    def layout(self):
        cmake_layout(self, src_folder="./source", build_folder=os.path.join("./build", str(self.settings.os), str(self.settings.arch)))

    def source(self):
        self.run("git clone https://github.com/fmtlib/fmt.git --branch %s" % (self.version))

    def generate(self):
        tc = CMakeToolchain(self)
         
        #tc.cache_variables["CMAKE_VERBOSE_MAKEFILE"] = True

        tc.cache_variables["FMT_TEST"] = "ON"
        tc.cache_variables["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder="./fmt")
        cmake.build()
        return
        
    def package(self):
        cmake = CMake(self)
        cmake.install()
        return

    def package_info(self):
        self.cpp_info.libs = ["fmt"]
        self.cpp_info.bindirs = ['bin']
        self.cpp_info.libdirs = ['lib']
        self.cpp_info.includedirs = ['include']
        return