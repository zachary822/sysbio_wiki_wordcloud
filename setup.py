from setuptools import setup, find_packages

setup(
    name='sysbio_wiki_wordcloud',
    version='1.0.0',
    description="Making a word cloud from Dr. Christine Vogel's Systems Biology Wiki.",
    author="Che-Lun Juang",
    entry_points={
        'console_scripts': [
            'sysbio_wiki_wordcloud=sysbio_wiki_wordcloud.__main__:main',
        ],
    },
    license="MIT",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages()
)
