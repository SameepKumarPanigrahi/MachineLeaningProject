from typing import List
from setuptools import find_packages, setup

PROJECT_NAME="housing-predictor"
VERSION="0.0.1"
AUTHOR="Sameep"
DESCRIPTION="We will add it later"
# PACKAGES=["housing"] 
REQUIREMENTS_FILE_NAME="requirements.txt"

def get_requirements_list()->List[str]:
    """
    DESCRIPTION : 
    This function will return the all the requirements mentioned in the requirements.txt file as a list.
    """
    with open(REQUIREMENTS_FILE_NAME) as requirement_file:
        return requirement_file.readlines().remove("-e .")

setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    packages= find_packages(),
    install_requires=get_requirements_list()
)

# if __name__ == "__main__":
#     print(get_requirements_list())