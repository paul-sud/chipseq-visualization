FROM node:15.5.1-alpine3.12
WORKDIR /app
COPY package.json /app/package.json
COPY yarn.lock /app/yarn.lock
ENV PATH /app/node_modules/.bin:$PATH
RUN yarn
