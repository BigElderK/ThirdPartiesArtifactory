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
import platform

class NDKSysrootConan(ConanFile):
    name = "android_sysroot"
    version = "27.2.12479018"
    topics = ("sysroot")
        
    settings = "os", "arch"
    def layout(self):
        self.output_folder = "./build/android-ndk-r27c"
        return

    def source(self):
        # manaully download and install from https://developer.android.com/ndk/downloads
        return
    
    def build(self):        
        # manaully download and install from https://developer.android.com/ndk/downloads
        return

    def package(self):
        sys_root_dir = ""
        for root, dirs, files in os.walk(os.path.join(self.output_folder, "toolchains")):
            for dir_name in dirs:
                if dir_name == "sysroot":
                    sys_root_dir = os.path.join(root, dir_name).replace("\\", "/")

        print(f"Sysroot found: {sys_root_dir}")

        copy(self, "*", src=sys_root_dir, dst=os.path.join(self.package_folder, "sysroot"), keep_path=True)
        return
        
    def package_id(self):
        del self.info.settings.arch
        del self.info.settings.os

    def package_info(self):
        system_triple = ""
        if self.settings.os == "Android":
            if self.settings.arch == "armv8":
                system_triple = "aarch64-linux-android"
            elif self.settings.arch == "aarch64":
                system_triple = "aarch64-linux-android"
            elif self.settings.arch == "i686":
                system_triple = "i686-linux-android"
            elif self.settings.arch == "riscv64":
                system_triple = "riscv64-linux-android"
            elif self.settings.arch == "x86_64":
                system_triple = "x86_64-linux-android"
        
        default_inlcude_dir = os.path.join(self.package_folder, "sysroot", "usr", "include")
        default_lib_dir = os.path.join(self.package_folder, "sysroot", "usr", "lib", system_triple, str(self.settings.os.api_level))

        self.cpp_info.components["vulkan"].includedirs = [os.path.join(default_inlcude_dir, "vulkan")]
        self.cpp_info.components["vulkan"].libdirs = [default_lib_dir]
        self.cpp_info.components["vulkan"].libs = ["vulkan"]
        return