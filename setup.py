import re
import setuptools
from pathlib import Path

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Framework :: AsyncIO",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Communications",
    "Topic :: Internet",
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: System :: Networking",
    "Typing :: Typed",
]

extras_require = {
    "docs": [
        "sphinx",
        "sphinx-rtd-theme",
        "sphinxcontrib-trio",
    ],
    "dev": [
        "pytest",
        "pytest-asyncio",
        "mypy",
        "black",
        "isort",
        "flake8",
    ],
    "speed": [
        "aiohttp[speedups]",
        "cchardet",
        "aiodns",
    ],
}

install_requires = [
    "aiohttp",
    "typing-extensions;python_version<'3.11'",
    "py-cord",
]

packages = setuptools.find_packages(include=["pycord", "pycord.*"])

project_urls = {
    "Issue Tracker": "https://github.com/ParrotXray/pycord-localizer/issues",
    "Source": "https://github.com/ParrotXray/pycord-localizer",
}

_version_regex = r"^__version__ = ['\"]([^'\"]*)['\"]$"

init_file = Path("pycord/localizer/__init__.py")
if init_file.exists():
    with open(init_file, encoding="utf-8") as stream:
        match = re.search(_version_regex, stream.read(), re.MULTILINE)
        if match:
            version = match.group(1)
        else:
            raise RuntimeError("Cannot find version string in __init__.py")
else:
    version = "0.1.4"

if "dev" in version or "alpha" in version or "beta" in version or "rc" in version:
    try:
        import subprocess

        process = subprocess.Popen(
            ["git", "rev-list", "--count", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        out, _ = process.communicate()
        if out and process.returncode == 0:
            commit_count = out.decode("utf-8").strip()
            version += f".dev{commit_count}"

        process = subprocess.Popen(
            ["git", "rev-parse", "--short", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        out, _ = process.communicate()
        if out and process.returncode == 0:
            short_hash = out.decode("utf-8").strip()
            version += f"+g{short_hash}"

    except (Exception, FileNotFoundError):
        pass

readme_file = Path("README.md")
if readme_file.exists():
    with open(readme_file, encoding="utf-8") as f:
        long_description = f.read()
    long_description_content_type = "text/markdown"
else:
    long_description = "A pycord extension for internationalization and localization.."
    long_description_content_type = "text/plain"

setuptools.setup(
    name="pycord-localizer",
    version=version,
    author="ParrotXray",
    author_email="",
    description="A pycord extension for internationalization and localization.",
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    url="https://github.com/ParrotXray/pycord-localizer",
    project_urls=project_urls,
    packages=packages,
    classifiers=classifiers,
    python_requires=">=3.10",
    install_requires=install_requires,
    extras_require=extras_require,
    license="MIT",
    keywords="discord py-cord i18n internationalization localization l10n",
    include_package_data=True,
    zip_safe=False,
    package_data={
        "pycord.localizer": ["py.typed"],
    },
)