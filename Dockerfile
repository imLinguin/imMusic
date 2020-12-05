FROM node:14.15.1

WORKDIR /bot

COPY . ./

RUN npm install

CMD [ "npm","start" ]