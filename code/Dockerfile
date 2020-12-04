FROM python:3.8
MAINTAINER Vladimir Carpa 'oswalth2@gmail.com'

COPY . /code
WORKDIR /code

RUN pip install -r code/requirements.txt
CMD ["ls"]

#CMD ["pytest", "--alluredir", "./allure-results", "--selenoid", "http://selenoid:4444/wd/hub/", "./tests"]