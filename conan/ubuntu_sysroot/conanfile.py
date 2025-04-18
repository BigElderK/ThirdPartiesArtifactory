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
        self.output_folder = os.path.join(".", "build")

        self.output_sysroot_folder = os.path.join(self.output_folder, self.system_name, "sysroot")

        self.linux_arch_name = f"{self.settings.arch}-linux-gnu"
        return

    def source(self):
        self.run("docker pull ubuntu:%s" % (self.version))
        return
        
    def generate(self):
        return
    
    def build(self):        
        self.run(f"docker rm -f {self.docker_instance_name}")
        self.run(f"docker run -d --name {self.docker_instance_name} ubuntu:{self.version} tail -f /dev/null")
        self.run(f"docker exec -it {self.docker_instance_name} apt update -y")
        self.run(f"docker exec -it {self.docker_instance_name} apt upgrade -y")
        #self.run(f"docker exec -it {self.docker_instance_name} env DEBIAN_FRONTEND=\"noninteractive\" apt install -y build-essential clang lld ")

        self.gcc_package_name = f"gcc-{self.settings.arch}-linux-gnu".replace('_', '-')
        self.run(f"docker exec -it {self.docker_instance_name} apt install -y libc6-dev libc++-dev libc++abi-dev {self.gcc_package_name}")

        self.run(f"docker exec -it {self.docker_instance_name} sh -c \"find /usr/lib/{self.linux_arch_name}/ -type l -xtype f > /tmp/file_links.txt\"")
        self.run(f"docker exec -it {self.docker_instance_name} sh -c \"xargs -a /tmp/file_links.txt" + " -I{} readlink -f {} > /tmp/file_src.txt\"")
        self.run(f"docker exec -it {self.docker_instance_name} sh -c \"paste /tmp/file_src.txt /tmp/file_links.txt | xargs -n 2 cp -r --remove-destination\"")
        self.run(f"docker exec -it {self.docker_instance_name} sh -c \"paste /tmp/file_src.txt /tmp/file_links.txt | xargs -n 2 cp -r --remove-destination\"")

        if not os.path.exists(self.output_sysroot_folder):
            os.makedirs(self.output_sysroot_folder)
        if not os.path.exists(os.path.join(self.output_sysroot_folder, "usr")):
            os.makedirs(os.path.join(self.output_sysroot_folder, "usr"))
            
        self.run(f"docker cp {self.docker_instance_name}:/usr/lib {self.output_sysroot_folder}/")
        self.run(f"docker cp {self.docker_instance_name}:/usr/lib64 {self.output_sysroot_folder}/")
        self.run(f"docker cp {self.docker_instance_name}:/usr/include {self.output_sysroot_folder}/usr")
        self.run(f"docker cp {self.docker_instance_name}:/usr/lib {self.output_sysroot_folder}/usr")
        self.run(f"docker cp {self.docker_instance_name}:/usr/lib64 {self.output_sysroot_folder}/usr")

        self.run(f"docker rm -f {self.docker_instance_name}")
        return

    def package(self):
        copy(self, "*", src=self.output_sysroot_folder, dst=os.path.join(self.package_folder, self.system_name, "sysroot"), keep_path=True)
        return

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []

        self.conf_info.define_path("tools.build:sysroot", os.path.join(self.package_folder, self.system_name, "sysroot"))

        # for cxxabi, libuwind
        self.conf_info.append("tools.build:cxxflags", f"-I" + os.path.join(self.package_folder, self.system_name, "sysroot", "usr", "lib", "llvm-19", "include").replace('\\', '/'))

        # for libc++.so, etc automatically
        # self.conf_info.append("tools.build:exelinkflags", f"-L" + os.path.join(self.package_folder, self.system_name, "sysroot", "usr", "lib", f"{self.linux_arch_name}").replace('\\', '/'))
        # self.conf_info.append("tools.build:sharedlinkflags", f"-L" + os.path.join(self.package_folder, self.system_name, "sysroot", "usr", "lib", f"{self.linux_arch_name}").replace('\\', '/'))
        
        return
