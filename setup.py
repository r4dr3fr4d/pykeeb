from setuptools import setup

setup(name='pykeeb',
      version='0.1',
      description='Python library to help generate OpenSCAD models of mechanical keyboard plates.',
      url='http://github.com/raycewest/pykeeb',
      author='Rayce West',
      author_email='rwest@g.clemson.edu',
      license='MIT',
      packages=['pykeeb'],
      data_files=[('./models',['pykeeb/models/cherry.stl','pykeeb/models/matias.stl','pykeeb/models/dsa_1u.stl'])],
      zip_safe=False)
