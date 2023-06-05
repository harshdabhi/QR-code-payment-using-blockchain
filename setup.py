from setuptools import find_packages,setup

def get_requirements():
    with open('requirements.txt','r+') as f:
        p=f.read()
        list_req=p.split('\n')
    return list_req


setup(

    name='pulse_pay',
    version='0.0.1',
    author='harsh_dabhi',
    packages=find_packages(),
    install_require=get_requirements()
    

)