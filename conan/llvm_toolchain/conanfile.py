import logging
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.scm import Git
from conan.tools.files import rmdir, copy
import os

class LlvmConan(ConanFile):
    name = "llvm_toolchain"
    version = "19.1.7"
    #license = "<Put the package license here>"
    #author = "<Put your name here> <And your email here>"
    #url = "<Package recipe repository url here, for issues about the package>"
    #description = "<Description of Llvm here>"
    topics = ("llvm", "clang")
    settings = "os", "compiler", "build_type", "arch"

    options = {"fPIC": [True, False]}
    default_options = {"fPIC": True}

    # package_type = "application"

    def source(self):
        self.run("git clone https://github.com/llvm/llvm-project.git  --branch llvmorg-%s --depth=1" % (self.version)) 

    def layout(self):
        cmake_layout(self, src_folder="./source", build_folder=os.path.join("./build", str(self.settings.os), str(self.settings.arch)))

    def generate(self):
        tc = CMakeToolchain(self)

        # More configrations could be found in https://llvm.org/docs/CMake.html
        tc.cache_variables["LLVM_ENABLE_PROJECTS"] = "bolt;clang;clang-tools-extra;cross-project-tests;libclc;lld;lldb;mlir;polly"
        tc.cache_variables["LLVM_ENABLE_RUNTIMES"] = "libc;libunwind;libcxxabi;pstl;libcxx;compiler-rt;openmp;offload"

        tc.cache_variables["LLVM_USE_LINKER"] = "lld"
        tc.cache_variables["LLVM_ENABLE_LIBCXX"] = True

        # tc.cache_variables["LLVM_LIBDIR_SUFFIX"] = "64"
        # tc.cache_variables["LLVM_TARGETS_TO_BUILD"] = "X86"
        tc.cache_variables["LLVM_USE_LINKER"] = "lld"

        # tc.cache_variables["LLVM_ENABLE_PROJECTS"] = "clang;clang-tools-extra;libc;libclc;lld;lldb;mlir;openmp;polly"
        # tc.cache_variables["LLVM_ENABLE_RUNTIMES"] = "libc;libcxxabi;pstl;libcxx;llvm-libgcc;offload"

        #tc.cache_variables["LLVM_STATIC_LINK_CXX_STDLIB"] = True
        #tc.cache_variables["LLVM_LIBGCC_EXPLICIT_OPT_IN"] = True
        
        tc.cache_variables["LLVM_ENABLE_PIC"] = "ON"
        tc.cache_variables["LIBCLANG_BUILD_STATIC"] = "ON"
        # tc.cache_variables["LIBCXXABI_USE_LLVM_UNWINDER"] = "OFF"

        if self.settings.os == "Windows":
            tc.cache_variables["LLVM_USE_CRT_RELEASE"] = self.settings.compiler.runtime
        
        # tc.cache_variables["LLVM_ENABLE_LIBCXX"] = True
        # tc.cache_variables["CMAKE_INSTALL_CONFIG_NAME"] = self.settings.build_type

        # tc.cache_variables["CMAKE_USE_OPENSSL"] = "OFF"
        # tc.cache_variables["BUILD_TESTING"] = "OFF"

        # https://github.com/llvm/llvm-project/issues/55629
        if self.settings.os == "Linux":
            tc.cache_variables["LIBUNWIND_LINK_FLAGS"] ="-ldl -lpthread"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder="./llvm-project/llvm")
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        #copy(self, "*", src=os.path.join(self.build_folder, "bin"), dst=os.path.join(self.package_folder, "bin"))
        #copy(self, "*", src=os.path.join(self.build_folder, "lib"), dst=os.path.join(self.package_folder, "lib"))

    def package_id(self):
        del self.info.settings.compiler

    def package_info(self):
        self.cpp_info.includedirs = ['include']
        self.cpp_info.libdirs = ['lib', "lib/x86_64-unknown-linux-gnu"]

        self.cpp_info.bindirs = ['bin']

        #self.buildenv_info.prepend_path("LIBRARY_PATH", self.cpp_info.libdirs[0])
        #self.buildenv_info.prepend_path("LD_LIBRARY_PATH", self.cpp_info.libdirs[1])
        #self.buildenv_info.prepend_path("LD_PATH", self.cpp_info.bindirs[0])
 
        self.runenv_info.prepend_path("LIBRARY_PATH", self.cpp_info.libdirs[0])
        self.runenv_info.prepend_path("LD_LIBRARY_PATH", self.cpp_info.libdirs[1])
        self.runenv_info.prepend_path("LD_PATH", self.cpp_info.bindirs[0])
        self.runenv_info.prepend_path("PATH", self.cpp_info.bindirs[0])
        
        #self.runenv_info.define("CC", os.path.join(self.package_folder, "bin", "clang"))
        #self.runenv_info.define("CXX", os.path.join(self.package_folder, "bin", "clang++"))

