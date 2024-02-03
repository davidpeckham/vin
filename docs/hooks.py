import shutil


def copy_history(*args, **kwargs):
    shutil.copy("CHANGELOG.md", "docs/changelog.md")
