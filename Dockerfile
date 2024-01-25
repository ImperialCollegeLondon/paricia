FROM python:3.11-buster as python

FROM python

# ssh
RUN apt-get update && apt-get install -y dos2unix
COPY utilities/install_ssh.sh .
RUN dos2unix /install_ssh.sh
RUN chmod u+x install_ssh.sh
RUN ./install_ssh.sh
COPY utilities/sshd_config /etc/ssh/

# Initialization
COPY utilities/init.sh /usr/local/bin/
RUN chmod u+x /usr/local/bin/init.sh
RUN dos2unix /usr/local/bin/init.sh
CMD ["/usr/local/bin/init.sh"]

# django
COPY requirements.txt .
COPY requirements-dev.txt .
RUN apt-get update && apt-get install -y --no-install-recommends libmagic1 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN mkdir log
RUN python manage.py collectstatic --no-input

# 8000 for the web and 2222 for ssh
EXPOSE 8000 2222
