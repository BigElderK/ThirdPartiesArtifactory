from conan import ConanFile
from conan.tools.files import download, copy
from conan.tools.scm import Version
import os

class MSVCBuildToolsConan(ConanFile):
    name = "msvc_build_tools"
    version = "14.43.34808"  # Update this to match the MSVC version you want
    settings = "os", "arch"
    description = "MSVC Build Tools package for Conan"
    url = "https://github.com/yourusername/msvc_build_tools"
    license = "MIT"
    topics = ("msvc", "build-tools", "c++")
    package_type = "application"

    # def build_requirements(self):
        # Ensure we have 7-Zip to extract the installer if needed
        # self.tool_requires("7z/19.00")

    def layout(self):
        self.msvc_build_folder = "./build"
        self.msvc_download_folder = "download"
        self.installer_file = os.path.join(self.msvc_download_folder, "vs_BuildTools.exe")
        
    def source(self):
        # Download the Visual Studio Build Tools bootstrapper
        download(
            self,
            url="https://aka.ms/vs/17/release/vs_BuildTools.exe",
            filename = self.installer_file
        )

    def build(self):
        # Run the silent installation
        install_path = os.path.abspath(os.path.join(self.msvc_build_folder, "msvc_build_tools"))
        installer_file = self.installer_file

        command = (
            f"{installer_file} --nocache --wait "
            f"--add Microsoft.VisualStudio.Workload.VCTools "
            f"--add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 "
            f"--add Microsoft.VisualStudio.Component.VC.Tools.ARM "
            f"--add Microsoft.VisualStudio.Component.VC.Tools.ARM64 "
            f"--installPath {install_path}"
        )

        self.run(command)

    def package(self):
        # Copy the installed MSVC Build Tools to the package folder
        install_path = os.path.join(self.build_folder, "msvc_build_tools")
        copy(self, "*", src=install_path, dst=os.path.join(self.package_folder, "msvc_build_tools"))

    def package_info(self):
        # Set environment variables for the MSVC tools
        msvc_path = os.path.join(self.package_folder, "msvc_build_tools", "VC", "Tools", "MSVC", self.version)
        self.buildenv_info.append_path("PATH", os.path.join(msvc_path, "bin", "Hostx64", "x64"))
        self.buildenv_info.define("CC", os.path.join(msvc_path, "bin", "Hostx64", "x64", "cl.exe"))
        self.buildenv_info.define("CXX", os.path.join(msvc_path, "bin", "Hostx64", "x64", "cl.exe"))
        self.buildenv_info.define("CMAKE_GENERATOR", "Visual Studio 17 2022")

    def package_id(self):
        # Ensure the package is specific to the OS and architecture
        self.info.settings.os = "Windows"
        self.info.settings.arch = "x86_64"