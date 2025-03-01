import logging
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.scm import Git
from conan.tools.files import rmdir
import os

class LlvmConan(ConanFile):
    name = "clang"
    version = "19.1.7"
    #license = "<Put the package license here>"
    #author = "<Put your name here> <And your email here>"
    #url = "<Package recipe repository url here, for issues about the package>"
    #description = "<Description of Llvm here>"
    topics = ("llvm", "clang")
    settings = "os", "compiler", "build_type", "arch"
    default_user = "kplanb"
    default_channel = "default"

    def source(self):
        self.run("git clone https://github.com/llvm/llvm-project.git  --branch llvmorg-%s --depth=1" % (self.version)) 

    def layout(self):
        cmake_layout(self, src_folder="./source", build_folder="./build")

    def generate(self):
        tc = CMakeToolchain(self)

        # More configrations could be found in https://llvm.org/docs/CMake.html
        # tc.preprocessor_definitions["LLVM_ENABLE_PROJECTS"] = "clang;clang-tools-extra;libcxx;libcxxabi;libunwind;lldb;comipler-rt;lld;compiler-rt;polly"
        tc.preprocessor_definitions["LLVM_ENABLE_PROJECTS"] = "clang;libcxx;libcxxabi;libunwind;lldb;lld;polly"
        tc.preprocessor_definitions["LLVM_STATIC_LINK_CXX_STDLIB"] = True

        tc.preprocessor_definitions["LLVM_ENABLE_PIC"] = "ON"
        tc.preprocessor_definitions["LIBCLANG_BUILD_STATIC"] = "ON"

        if self.settings.os == "Windows":
            tc.preprocessor_definitions["LLVM_USE_CRT_RELEASE"] = self.settings.compiler.runtime
        
        tc.preprocessor_definitions["LLVM_ENABLE_LIBCXX"] = True
        tc.preprocessor_definitions["CMAKE_INSTALL_CONFIG_NAME"] = self.settings.build_type

        tc.cache_variables["CMAKE_USE_OPENSSL"] = "OFF"
        tc.cache_variables["BUILD_TESTING"] = "OFF"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder="./llvm-project/llvm")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["clang", "clangAST"]
        self.cpp_info.includedirs = ['include']
        self.cpp_info.libdirs = ['lib']
        self.cpp_info.bindirs = ['bin']

        self.env_info.path.append(os.path.join(self.package_folder, "bin"))

