from setuptools import setup
import rumps

APP = ['main.py']  # 主程序文件
DATA_FILES = ['app_icon.icns']  # 需打包的额外文件（如图标）
OPTIONS = {
    'argv_emulation': False,
    'plist': {
        'CFBundleName': 'Eye Care',
        'CFBundleShortVersionString': '1.0',
        'LSUIElement': True  # 隐藏Dock图标（rumps应用需要）
    },
    'packages': ['rumps'],  # 确保打包包含rumps库
    'iconfile': 'app_icon.icns' # 指定应用程序图标
}


setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app']
)