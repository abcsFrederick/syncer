from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'girder>=3',
    'pyinotify'
]

setup(
    author='Tianyi Miao',
    author_email='tymiao1220@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    description='Girder v3 adaptation of Syncer',
    install_requires=requirements,
    license='Apache Software License 2.0',
    long_description=readme,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='girder-plugin, syncer_girder3',
    name='girder-syncer',
    packages=find_packages(exclude=['plugin_tests']),
    url='https://github.com/abcsFrederick/syncer',
    version='0.1.0',
    zip_safe=False,
    entry_points={
        'girder.plugin': [
            'syncer = girder_syncer:SyncerPlugin'
        ]
    }
)
