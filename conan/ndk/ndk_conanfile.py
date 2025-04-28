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

class NDKToolChainConan(ConanFile):
    name = "ndk"
    version = "27.2.12479018"
    topics = ("toolchain")

    settings = "os"

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
        
    def package_info(self):
        self.conf_info.define_path("tools.android:ndk_path", os.path.join(self.package_folder))