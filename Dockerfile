FROM python:2.7

MAINTAINER Samuel Gratzl <samuel.gratzl@datavisyn.io>

# install node
RUN curl -sL https://deb.nodesource.com/setup_6.x | bash -
RUN apt-get install -y nodejs

EXPOSE 9000
CMD ["python", "phovea_processing_queue"]

WORKDIR /phovea

# install dependencies last step such that everything before can be cached
COPY requirements*.txt docker_packages.txt ./
RUN pip install --no-cache-dir -r requirements.txt && (pip install --no-cache-dir -r requirements_dev.txt) && (!(test -f docker_packages.txt) || (cat docker_packages.txt | xargs apt-get install -y))