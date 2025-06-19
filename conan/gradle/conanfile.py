import logging
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.scm import Git
from conan.tools.files import rmdir
from conan.tools.files import apply_conandata_patches, copy, export_conandata_patches, get, rmdir
from conan.tools.microsoft import MSBuild
import os

class GradleConan(ConanFile):
    name = "gradle"
    version = "8.14.2"
    settings = "os", "arch", "build_type"

    package_type = "application"
            
    def layout(self):
        cmake_layout(self, src_folder="./source", build_folder=os.path.join("./build", str(self.settings.os), str(self.settings.arch)))

    def source(self):
        return
    
    def build(self):
        return

    def package_id(self):
        del self.info.settings.build_type

    def package(self):
        copy(self, '*', src=os.path.join(self.build_folder), dst=os.path.join(self.package_folder))
        

    def package_info(self):
        self.cpp_info.bindirs = ['bin']