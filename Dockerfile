FROM node:14.15.1

WORKDIR /bot

COPY package*.json ./

RUN npm install

COPY . ./

CMD [ "npm","start" ]