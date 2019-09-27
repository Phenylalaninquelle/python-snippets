import setuptools

with open('README.md', 'r') as f:
    long_desc = f.read()

setuptools.setup(
    name = 'pysnips',
    version = '0.1',
    author = 'Jan Kiene',
    author_email = 'jankiene@mailbox.org',
    description = 'Collection of small python snippets',
    long_description = long_desc,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/phenyque/python-snippets',
    packages = setuptools.find_packages(),
    python_requires='>=3.5'
)
