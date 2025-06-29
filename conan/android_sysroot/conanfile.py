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

import re
from pathlib import Path

class NDKSysrootConan(ConanFile):
    name = "android_sysroot"
    version = "current_ndk"
    topics = ("sysroot")
        
    settings = "os", "arch"

    def package(self):
        return
        
    def package_id(self):
        del self.info.settings.arch
        del self.info.settings.os


    def package_info(self):
        def expand_env_vars_in_path(path):
            """
            Expand all $ENV{VAR} references in a path string with their actual values.
            Raises ValueError if any referenced environment variable is not set.
            """
            def replace_env_match(match):
                var_name = match.group(1)
                value = os.environ.get(var_name)
                if value is None:
                    raise ValueError(f"Environment variable {var_name} is not set")
                return value
            
            # Replace all $ENV{VAR} occurrences with their values
            expanded_path = re.sub(r'\$ENV\{([^}]+)\}', replace_env_match, path)
            
            # Convert to absolute path and normalize
            return str(Path(expanded_path).resolve())

        ndk_path = expand_env_vars_in_path(self.conf.get("tools.android:ndk_path"))
        self.output.warning(f"Ndk path found: {ndk_path}")

        sys_root_dir = ""
        for root, dirs, files in os.walk(os.path.join(ndk_path, "toolchains")):
            for dir_name in dirs:
                if dir_name == "sysroot":
                    sys_root_dir = os.path.join(root, dir_name).replace("\\", "/")

        self.output.warning(f"Sysroot found: {sys_root_dir}")

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
        
        default_inlcude_dir = os.path.join(sys_root_dir, "usr", "include")
        default_lib_dir = os.path.join(sys_root_dir, "usr", "lib", system_triple, str(self.settings.os.api_level))

        self.cpp_info.components["vulkan"].includedirs = [os.path.join(default_inlcude_dir, "vulkan")]
        self.cpp_info.components["vulkan"].libdirs = [default_lib_dir]
        self.cpp_info.components["vulkan"].libs = ["vulkan"]
        return