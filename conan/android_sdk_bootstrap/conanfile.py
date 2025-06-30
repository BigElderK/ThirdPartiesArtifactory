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
    name = "android_sdk"
    version = "bootstrap"
    topics = ("toolchain")

    settings = "os", "arch"

    def layout(self):
        self.sdk_build_folder=os.path.join("./build", str(self.settings.os), str(self.settings.arch))
        return

    def source(self):
        # manaully download and install from https://developer.android.com/ndk/downloads
        return
        
    def build(self):
        return

    def package(self):
        copy(self, "*", src=os.path.join(self.sdk_build_folder, "AndroidSDK"), dst=os.path.join(self.package_folder, "AndroidSDK"), keep_path=True)
        return

    def package_info(self):
        # self.cpp_info.bindirs = [os.path.join(self.package_folder, "AndroidSDK", "cmdline-tools", "bootstrap", "bin")]
        self.runenv_info.define("ANDROID_SDK_BOOTSTRAP_ROOT", os.path.join(self.package_folder, "AndroidSDK"))

        

