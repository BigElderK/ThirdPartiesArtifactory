https://docs.conan.io/2/tutorial/developing_packages/local_package_development_flow.html

# Step 1: Prepare sources
conan source .

# Step 2: Install dependencies
conan install .

# Step 3: Build
conan build . --profile=../conan_linux_profile.txt 
conan build . --profile=../conan_windows_profile.txt 

# Step 4: Export to cache
conan export-pkg . --profile=../conan_linux_profile.txt 
conan export-pkg . --profile=../conan_windows_profile.txt 

# Step 5: Check local conan cache
conan list

# Step 6: Upload to remote repo
conan upload "*" -r=divineland

# Issues
- When meet timeout when upload, add "core.net.http:timeout = 600000" to global.conf under ~/.conan2/

# Test
E:\BigElderK\.conan\p\b\llvmdf2f067e920ff\p\bin\clang++.exe -isystem "E:\BigElderK\.conan\p\b\llvmdf2f067e920ff\p\include\c++\v1" -L"E:\BigElderK\.conan\p\b\llvmdf2f067e920ff\p\lib" -llibc++ -stdlib=libc++ -o test.o -c test.cpp -Xclang --dependent-lib=libcpmt
E:\BigElderK\.conan\p\b\llvmdf2f067e920ff\p\bin\clang++.exe -fuse-ld=lld test.o -o test.exe -L'E:\BigElderK\.conan\p\b\llvmdf2f067e920ff\p\lib' -llibc++
E:\BigElderK\.conan\p\b\llvmdf2f067e920ff\p\bin\clang.exe -o test.exe test.cpp -Xclang -std=c++17 -Xclang -stdlib=libc++

# sys_root
docker run -it --name sysroot-ubuntu-22_04 ubuntu:22.04
apt update
apt install build-essential clang lld 
apt install libc6-dev libc++-dev libc++abi-dev
docker export sysroot-ubuntu-22_04 -o E:\BigElderK\wsl\sysroot-ubuntu-22_04.tar

clang++ --target=x86_64-linux-gnu -o test test.cpp -fuse-ld=lld -std=c++17 -stdlib=libc++ --sysroot=/home/k/ttt/sysroot-ubuntu-amd64-stable -v

E:\BigElderK\.conan\p\b\llvmdf2f067e920ff\p\bin\clang++.exe --target=x86_64-pc-linux-gnu -o test test.cpp -fuse-ld=lld -std=c++17 -stdlib=libc++ --sysroot=E:/BigElderK/wsl/sysroot-ubuntu-amd64-stable -v -L/lib/x86_64-linux-gnu "E:/BigElderK/wsl/sysroot-ubuntu-amd64-stable/lib/llvm-14/lib/libc++.a"


