FROM node:current-alpine3.17

RUN npm install elasticdump -g

COPY entrypoints.sh /

ADD dumps.tar.gz /dumps

ENTRYPOINT ["sh", "entrypoints.sh"]