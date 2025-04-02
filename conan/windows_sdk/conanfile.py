import logging
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.scm import Git
from conan.tools.files import rmdir
from conan.tools.files import copy
from conan.tools.files import rm
from conan.tools.files import rename
import tarfile
import os
import glob

class WindowsSDKConan(ConanFile):
    name = "windows_sdk"
    version = "10.0.26100.0_x86_64"
    topics = ("build", "installer")

    def layout(self):
        self.windows_sdk_install_root_folder = os.path.join(".", "build", "10")
        self.version_number = "10.0.26100.0"
        self.version_arch = "x64"
        return

    def source(self):
        # manaully download and install from https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/
        return
        
    def generate(self):
        # manaully download and install from https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/
        return
    
    def build(self):        

        return

    def package(self):
        self.windows_sdk_package_root_folder = os.path.join(self.package_folder, "10")
        copy(self, "*", src=os.path.join(self.windows_sdk_install_root_folder, "lib", self.version_number), dst=os.path.join(self.windows_sdk_package_root_folder, "lib", self.version_number), keep_path=True)
        copy(self, "*", src=os.path.join(self.windows_sdk_install_root_folder, "include", self.version_number), dst=os.path.join(self.windows_sdk_package_root_folder, "include", self.version_number), keep_path=True)
        copy(self, "*", src=os.path.join(self.windows_sdk_install_root_folder, "redist", self.version_number), dst=os.path.join(self.windows_sdk_package_root_folder, "redist", self.version_number), keep_path=True)

        # Then rename .Lib to .lib in the package folder
        package_lib_dir = os.path.join(self.windows_sdk_package_root_folder, "lib", self.version_number)
        if os.path.exists(package_lib_dir):
            for root, _, files in os.walk(package_lib_dir):
                for file in files:
                    if file.endswith(".Lib"):
                        old_path = os.path.join(root, file)
                        new_path = os.path.join(root, file[:-4] + ".lib")
                        rename(self, old_path, new_path+".bak")
                        rename(self, new_path+".bak", new_path)
        return

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
        self.windows_sdk_package_root_folder = os.path.join(self.package_folder, "10")

        self.conf_info.append("tools.build:cxxflags", "-Xclang -internal-isystem -Xclang " + os.path.join(self.windows_sdk_package_root_folder, "include", self.version_number, "cppwinrt").replace('\\', '/'))
        self.conf_info.append("tools.build:cflags", "-Xclang -internal-isystem -Xclang " + os.path.join(self.windows_sdk_package_root_folder, "include", self.version_number, "cppwinrt").replace('\\', '/'))

        self.conf_info.append("tools.build:cxxflags", "-Xclang -internal-isystem -Xclang " + os.path.join(self.windows_sdk_package_root_folder, "include", self.version_number, "shared").replace('\\', '/'))
        self.conf_info.append("tools.build:cflags", "-Xclang -internal-isystem -Xclang " + os.path.join(self.windows_sdk_package_root_folder, "include", self.version_number, "shared").replace('\\', '/'))

        self.conf_info.append("tools.build:cxxflags", "-Xclang -internal-isystem -Xclang " + os.path.join(self.windows_sdk_package_root_folder, "include", self.version_number, "ucrt").replace('\\', '/'))
        self.conf_info.append("tools.build:cflags", "-Xclang -internal-isystem -Xclang " + os.path.join(self.windows_sdk_package_root_folder, "include", self.version_number, "ucrt").replace('\\', '/'))

        self.conf_info.append("tools.build:cxxflags", "-Xclang -internal-isystem -Xclang " + os.path.join(self.windows_sdk_package_root_folder, "include", self.version_number, "um").replace('\\', '/'))
        self.conf_info.append("tools.build:cflags", "-Xclang -internal-isystem -Xclang " + os.path.join(self.windows_sdk_package_root_folder, "include", self.version_number, "um").replace('\\', '/'))

        self.conf_info.append("tools.build:cxxflags", "-Xclang -internal-isystem -Xclang " + os.path.join(self.windows_sdk_package_root_folder, "include", self.version_number, "winrt").replace('\\', '/'))
        self.conf_info.append("tools.build:cflags", "-Xclang -internal-isystem -Xclang " + os.path.join(self.windows_sdk_package_root_folder, "include", self.version_number, "winrt").replace('\\', '/'))

        self.conf_info.append("tools.build:exelinkflags", "-L"+os.path.join(self.windows_sdk_package_root_folder, "lib", self.version_number, "um", self.version_arch).replace('\\', '/'))
        self.conf_info.append("tools.build:sharedlinkflags", "-L"+os.path.join(self.windows_sdk_package_root_folder,"lib", self.version_number, "um", self.version_arch).replace('\\', '/'))

        self.conf_info.append("tools.build:exelinkflags", "-L"+os.path.join(self.windows_sdk_package_root_folder, "lib", self.version_number, "ucrt", self.version_arch).replace('\\', '/'))
        self.conf_info.append("tools.build:sharedlinkflags", "-L"+os.path.join(self.windows_sdk_package_root_folder,"lib", self.version_number, "ucrt", self.version_arch).replace('\\', '/'))

        return
