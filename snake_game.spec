# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/assets', 'assets'),  # Include game assets
        ('docs', 'docs'),          # Include documentation
    ],
    hiddenimports=[
        'pygame',
        'pygame.locals',
        'pygame.display',
        'pygame.event',
        'pygame.key',
        'pygame.time',
        'pygame.mixer',
        'pygame.font',
        'pygame.draw',
        'pygame.rect',
        'pygame.surface',
        'pygame.image',
        'pygame.transform',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SnakeGame',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Set to True for debugging to see error messages
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # No icon for now to avoid build issues
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SnakeGame',
)
