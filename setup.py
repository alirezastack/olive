from setuptools import setup, find_packages

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

with open('requirements.txt') as f:
      requirements = [r for r in f.read().splitlines() if r and not r.startswith(('#', 'flake8', 'coverage'))]

setup(name='olive',
      version='0.0.22',
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
      install_requires=requirements
      )
