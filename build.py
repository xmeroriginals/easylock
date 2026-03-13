import PyInstaller.__main__
import os
import sys
import platform

base_path = os.path.dirname(os.path.abspath(__file__))
args = [
    'run.py',
    '--name=EasyLock',
    '--onefile',
    '--windowed',
    '--add-data=' + os.path.join(base_path, 'resources') + os.pathsep + 'resources',
    '--clean',
]

if platform.system() == 'Windows':
    args.append('--icon=' + os.path.join(base_path, 'resources', 'logotwo.ico'))
elif platform.system() == 'Linux':
    args.extend(['--hidden-import=dbus'])

if __name__ == "__main__":
    print(f"Building EasyLock executable for {platform.system()}...")
    try:
        PyInstaller.__main__.run(args)
        print("\n" + "="*50)
        print(f"BUILD SUCCESSFUL!")
        print(f"Executable found in: {os.path.join(base_path, 'dist')}")
        print("="*50)
    except Exception as e:
        print(f"Build failed: {e}")
