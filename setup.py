from setuptools import setup, find_packages

version = '0.1'

setup(name='chut',
      version=version,
      description="Small tool to interact with shell pipes",
      long_description=open('README.rst').read(),
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: POSIX',
          'Programming Language :: Unix Shell',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          ],
      keywords='sh shell bash',
      author='Gael Pasgrimaud',
      author_email='gael@gawel.org',
      url='https://github.com/gawel/chut/',
      license='MIT',
      py_modules=['chut'],
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      )