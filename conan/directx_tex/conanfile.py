import logging
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.scm import Git
from conan.tools.files import rmdir
from conan.tools.files import apply_conandata_patches, copy, export_conandata_patches, get, rmdir
from conan.tools.microsoft import MSBuild
import os

class FreeImageConan(ConanFile):
    name = "DirectXTex"
    version = "sept2023"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    def configure(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
            
    def layout(self):
        cmake_layout(self, src_folder="./source", build_folder=os.path.join("./build", str(self.settings.os), str(self.settings.arch)))

    def source(self):
        self.run("git clone https://github.com/microsoft/DirectXTex.git --branch %s --depth=1" % (self.version)) 

    def generate(self):
        tc = CMakeToolchain(self)
        #tc.cache_variables["GLFW_BUILD_WAYLAND"] = False
        #tc.cache_variables["GLFW_BUILD_X11"] = True
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder="./DirectXTex")
        cmake.build()
        return
    
    # def build(self):

    #     if self.settings.os == "Windows":
    #         msbuild = MSBuild(self)
    #         if self.options.shared == "True":
    #             msbuild.build("source/DirectXTex/FreeImage.2017.sln")
    #         else:
    #             msbuild.build("FreeImage/Source/FreeImageLib/FreeImageLib.2017.vcxproj")
                
    #         #if self.settings.compiler.runtime == 'MT':
    #         #    cmake.definitions["CMAKE_CXX_FLAGS_RELEASE"] = "/MT"
    #     else:
    #         self.run("make --directory=./FreeImage")

    def package(self):
        self.copy('*.h', dst='include', src='FreeImage/Dist', keep_path=False)
        self.copy('*', dst='lib', src='FreeImage/Dist', keep_path=False)

    def package_info(self):  # still very useful for package consumers
        self.cpp_info.includedirs = ['include']
        self.cpp_info.libdirs = ['lib']
        #self.cpp_info.bindirs = ['bin']
        if self.settings.os == "Windows":
            if self.options.shared == "True":
                self.cpp_info.libs = ["FreeImage"]
            else:
                self.cpp_info.libs = ["FreeImageLib"]
                self.cpp_info.defines = ['FREEIMAGE_LIB']
        else:
            if self.options.shared == "True":
                self.cpp_info.libs = ["freeimage-%s" % (self.version)]
            else:
                self.cpp_info.libs = ["freeimage"]
                self.cpp_info.defines = ['FREEIMAGE_LIB']