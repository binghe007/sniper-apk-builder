[app]
title = IP狙击
package.name = ipsniper
package.domain = org.yourname
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,pyx
version = 0.1
requirements = python3,kivy==2.2.1,kivymd==1.1.1,requests,urllib3,charset_normalizer,idna,cython
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.2.1
fullscreen = 0
android.permissions = INTERNET
android.arch = arm64-v8a
android.api = 31
android.minapi = 21
android.ndk = 25b
android.gradle_dependencies = 'androidx.appcompat:appcompat:1.6.1'
android.add_src = 
android.sdk_path = 
android.ndk_path = 
android.ant_path = 
ios.kivy_version = 2.2.1
ios.requirements = 
p4a.source_dir = .
p4a.local_recipes = .
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1