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
    name = "raspberry64_sysroot"
    version = "12.2.0"
    topics = ("sysroot", "build", "installer")

    # package_type = "application"
    
    default_user = "arieo"
    default_channel = "dev"

    options = {"system_triple": ["aarch64-linux-gnu"]}

    def config_options(self):
        self.options.system_triple = "aarch64-linux-gnu"

    def layout(self):
        self.system_name = f"raspberray64-armv8"
        self.output_folder = f"./build/{self.options.system_triple}"
        return

    def source(self):
        # manaully download and install from https://gnutoolchains.com/raspberry/
        return
    
    def build(self):        
        # manaully download and install from https://gnutoolchains.com/raspberry/
        return

    def package(self):
        copy(self, "*", src=os.path.join(self.output_folder, "sysroot"), dst=os.path.join(self.package_folder, self.system_name, "sysroot"), keep_path=True)
        copy(self, "*", src=os.path.join(self.output_folder, "include"), dst=os.path.join(self.package_folder, self.system_name, "include"), keep_path=True)
        copy(self, "*", src=os.path.join(self.output_folder, "lib"), dst=os.path.join(self.package_folder, self.system_name, "lib"), keep_path=True)
        copy(self, "*", src=os.path.join(self.output_folder, "bin"), dst=os.path.join(self.package_folder, self.system_name, "bin"), keep_path=True)

        return

    def package_info(self):
        self.conf_info.define_path("tools.build:sysroot", os.path.join(self.package_folder, self.system_name, "sysroot"))

        # for abi and exception, etc
        self.conf_info.append("tools.build:cxxflags", "-I" + os.path.join(self.package_folder, self.system_name, "include", "c++", "12").replace('\\', '/'))

        self.cpp_info.components["vulkan"].includedirs = [os.path.join(self.package_folder, self.system_name, "sysroot", "usr", "include"), os.path.join(self.package_folder, self.system_name, "sysroot", "usr", "include", "vulkan")]
        self.cpp_info.components["vulkan"].libdirs = [os.path.join(self.package_folder, self.system_name, "sysroot", "usr", "lib", str(self.options.system_triple))]
        self.cpp_info.components["vulkan"].libs = ["vulkan"]
        return
