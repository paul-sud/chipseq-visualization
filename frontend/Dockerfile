FROM node:12.20.1-alpine3.12
WORKDIR /app
COPY package.json /app/package.json
COPY yarn.lock /app/yarn.lock
ENV PATH /app/node_modules/.bin:$PATH
RUN apk --no-cache add --virtual native-deps \
  g++ gcc libgcc libstdc++ linux-headers make python2 && \
  yarn && \
  apk del native-deps
