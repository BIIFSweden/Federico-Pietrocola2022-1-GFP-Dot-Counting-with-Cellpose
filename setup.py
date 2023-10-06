from setuptools import setup
from setuptools import find_packages

setup(
    name="Senolytic-Dot-Counting",
    verion="0.1.1",
    description="A program to count fluorescent markers in images of cells",
    py_modules=[
        "functions",
        "get_user_inputs",
        "run_analysis",
    ],
    package_dir={"": "src"},
    author_email="robert.welch@scilifelab.se",
    author="Robert Welch",
    url="https://github.com/BIIFSweden/Senolytic-Dot-Counting",
    packages=find_packages(","),
    install_requires=[
        "matplotlib",
        "numpy",
        "cellpose",
        "nd2reader",
        "pandas",
        "psutil",
        "scikit-image",
        "tk",
        "openpyxl",
    ],
)
