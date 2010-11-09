from setuptools import setup, find_packages

setup(
    name='django-carousel',
    version=__import__('carousel').__version__,
    description='Helpers to generate dynamic carousels.',
    author='Baptiste Mispelon',
    author_email='bmispelon@gmail.com',
    url='http://github.com/bmispelon/django-carousel',
    download_url='http://github.com/bmispelon/django-carousel/downloads',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False, # because we're including media that Django needs
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
