from distutils.core import setup


setup(
    name = "testbench",
    version = "0.01.0dev",
    author = "startling",
    author_email = "tdixon51793@gmail.com",
    description = "a benchmarking library in the vein of unittest",
    packages = ["testbench"],
    scripts = ["scripts/testbench", "scripts/testbench-color"],
)
