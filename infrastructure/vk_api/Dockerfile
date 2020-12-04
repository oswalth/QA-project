FROM python:3.8
MAINTAINER Vladimir Carpa 'oswalth2@gmail.com'


COPY . /vk_api
WORKDIR /vk_api

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["vk_app.py"]