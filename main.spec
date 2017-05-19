# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\xuning\\AppData\\Local\\Programs\\Python\\Python36\\Lib\\site-packages\\PyQt5\\Qt\\bin'],
             binaries=[],
             datas=[('Resource', 'Resource')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='BannerFactory',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='icon.ico')
app = BUNDLE(exe,
             name='BannerFactory.app',
             icon='icon.icns',
             bundle_identifier='com.XuNing.BannerFactory',
             info_plist={
                    'NSHighResolutionCapable': 'True',
                    'CFBundleDevelopmentRegion': 'zh-CN',
                    'CFBundleShortVersionString': '1.1.0',
                    'NSHumanReadableCopyright': 'Copyright © 2017年 XuNing. All rights reserved.',
                }
             )
