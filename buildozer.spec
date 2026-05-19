[app]
title = IP狙击
package.name = ipsniper
package.domain = org.yourname
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,pyx
version = 0.1
requirements = python3,kivy==2.2.1,kivymd==1.1.1,requests,urllib3,charset_normalizer,idna,cython
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.archs = arm64-v8a
android.api = 30
android.minapi = 21
android.ndk = 23c
android.build_tools_version = 30.0.3
android.gradle_dependencies = 'androidx.appcompat:appcompat:1.6.1'
android.skip_update = 1
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1