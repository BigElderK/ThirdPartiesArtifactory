https://docs.conan.io/2/tutorial/developing_packages/local_package_development_flow.html

# Step 1: Prepare sources
conan source .

# Step 2: Install dependencies
conan install .

# Step 3: Build
conan build . --profile:build=../conan_linux_build_profile.txt --profile:host=../conan_linux_host_profile.txt
conan build . --profile:build=../conan_windows_build_profile.txt --profile:host=../conan_windows_host_profile.txt

# Step 4: Export to cache
conan export-pkg .

# Step 5: Check local conan cache
conan list

# Step 6: Upload to remote repo
conan upload "*" -r=divineland