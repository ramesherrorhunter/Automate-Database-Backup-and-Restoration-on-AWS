ARG FUNCTION_DIR="/home/app"

FROM python:slim-buster

ARG FUNCTION_DIR
RUN mkdir -p ${FUNCTION_DIR}
COPY *.py ${FUNCTION_DIR}

RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev

RUN python3 -m pip install awslambdaric boto3 pymysql cursor

RUN python3 -m pip install \ 
  awscli

RUN apt-get update && apt-get install -y mariadb-client && \
  apt-get clean autoclean && \
  apt-get autoremove --yes && \
  rm -rf /var/lib/{apt,dpkg,cache,log}/

WORKDIR ${FUNCTION_DIR}
ENTRYPOINT [ "/usr/local/bin/python3", "-m", "awslambdaric" ]
CMD [ "lambda_function.lambda_handler" ]
