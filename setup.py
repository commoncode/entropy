from setuptools import setup, find_packages

setup( name='entropy',
    version = '0.0.3',
    description = 'Base classes framework for modern Django projects',
    author = 'Daryl Antony',
    author_email = 'daryl@commoncode.com.au',
    url = 'https://github.com/commoncode/entropy',
    keywords = ['django',],
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires = [
        'Django>=1.4',
    ]
)