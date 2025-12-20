import PyInstaller.__main__
import os
import sys
import platform

# Get the path to the current directory
base_path = os.path.dirname(os.path.abspath(__file__))

# Define the arguments for PyInstaller
args = [
    'run.py',  # Entry point
    '--name=EasyLock',
    '--onefile',
    '--windowed',
    # Add resources folder (icons, fonts etc)
    '--add-data=' + os.path.join(base_path, 'resources') + os.pathsep + 'resources',
    '--clean',
]

# Platform-specific adjustments
if platform.system() == 'Windows':
    args.append('--icon=' + os.path.join(base_path, 'resources', 'logotwo.ico'))
elif platform.system() == 'Linux':
    # Linux doesn't embed icons in the same way, but we can ensure dependencies are handled
    # On Linux, hidden imports might be needed for some DBus integrations
    args.extend(['--hidden-import=dbus'])

# Run PyInstaller
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
