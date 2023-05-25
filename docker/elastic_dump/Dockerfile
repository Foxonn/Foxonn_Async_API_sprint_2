FROM node

RUN npm install elasticdump -g \
    && apt install unzip

COPY dumps.zip /
COPY entrypoints.sh /

RUN unzip dumps.zip

ENTRYPOINT ["sh", "entrypoints.sh"]