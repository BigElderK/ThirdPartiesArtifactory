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
        
        return

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
        return
