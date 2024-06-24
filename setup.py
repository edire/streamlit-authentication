# setup.py placed at root directory
from setuptools import setup
setup(
    name='streamlit-authentication',
    packages=['streamlit_authentication'],
    version='0.1.0',
    license='MIT',
    author='Eric Di Re',
    author_email='eric.dire@direanalytics.com',
    description='Standardized Streamlit OAuth.',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url='https://github.com/edire/streamlit-authentication.git',
    python_requires='>=3.11',
    install_requires=['streamlit', 'extra-streamlit-components', 'google-auth-oauthlib', 'google-api-python-client']
)