import logging
import shutil
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.scm import Git
from conan.tools.files import rmdir
import os

class LlvmConan(ConanFile):
    name = "llvm"
    version = "20.1.1"
    #license = "<Put the package license here>"
    #author = "<Put your name here> <And your email here>"
    #url = "<Package recipe repository url here, for issues about the package>"
    #description = "<Description of Llvm here>"
    topics = ("llvm", "clang")
    settings = "os", "compiler", "build_type", "arch"
    
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    default_user = "arieo"
    default_channel = "dev"

    # requires = {"zlib/1.3.1", "libxml2/2.13.6", "libiconv/1.17"}

    def source(self):
        self.run("git clone https://github.com/llvm/llvm-project.git  --branch llvmorg-%s --depth=1" % (self.version)) 

    def layout(self):
        #cmake_layout(self, src_folder="./source", build_folder=os.path.join("./build", str(self.settings.os), str(self.settings.arch), "stage2"))
        cmake_layout(self, src_folder="./source", build_folder=os.path.join("./build", str(self.settings.os), str(self.settings.arch)))

    def generate(self):
        #clang_package = self.dependencies["llvm_toolchain"]
        #self.env_info.LIBRARY_PATH.append(clang_package.cpp_info.libdirs[0])
        print(os.environ)
        tc = CMakeToolchain(self)

        #tc.cache_variables["CMAKE_VERBOSE_MAKEFILE"] = True

        # https://llvm.org/docs/AdvancedBuilds.html
        # BUG: Stage2 could not found libc++so built from Stage1
        # have to install with "sudo apt install libc++-dev" in the stystem
        

        # More configrations could be found in https://llvm.org/docs/CMake.html
        # https://github.com/owent/bash-shell/blob/main/LLVM%26Clang%20Installer/19.1/README.md

        tc.cache_variables["CLANG_ENABLE_BOOTSTRAP"] = False
        if self.settings.os == "Linux":
            tc.cache_variables["LLVM_ENABLE_PROJECTS"] = "bolt;clang;clang-tools-extra;lld;llvm;lldb;libclc;polly;pstl"
            tc.cache_variables["LLVM_ENABLE_RUNTIMES"] = "compiler-rt;libcxx;libcxxabi;libunwind"

            tc.cache_variables["BOOTSTRAP_LLVM_ENABLE_PROJECTS"] = "bolt;clang;clang-tools-extra;lld;llvm;lldb;libclc;mlir;polly;pstl"
            tc.cache_variables["BOOTSTRAP_LLVM_ENABLE_RUNTIMES"] = "compiler-rt;libcxx;libcxxabi;libunwind"

            tc.cache_variables["BOOTSTRAP_LLVM_ENABLE_LIBCXX"] = True
            tc.cache_variables["BOOTSTRAP_LLVM_ENABLE_LIBCXXABI"] = True
            
            #tc.cache_variables["LLVM_STATIC_LINK_CXX_STDLIB"] = True
            #tc.cache_variables["LLVM_LIBGCC_EXPLICIT_OPT_IN"] = True
            
            tc.cache_variables["BOOTSTRAP_LLVM_ENABLE_LLVM_LIBC"] = True
            tc.cache_variables["BOOTSTRAP_LLVM_ENABLE_PIC"] = True
            tc.cache_variables["LLVM_ENABLE_PIC"] = "ON"

            tc.cache_variables["LIBUNWIND_LINK_FLAGS"] ="-ldl -lpthread"

        if self.settings.os == "Macos":
            tc.cache_variables["LLVM_ENABLE_PROJECTS"] = "clang;clang-tools-extra;lld;llvm;lldb;polly;pstl"
            tc.cache_variables["LLVM_ENABLE_RUNTIMES"] = "compiler-rt;libcxx;libcxxabi;libunwind"
            tc.cache_variables["LLVM_ENABLE_PIC"] = "ON"
            tc.cache_variables["LLDB_USE_SYSTEM_DEBUGSERVER"] = "ON"
            tc.cache_variables["LIBCXXABI_USE_LLVM_UNWINDER"] = "OFF"
            

        if self.settings.os == "Windows":
            tc.cache_variables["LLVM_ENABLE_PROJECTS"] = "clang;clang-tools-extra;lld;llvm;lldb;polly;pstl"
            tc.cache_variables["LLVM_ENABLE_RUNTIMES"] = "compiler-rt;libcxx"

            #tc.cache_variables["LLVM_ENABLE_INCREMENTAL_LINK"] = False
            #tc.cache_variables["LLVM_ENABLE_EH"] = True
            #tc.cache_variables["LLVM_ENABLE_RTTI"] = True

            tc.cache_variables["LLVM_USE_CRT_RELEASE"] = "MT"
            tc.cache_variables["LIBCXX_ENABLE_SHARED"] = False
            #tc.cache_variables["LIBCXX_ENABLE_ABI_LINKER_SCRIPT"] = False

            #tc.cache_variables["LLVM_ENABLE_LIBUNWIND"] = False
            #tc.cache_variables["LIBCXXABI_USE_LLVM_UNWINDER"] = False

            # tc.cache_variables["LLVM_STATIC_LINK_CXX_STDLIB"] = True
            # https://stackoverflow.com/questions/73679415/build-llvm-16-master-fail-on-libunwind
            #tc.cache_variables["BOOTSTRAP_STATIC_LINK_CXX_STDLIB"] = True
            #tc.cache_variables["BOOTSTRAP_LLVM_ENABLE_PROJECTS"] = "bolt;clang;clang-tools-extra;lld;llvm;lldb;mlir;polly;pstl"
            #tc.cache_variables["BOOTSTRAP_LLVM_ENABLE_RUNTIMES"] = "compiler-rt;libcxx"

            #tc.cache_variables["BOOTSTRAP_LLVM_ENABLE_INCREMENTAL_LINK"] = False
            #tc.cache_variables["BOOTSTRAP_LLVM_ENABLE_EH"] = True
            #tc.cache_variables["BOOTSTRAP_LLVM_ENABLE_RTTI"] = True
            
            #tc.cache_variables["BOOTSTRAP_LLVM_ENABLE_LIBCXX"] = True

            #tc.cache_variables["BOOTSTRAP_LLVM_USE_CRT_RELEASE"] = "MT"
            #tc.cache_variables["BOOTSTRAP_LIBCXX_ENABLE_SHARED"] = False

            #tc.cache_variables["BOOTSTRAP_LIBCXXABI_USE_LLVM_UNWINDER"] = False

        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_script_folder="./llvm-project/llvm")
        cmake.build()

    def package(self):
        cmake = CMake(self)

        # Copy the folder
        #shutil.copytree(
        #    os.path.join(self.build_folder, "tools", "clang", "stage2-bins"), 
        #    os.path.join(self.build_folder, "..", "..", "..", str(self.settings.os), str(self.settings.arch), "stage2", str(self.settings.build_type))
        #)

        # When meet "cmake not found", run this line in layout
        #cmake_layout(self, src_folder="./source", build_folder=os.path.join("./build", str(self.settings.os), str(self.settings.arch), "stage2"))
        cmake.install()

    def package_id(self):
        del self.info.settings.compiler
        del self.info.settings.build_type

    def package_info(self):
        #self.cpp_info.includedirs = ['include']
        #self.cpp_info.libdirs = ['lib']
        self.cpp_info.bindirs = ['bin']

        #self.buildenv_info.prepend_path("LIBRARY_PATH", self.cpp_info.libdirs[0])
        #self.buildenv_info.prepend_path("LD_LIBRARY_PATH", self.cpp_info.libdirs[1])
        #self.buildenv_info.prepend_path("LD_PATH", self.cpp_info.bindirs[0])
 
        #self.runenv_info.prepend_path("LIBRARY_PATH", self.cpp_info.libdirs[0])
        #self.runenv_info.prepend_path("LD_LIBRARY_PATH", self.cpp_info.libdirs[1])
        #self.runenv_info.prepend_path("LD_PATH", self.cpp_info.bindirs[0])
        #self.runenv_info.prepend_path("PATH", self.cpp_info.bindirs[0])
        #if self.settings.os == "Linux" or self.settings.os == "Linux":

        self.buildenv_info.prepend_path("PATH", self.cpp_info.bindirs[0])
        self.buildenv_info.define("LLVM_ROOT", os.path.join(self.package_folder))