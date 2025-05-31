#!/bin/bash
# https://stackoverflow.com/questions/69719363/httpsconnectionpool-error-when-trying-to-install-gtest-with-conan
# https://github.com/conan-io/conan/issues/9695
# conan config install https://github.com/conan-io/conanclientcert.git

conan install $DEV_THIRD_PARTIES_ROOT_PATH/conan/conanfile.macos.txt --update --output-folder $DEV_THIRD_PARTIES_ROOT_PATH/conan/_generated/macos -pr:h=$DEV_THIRD_PARTIES_ROOT_PATH/../build_env/conan/profiles/host/conan_host_profile.macos.txt --build=missing 
conan install $DEV_THIRD_PARTIES_ROOT_PATH/conan/conanfile.ubuntu.txt --update --output-folder $DEV_THIRD_PARTIES_ROOT_PATH/conan/_generated/ubuntu -pr:h=$DEV_THIRD_PARTIES_ROOT_PATH/../build_env/conan/profiles/host/conan_host_profile.ubuntu.txt --build=missing
conan install $DEV_THIRD_PARTIES_ROOT_PATH/conan/conanfile.android.txt --update --output-folder $DEV_THIRD_PARTIES_ROOT_PATH/conan/_generated/android -pr:h=$DEV_THIRD_PARTIES_ROOT_PATH/../build_env/conan/profiles/host/conan_host_profile.android.txt --build=missing
conan install $DEV_THIRD_PARTIES_ROOT_PATH/conan/conanfile.raspberry64.txt --update --output-folder $DEV_THIRD_PARTIES_ROOT_PATH/conan/_generated/raspberry64 -pr:h=$DEV_THIRD_PARTIES_ROOT_PATH/../build_env/conan/profiles/host/conan_host_profile.raspberry64.txt --build=missing