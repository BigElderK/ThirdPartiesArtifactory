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
    name = "jdk"
    version = "24.0.1"
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
        copy(self, "*", src=os.path.join(self.sdk_build_folder, f"jdk-{self.version}"), dst=os.path.join(self.package_folder, f"jdk-{self.version}"), keep_path=True)
        return

    def package_info(self):
        self.cpp_info.bindirs = [os.path.join(self.package_folder, f"jdk-{self.version}", "bin")]
        self.runenv_info.define("JAVA_HOME", os.path.join(self.package_folder, f"jdk-{self.version}"))
        return

        

