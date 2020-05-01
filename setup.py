from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name='SpoofDogg',
    version='1.0',
    description='A tool that does ARP poisoning and DNS spoofing.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires="~=3.5",
    url='',
    license='Apache',
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    author='Ada Donder',
    author_email='adadonderr@gmail.com',
    keywords="ARP, DNS, spoof, poison, gateway",
    install_requires=['scapy', 'netfilterqueue']
)