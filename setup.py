from setuptools import find_packages, setup

setup(
    name='sysbio_wiki_wordcloud',
    version='1.1.1',
    description="Making a word cloud from Dr. Christine Vogel's Systems Biology Wiki.",
    author="Che-Lun Juang",
    entry_points={
        'console_scripts': [
            'sysbio-wiki-wordcloud = sysbio_wiki_wordcloud.__main__:main',
        ],
    },
    license="MIT",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=['docs']),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'matplotlib',
        'Pillow',
        'wordcloud',
        'lxml'
    ],
    include_package_data=True,
    package_data={
        'sysbio_wiki_wordcloud': ['stopwords']
    }
)
