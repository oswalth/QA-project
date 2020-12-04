FROM jenkins/jenkins:lts
USER root
ENV TZ=Europe/Moscow

RUN apt-get update
RUN apt-get install -y gcc build-essential checkinstall

RUN apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev \
    libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev

RUN mkdir -p /opt/python38
RUN cd /opt/python38
RUN wget https://www.python.org/ftp/python/3.8.2/Python-3.8.2.tgz
RUN tar xzf Python-3.8.2.tgz && cd Python-3.8.2 && ./configure --enable-optimizations && make altinstall

RUN rm -rf /opt/python38

RUN pip3.8 install --upgrade pip
RUN pip3.8 install pytest allure-pytest