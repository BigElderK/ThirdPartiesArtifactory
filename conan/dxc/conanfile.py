import logging
import shutil
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.scm import Git
from conan.tools.files import rmdir
from conan.tools.files import copy
import os

class TinyObjLoaderConan(ConanFile):
    name = "dxc"
    version = "1.8.2505"
    #license = "<Put the package license here>"
    #author = "<Put your name here> <And your email here>"
    #url = "<Package recipe repository url here, for issues about the package>"
    #description = "<Description of Llvm here>"
    topics = ("shader")
    settings = "os", "compiler", "build_type", "arch"
    
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    generators = "CMakeDeps"
    
    #def requirements(self):
        #if self.settings.os in ["Linux", "FreeBSD"]:
            #self.requires("xorg/system")
            #self.requires("wayland/1.22.0")
            #self.requires("xkbcommon/1.6.0")
        
    def layout(self):
        cmake_layout(self, src_folder="./source", build_folder=os.path.join("./build", str(self.settings.os), str(self.settings.arch)))

    def source(self):
        self.run("git clone --recursive https://github.com/microsoft/DirectXShaderCompiler.git --branch v%s" % (self.version))

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder="./DirectXShaderCompiler", cli_args=["-C %s/DirectXShaderCompiler/cmake/caches/PredefinedParams.cmake" % (self.source_folder)])
        cmake.build()
        return
        
    def package(self):
        copy(self, "*", src=os.path.join(self.build_folder, "bin"), dst=os.path.join(self.package_folder, "bin"), keep_path=True)
        return
    
    def package_id(self):
        del self.info.settings.compiler
        del self.info.settings.build_type
        del self.info.options.shared
        del self.info.options.fPIC

    def package_info(self):
        self.cpp_info.bindirs = ['bin']
        return