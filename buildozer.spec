[app]
title = AI Plant Doctor
package.name = aiplantdoctor
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,jpeg,txt,keras,h5

version = 0.1
requirements = python3,kivy,kivymd,requests,numpy,tensorflow-lite,pillow,plyer
android.permissions = INTERNET,CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

[buildozer]
log_level = 2