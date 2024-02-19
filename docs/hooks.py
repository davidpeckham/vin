import shutil


def copy_docs(*args, **kwargs):
    shutil.copy("CHANGELOG.md", "docs/changelog.md")
    shutil.copy("README.md", "docs/index.md")
