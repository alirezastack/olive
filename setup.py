from setuptools import setup, find_packages

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(name='olive',
      version='0.0.11',
      description='Olive, a utility library shared across all services',
      long_description=LONG_DESCRIPTION,
      long_description_content_type='text/markdown',
      url='https://git.zoodroom.com/basket/olive',
      author='Sayyed Alireza Hoseini',
      author_email='alireza.hosseini@zoodroom.com',
      license='unlicensed',
      packages=find_packages(exclude=['ez_setup', 'tests*']),
      package_data={'olive': ['proto/*.proto']},
      include_package_data=True,
      install_requires=[
            'grpcio==1.20.1',
            'grpcio-tools==1.20.1',
            'protobuf==3.7.1',
            'retry==0.9.2',
            'pymongo==3.8.0',
            'marshmallow==3.0.0rc6',
      ]
      )
