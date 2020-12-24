from setuptools import setup, find_packages
from setuptools.command.install import install
import setuptools

from pickle5_wheels_helper import try_install_pickle5


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        try_install_pickle5()
        try:
            import pickle5
        except Exception as e:
            raise Exception("pickle5 setup failed!") from e


setup(
    name="pickle5-wheels-helper",
    version="0.0.6",
    author="Siyuan Zhuang",
    author_email="suquark@gmail.com",
    description="Helper package for installing pickle5 wheels",
    url="https://github.com/suquark/pickle5-wheels-helper",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    license="Apache 2.0",
    cmdclass={"install": PostInstallCommand},
)
