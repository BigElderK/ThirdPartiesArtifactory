import logging
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.scm import Git
from conan.tools.files import rmdir
import os

class NinjaBinConan(ConanFile):
    name = "ninja"
    version = "1.12.1"
    topics = ("ninja", "build", "installer")
    settings = "os", "arch", "build_type"

    package_type = "application"
    
    # default_user = "bigelderk"
    # default_channel = "default"

    def layout(self):
        cmake_layout(self, src_folder="./source", build_folder=os.path.join("./build", str(self.settings.os), str(self.settings.arch)))

    def source(self):
        self.run("git clone https://github.com/ninja-build/ninja.git --branch v%s --depth=1" % (self.version)) 
        
    def generate(self):
        tc = CMakeToolchain(self)
        tc.cache_variables["CMAKE_USE_OPENSSL"] = "OFF"
        tc.cache_variables["BUILD_TESTING"] = "OFF"
        tc.generate()
    
    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder="./ninja")
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []

        #self.runenv_info.append_path(os.path.join(self.package_folder, "bin"))
        #self.runenv_info.append_path("PATH", os.path.join(self.package_folder, "bin"))
        #self.buildenv_info.append_path("PATH", os.path.join(self.package_folder, "bin"))
        return
