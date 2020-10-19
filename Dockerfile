FROM python:3.8.3

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
                    gcc \
                    libsasl2-dev \
                    python3-dev \
                    libldap2-dev \
                    libssl-dev \
                    default-libmysqlclient-dev \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ADD requirements.txt .

RUN pip3 install -r requirements.txt
