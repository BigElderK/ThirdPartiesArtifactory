import logging
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.scm import Git
from conan.tools.files import rmdir
from conan.tools.files import apply_conandata_patches, copy, export_conandata_patches, get, rmdir
from conan.tools.microsoft import MSBuild
import os

class FreeImageConan(ConanFile):
    name = "directx_tex"
    version = "0.4.1"
    settings = "os", "arch", "build_type"

    package_type = "application"
            
    def layout(self):
        cmake_layout(self, src_folder="./source", build_folder=os.path.join("./build", str(self.settings.os), str(self.settings.arch)))

    def source(self):
        return
    
    def build(self):
        if self.settings.os == "Windows":
            get(self, url = "https://github.com/matyalatte/Texconv-Custom-DLL/releases/download/v%s/TexconvCustomDLL-v%s-Windows.zip" % (self.version, self.version), destination="bin")
        if self.settings.os == "Linux":
            get(self, url = "https://github.com/matyalatte/Texconv-Custom-DLL/releases/download/v%s/TexconvCustomDLL-v%s-Linux-no-deps.tar.bz2" % (self.version, self.version), destination="bin")
            os.chmod(os.path.join(self.build_folder, "bin", "TexconvCustomDLL", "texconv"), 0o755) 
            os.chmod(os.path.join(self.build_folder, "bin", "TexconvCustomDLL", "texassemble"), 0o755) 
        if self.settings.os == "Macos":
            get(self, url = "https://github.com/matyalatte/Texconv-Custom-DLL/releases/download/v%s/TexconvCustomDLL-v%s-macOS-no-deps.tar.bz2" % (self.version, self.version), destination="bin")
            os.chmod(os.path.join(self.build_folder, "bin", "TexconvCustomDLL", "texconv"), 0o755) 
            os.chmod(os.path.join(self.build_folder, "bin", "TexconvCustomDLL", "texassemble"), 0o755) 
        

    def package(self):
        if self.settings.os == "Linux":
            copy(self, '*', src=os.path.join(self.build_folder, "bin", "TexconvCustomDLL"), dst=os.path.join(self.package_folder, "bin"))
        if self.settings.os == "Windows":
            copy(self, '*', src=os.path.join(self.build_folder, "bin"), dst=os.path.join(self.package_folder, "bin"))
        if self.settings.os == "Macos":
            copy(self, '*', src=os.path.join(self.build_folder, "bin", "TexconvCustomDLL"), dst=os.path.join(self.package_folder, "bin"))
        

    def package_info(self):
        self.cpp_info.bindirs = ['bin']