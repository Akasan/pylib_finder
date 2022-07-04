from setuptools import setup, find_packages


setup(name="pylib_finder",
	version="1.0",
	packages=[
        "pylib_finder",
    ],
    entry_points={
        "console_scripts":[
            "pylib_finder=pylib_finder.pylib_finder:main"
        ]
    }
)

