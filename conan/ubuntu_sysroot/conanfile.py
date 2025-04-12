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
    name = "ubuntu_sysroot"
    version = "24.10"
    topics = ("sysroot", "build", "installer")
    settings = "arch"
    
    default_user = "arieo"
    default_channel = "dev"

    def layout(self):
        self.system_name = f"ubuntu-{self.version}-{self.settings.arch}"
        self.docker_instance_name = f"conan-{self.system_name}"
        self.output_folder = os.path.join(".", "build", str(self.settings.arch))

        self.output_tar_file_path = os.path.join(self.output_folder, self.system_name) + ".tar"
        self.output_sysroot_folder = os.path.join(self.output_folder, self.system_name, "sysroot")
        return

    def source(self):
        self.run("docker pull ubuntu:%s" % (self.version))
        return
        
    def generate(self):
        return
    
    def build(self):        
        self.run(f"docker run -d --name {self.docker_instance_name} ubuntu:{self.version} tail -f /dev/null")
        self.run(f"docker exec -it {self.docker_instance_name} apt update -y")
        self.run(f"docker exec -it {self.docker_instance_name} apt upgrade -y")
        self.run(f"docker exec -it {self.docker_instance_name} env DEBIAN_FRONTEND=\"noninteractive\" apt install -y build-essential clang lld ")
        self.run(f"docker exec -it {self.docker_instance_name} apt install -y libc6-dev libc++-dev libc++abi-dev")
        
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        self.run(f"docker export {self.docker_instance_name} -o {self.output_tar_file_path}")
        self.run(f"docker stop {self.docker_instance_name}")
        self.run(f"docker rm {self.docker_instance_name}")

        # extra tar to sysroot folder        
        with tarfile.open(self.output_tar_file_path) as tar:
            members = tar.getmembers()
            total = len(members)
            for i, member in enumerate(members, 1):
                print(f"Extracting {i}/{total}: {member.name}")
                tar.extract(member, self.output_sysroot_folder)

        return

    def package(self):
        copy(self, "*", src=self.output_sysroot_folder, dst=os.path.join(self.package_folder, self.system_name, "sysroot"), keep_path=True)

        rm(self, "lib", os.path.join(self.package_folder, self.system_name, "sysroot"))
        rm(self, "lib32", os.path.join(self.package_folder, self.system_name, "sysroot"))
        rm(self, "lib64", os.path.join(self.package_folder, self.system_name, "sysroot"))

        copy(self, "*", src=os.path.join(self.output_sysroot_folder, "usr", "lib"), dst=os.path.join(self.package_folder, self.system_name, "sysroot", "lib"), keep_path=True, overwrite_equal=True)
        copy(self, "*", src=os.path.join(self.output_sysroot_folder, "usr", "lib32"), dst=os.path.join(self.package_folder, self.system_name, "sysroot", "lib32"), keep_path=False, overwrite_equal=True)
        copy(self, "*", src=os.path.join(self.output_sysroot_folder, "usr", "lib64"), dst=os.path.join(self.package_folder, self.system_name, "sysroot", "lib64"), keep_path=False, overwrite_equal=True)

        # for ld-linux-x86-64.so.2
        rm(self, "ld-linux-x86-64.so.2", os.path.join(self.package_folder, self.system_name, "sysroot", "lib64"))
        copy(self, "ld-linux-x86-64.so.2", src=os.path.join(self.output_sysroot_folder, "usr", "lib", "x86_64-linux-gnu"), dst=os.path.join(self.package_folder, self.system_name, "sysroot", "lib64"), keep_path=False, overwrite_equal=True)

        rm(self, "clang", os.path.join(self.package_folder, self.system_name, "sysroot", "usr", "bin"))
        rm(self, "clang++", os.path.join(self.package_folder, self.system_name, "sysroot", "usr", "bin"))

        return

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []

        for root, dirs, files in os.walk(os.path.join(self.package_folder, self.system_name, "sysroot")):
            for file in files:
                if file == "cxxabi.h":
                    if root.find('llvm') != -1 and root.find('v1') == -1:
                        #print("found cxxabi.h in ", os.path.relpath(os.path.join(root, file), (self.output_sysroot_folder)))
                        self.cxxabi_h_folder = os.path.join(root)

        self.conf_info.define_path("tools.build:sysroot", os.path.join(self.package_folder, self.system_name, "sysroot"))
        self.conf_info.append("tools.build:cxxflags", f"-I{self.cxxabi_h_folder}".replace('\\', '/'))

        for root, dirs, files in os.walk(os.path.join(self.package_folder, self.system_name, "sysroot")):
            for file in files:
                if file == "libc++.so":
                    if root.find('llvm') != -1:
                        #print("found libc++.so in ", os.path.relpath(os.path.join(root, file), (self.output_sysroot_folder)))
                        self.libcxx_folder = os.path.join(root)

        self.conf_info.append("tools.build:exelinkflags", f"-L{self.libcxx_folder}".replace('\\', '/'))
        self.conf_info.append("tools.build:sharedlinkflags", f"-L{self.libcxx_folder}".replace('\\', '/'))

        #, "-LE:/BigElderK/.conan/p/b/ubunt67b60a8b8e630/p/ubuntu-24.10-x86_64/sysroot/usr/lib/llvm-19/lib"

        #self.cpp_info.bindirs = ['bin']
        #self.runenv_info.prepend_path("PATH", os.path.join(self.package_folder, "bin"))
        #self.buildenv_info.prepend_path("PATH", os.path.join(self.package_folder, "bin"))

        #self.runenv_info.append_path(os.path.join(self.package_folder, "bin"))
        #self.runenv_info.append_path("PATH", os.path.join(self.package_folder, "bin"))
        #self.buildenv_info.append_path("PATH", os.path.join(self.package_folder, "bin"))
        return
