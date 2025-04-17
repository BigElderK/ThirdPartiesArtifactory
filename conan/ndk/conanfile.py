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
    name = "ndk"
    version = "27.2.12479018"
    topics = ("sysroot", "build", "installer")

    default_user = "arieo"
    default_channel = "dev"

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
        copy(self, "*", src=os.path.join(self.output_folder), dst=os.path.join(self.package_folder), keep_path=True)
        return

    def package_id(self):
        del self.info.settings.arch
        del self.info.settings.os
        
    def package_info(self):
        self.conf_info.define_path("tools.android:ndk_path", os.path.join(self.package_folder))

        if self.settings.os == "Android":
            if self.settings.arch == "armv8":
                default_arch_folder_name = "aarch64-linux-android"
            #elif self.settings.arch == "aarch64":
            #    default_arch_folder_name = "aarch64-linux-android"
            #elif self.settings.arch == "i686":
            #    default_arch_folder_name = "i686-linux-android"
            #elif self.settings.arch == "riscv64":
            #    default_arch_folder_name = "riscv64-linux-android"
            elif self.settings.arch == "x86_64":
                default_arch_folder_name = "x86_64-linux-android"
            
            default_inlcude_dir = os.path.join(self.package_folder, "toolchains", "llvm", "prebuilt", "windows-x86_64", "sysroot", "usr", "include")
            default_lib_dir = os.path.join(self.package_folder, "toolchains", "llvm", "prebuilt", "windows-x86_64", "sysroot", "usr", "lib", default_arch_folder_name, str(self.settings.os.api_level))

            self.cpp_info.components["vulkan"].includedirs = [os.path.join(default_inlcude_dir, "vulkan")]
            self.cpp_info.components["vulkan"].libdirs = [default_lib_dir]
            self.cpp_info.components["vulkan"].libs = ["vulkan"]
        return
    
        # E:\BigElderK\ThirdPartiesArtifactory\conan\ndk\build\android-ndk-r27c\toolchains\llvm\prebuilt\windows-x86_64\sysroot\usr\include
        # E:\BigElderK\ThirdPartiesArtifactory\conan\ndk\build\android-ndk-r27c\toolchains\llvm\prebuilt\windows-x86_64\sysroot\usr\lib\x86_64-linux-android\35
        return
