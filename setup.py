from setuptools import setup, find_packages

# 参考
# https://mp.weixin.qq.com/s/SyMRQ6KUDTGLB9Px9oBPIg
# https://github.com/Gerapy/GerapyAutoExtractor/blob/master/setup.py
# https://github.com/kingname/GeneralNewsExtractor/blob/master/setup.py

def read_file(filename):
    with open(filename) as fp:
        return fp.read().strip()


def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


REQUIRED = read_requirements('requirements.txt')

setup(
    name='crawl_utils',
    version='0.2.1',
    description='Commonly Used Crawl Utils',
    author='cjr',
    author_email='cjr0707@qq.com',
    python_requires='>=3.6.0',
    url='https://github.com/cjr0707/CrawlUtils',
    packages=find_packages(exclude=[]),
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
)
