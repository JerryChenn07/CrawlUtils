from setuptools import setup, find_packages

# https://mp.weixin.qq.com/s/SyMRQ6KUDTGLB9Px9oBPIg
# https://github.com/Gerapy/GerapyAutoExtractor/blob/master/setup.py
# https://github.com/kingname/GeneralNewsExtractor/blob/master/setup.py
setup(
    name='crawl_utils',
    version='0.1.4',
    description='Commonly Used Crawl Utils',
    author='cjr',
    author_email='cjr0707@qq.com',
    python_requires='>=3.6.0',
    url='https://github.com/cjr0707/CrawlUtils',
    packages=find_packages(exclude=[]),
    install_requires=['parsel'],
    include_package_data=True,
    license='MIT',
)
