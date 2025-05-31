#!/bin/bash
BUILD_ENV_CONAN_ROOT_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# https://stackoverflow.com/questions/69719363/httpsconnectionpool-error-when-trying-to-install-gtest-with-conan
# https://github.com/conan-io/conan/issues/9695
# conan config install https://github.com/conan-io/conanclientcert.git

conan profile detect --force
conan install $BUILD_ENV_CONAN_ROOT_PATH/conanfile.txt --update --generator CMakeToolchain --output-folder $BUILD_ENV_CONAN_ROOT_PATH/_generated/host/macos --build never --profile=$BUILD_ENV_CONAN_ROOT_PATH/profiles/host/conan_host_profile.macos.txt
conan install $BUILD_ENV_CONAN_ROOT_PATH/conanfile.txt --update --generator CMakeToolchain --output-folder $BUILD_ENV_CONAN_ROOT_PATH/_generated/host/ubuntu --build never --profile=$BUILD_ENV_CONAN_ROOT_PATH/profiles/host/conan_host_profile.ubuntu.txt
conan install $BUILD_ENV_CONAN_ROOT_PATH/conanfile.txt --update --generator CMakeToolchain --output-folder $BUILD_ENV_CONAN_ROOT_PATH/_generated/host/android --build never --profile=$BUILD_ENV_CONAN_ROOT_PATH/profiles/host/conan_host_profile.android.txt
conan install $BUILD_ENV_CONAN_ROOT_PATH/conanfile.txt --update --generator CMakeToolchain --output-folder $BUILD_ENV_CONAN_ROOT_PATH/_generated/host/raspberry64 --build never --profile=$BUILD_ENV_CONAN_ROOT_PATH/profiles/host/conan_host_profile.raspberry64.txt