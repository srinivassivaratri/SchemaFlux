from pathlib import Path
import build
import build.util
import sys

def build_package():
    """Build both wheel and source distribution."""
    builder = build.ProjectBuilder(Path("."))
    builder.build(distribution='sdist', output_directory='dist')
    builder.build(distribution='wheel', output_directory='dist')

if __name__ == '__main__':
    build_package()
