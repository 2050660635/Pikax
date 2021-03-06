# -*- mode: python ; coding: utf-8 -*-

spec_path = os.path.dirname(os.path.abspath(SPEC))
block_cipher = None


a = Analysis(['main.py'],
             pathex=['D:\\University of Manchester\\Projects\\Pikax\\gui'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += [('/assets/images/background.jpg', './assets/images/background.jpg', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Pikax DEBUG',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          icon=f'{spec_path}/assets/images/pikax_icon.ico')
