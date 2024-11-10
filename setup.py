from setuptools import setup, find_packages

setup(
    name="hogwarts_assistant",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "prompt-toolkit==3.0.36",
        "questionary==2.0.1",
        "wcwidth==0.2.13",
        "rapidfuzz===3.9.6",
        "colorama==0.4.6",
    ],
    entry_points={
        "console_scripts": [
            "hogwarts=hogwarts.main:main",
        ],
    },
    author="Hogwarts Team",
    author_email="stronglav95@gmail.com",
    description="A Hogwarts-themed assistant for managing pupil records and magical notes.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Srh-Yakovenko-ua/hogwarts_team_7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12.4",
)
