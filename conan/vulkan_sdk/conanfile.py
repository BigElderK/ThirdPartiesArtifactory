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

class VulkanSDKConan(ConanFile):
    name = "vulkan_sdk"
    version = "1.4.309.0"
    settings = "os", "arch"

    def layout(self):
        self.sdk_install_root_folder = os.path.join(".", "build", str(self.settings.os), str(self.settings.arch), str(self.version))
        return

    def source(self):
        # manaully download and install from https://www.vulkan.org/
        return
        
    def generate(self):
        # manaully download and install from https://www.vulkan.org/
        return
    
    def build(self):        
        return

    def package(self):
        copy(self, "*", src=os.path.join(self.sdk_install_root_folder), dst=os.path.join(self.package_folder), keep_path=True)

        # Then rename .Lib to .lib in the package folder
        """
        package_lib_dir = os.path.join(self.windows_sdk_package_root_folder, "lib", self.version_number)
        if os.path.exists(package_lib_dir):
            for root, _, files in os.walk(package_lib_dir):
                for file in files:
                    if file.endswith(".Lib"):
                        old_path = os.path.join(root, file)
                        new_path = os.path.join(root, file[:-4] + ".lib")
                        rename(self, old_path, new_path+".bak")
                        rename(self, new_path+".bak", new_path)
        ]]
        """
        return

    def package_info(self):
        self.cpp_info.components["vulkan"].includedirs = ['include', os.path.join('include', 'vulkan')]
        self.cpp_info.components["vulkan"].libdirs = ['lib']
        self.cpp_info.components["vulkan"].bindirs = ['bin', 'share']
        self.cpp_info.components["vulkan"].builddirs = ['lib']

        if self.settings.os == "Linux":
            self.cpp_info.components["vulkan"].libs = ["vulkan"]
        if self.settings.os == "Windows":
            self.cpp_info.components["vulkan"].libs = ["vulkan-1"]
        if self.settings.os == "Macos":
            self.cpp_info.components["vulkan"].libs = ["vulkan"]

        self.runenv_info.define("VK_LAYER_PATH", os.path.join(self.package_folder, "bin"))
        return
