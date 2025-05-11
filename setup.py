from setuptools import setup, find_packages

setup(
    name="piv_2025",
    version="0.0.1",
    author="Maria Usuga",
    author_email="",
    description="",
    py_modules=["actividad_1","actividad_2"],
    install_requires=[
        "seaborn>=0.11.2",
        "pandas==2.2.3",
        "numpy",
        "openpyxl",
        "requests==2.32.3",
        "beautifulsoup4==4.13.3",
        "scikit-learn>=0.24.0"
    ]
) 