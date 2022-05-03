FROM python:3.8-slim

ENV DEBUG=1
ENV ECHO_ACTIVE=1
ENV APP_AUTH_TOKEN=Pm3GF4q8_1ewABEn-m88nL7w_mErBqs5ESeVx9BUUkY
ENV APP_AUTH_TOKEN_PROD=ncVY2JpEAvEx1QNABBs863sihto8GB3hL61bZZn1dG4
ENV SKIP_AUTH=1

COPY ./entrypoint.sh /entrypoint.sh
COPY ./app /app
COPY ./requirements.txt /requirements.txt

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        python3-dev \
        python3-setuptools \
        tesseract-ocr \
        make \
        gcc \
    && python3 -m pip install -r requirements.txt \
    && apt-get remove -y --purge make gcc build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
