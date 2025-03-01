import logging
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.scm import Git
from conan.tools.files import rmdir
import os

class CMakeBinConan(ConanFile):
    name = "cmake"
    version = "3.31.6"
    topics = ("cmake", "build", "installer")
    package_type = "application"
    settings = "os", "arch", "build_type"
    
    default_user = "kplanb"
    default_channel = "default"

    def layout(self):
        cmake_layout(self, src_folder="./source", build_folder="./build")

    def source(self):
        rmdir(self, "CMake")
        self.run("git clone https://github.com/Kitware/CMake.git --branch v%s --depth=1" % (self.version)) 
        
    def generate(self):
        tc = CMakeToolchain(self)
        tc.cache_variables["CMAKE_USE_OPENSSL"] = "OFF"
        tc.cache_variables["BUILD_TESTING"] = "OFF"
        tc.generate()
    
    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder="./CMake")
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_id(self):
        del self.info.settings.build_type

    def package_info(self):
        self.runenv_info.append_path("PATH", os.path.join(self.package_folder, "bin"))
        self.buildenv_info.append_path("PATH", os.path.join(self.package_folder, "bin"))
        return
