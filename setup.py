from setuptools import setup, find_packages

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(name='olive',
      version='0.0.6',
      description='Olive, a utility library shared across all services',
      long_description=LONG_DESCRIPTION,
      long_description_content_type='text/markdown',
      url='http://sample.com/backend/olive',
      author='Sayyed Alireza Hoseini',
      author_email='alireza.hosseini@zoodroom.com',
      license='unlicensed',
      packages=find_packages(exclude=['ez_setup', 'tests*']),
      package_data={'olive': ['proto/*.proto']},
      include_package_data=True,
      )
