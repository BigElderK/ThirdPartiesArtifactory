import logging
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.scm import Git
from conan.tools.files import rmdir
from conan.tools.microsoft import MSBuild
from conan.tools.files import copy
import os

class MiMallocConan(ConanFile):
    name = "mimalloc"
    version = "3.1.5"
    settings = "os", "arch", "build_type"

    options = {"shared": [True, False], "fPIC": [True, False], "secure": [True, False]}
    default_options = {"shared": False, "fPIC": True, "secure": False}
    
    # default_user = "bigelderk"
    # default_channel = "default"

    def layout(self):
        cmake_layout(self, src_folder="./source", build_folder=os.path.join("./build", str(self.settings.os), str(self.settings.arch)))

    def source(self):
        self.run("git clone https://github.com/microsoft/mimalloc.git --branch v%s --depth=1" % (self.version)) 
        
    def generate(self):
        tc = CMakeToolchain(self)
        tc.cache_variables["MI_BUILD_STATIC"] = "ON"
        if self.options.secure == True:
            tc.cache_variables["MI_SECURE"] = "ON"
        tc.generate()
    
    def build(self):
        if self.settings.os == "Windows":
            msbuild = MSBuild(self)
            msbuild.build(os.path.join(self.source_folder, "mimalloc", "ide", "vs2022", "mimalloc.sln"))

            copy(self, "*", src=os.path.join(self.source_folder, "mimalloc", "out", "msvc-x64", str(self.settings.build_type)), dst=os.path.join(self.build_folder, "lib"), keep_path=True)
            copy(self, "*", src=os.path.join(self.source_folder, "mimalloc", "include"), dst=os.path.join(self.build_folder, "include"), keep_path=True)
        else:
            cmake = CMake(self)
            cmake.configure(build_script_folder="./mimalloc")
            cmake.build()

    def package(self):
        if self.settings.os == "Windows":
            copy(self, "*", src=os.path.join(self.build_folder, "lib"), dst=os.path.join(self.package_folder, "lib"), keep_path=True)
            copy(self, "*", src=os.path.join(self.build_folder, "include"), dst=os.path.join(self.package_folder, "include"), keep_path=True)
        else:
            cmake = CMake(self)
            cmake.install()
            copy(self, "*", src=os.path.join(self.package_folder, "lib", "mimalloc-3.1"), dst=os.path.join(self.package_folder, "lib"), keep_path=True)

    def package_info(self):
        self.cpp_info.includedirs = ['include']
        self.cpp_info.libdirs = ['lib']
        self.cpp_info.libs = ['mimalloc']

        #self.runenv_info.append_path(os.path.join(self.package_folder, "bin"))
        #self.runenv_info.append_path("PATH", os.path.join(self.package_folder, "bin"))
        #self.buildenv_info.append_path("PATH", os.path.join(self.package_folder, "bin"))
        return
