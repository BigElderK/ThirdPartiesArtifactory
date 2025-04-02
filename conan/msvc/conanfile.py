import logging
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.scm import Git
from conan.tools.files import rmdir
from conan.tools.files import copy
from conan.tools.files import rm
import tarfile
import os
import glob

class SysRootBinConan(ConanFile):
    name = "msvc"
    version = "14.43.34808_x86_64"
    topics = ("compiler", "build", "installer")
    settings = "arch"

    def layout(self):
        self.msvc_install_root_folder = os.path.join(".", "build", "2022", "Community")
        self.version_number = "14.43.34808"
        self.version_arch = "x64"
        return

    def source(self):
        # manaully download and install from https://visualstudio.microsoft.com/zh-hans/downloads/
        return
        
    def generate(self):
        # manaully download and install from https://visualstudio.microsoft.com/zh-hans/downloads/
        return
    
    def build(self): 
        return

    def package(self):
        self.msvc_package_root_folder = os.path.join(self.package_folder, "2022", "Community")
        copy(self, "*", src=os.path.join(self.msvc_install_root_folder, "VC", "Auxiliary", "VS"), dst=os.path.join(self.msvc_package_root_folder, "VC", "Auxiliary", "VS"), keep_path=True)
        copy(self, "*", src=os.path.join(self.msvc_install_root_folder, "VC", "Tools", "MSVC", self.version_number), dst=os.path.join(self.msvc_package_root_folder, "VC", "Tools", "MSVC", self.version_number), keep_path=True)
        return

    def package_info(self):
        self.msvc_package_root_folder = os.path.join(self.package_folder, "2022", "Community")

        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []

        self.conf_info.define_path("tools.microsoft.msbuild:installation_path", os.path.join(self.msvc_package_root_folder).replace('\\', '/'))
        self.conf_info.define("tools.microsoft.msbuild:vs_version", 17)
        
        self.conf_info.append("tools.build:cxxflags", "-Xclang -internal-isystem -Xclang " + os.path.join(self.msvc_package_root_folder, "VC", "Auxiliary", "VS", "include").replace('\\', '/'))
        self.conf_info.append("tools.build:cflags", "-Xclang -internal-isystem -Xclang " + os.path.join(self.msvc_package_root_folder, "VC", "Auxiliary", "VS", "include").replace('\\', '/'))

        self.conf_info.append("tools.build:cxxflags", "-Xclang -internal-isystem -Xclang " + os.path.join(self.msvc_package_root_folder, "VC", "Tools", "MSVC", str(self.version_number), "include").replace('\\', '/'))
        self.conf_info.append("tools.build:cflags", "-Xclang -internal-isystem -Xclang " + os.path.join(self.msvc_package_root_folder, "VC", "Tools", "MSVC", str(self.version_number), "include").replace('\\', '/'))

        self.conf_info.append("tools.build:exelinkflags", "-L"+os.path.join(self.msvc_package_root_folder, "VC", "Tools", "MSVC", self.version_number, "lib", self.version_arch).replace('\\', '/'))
        self.conf_info.append("tools.build:sharedlinkflags", "-L"+os.path.join(self.msvc_package_root_folder, "VC", "Tools", "MSVC", self.version_number, "lib", self.version_arch).replace('\\', '/'))
        return
