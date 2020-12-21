FROM node:14.15.3-alpine3.11

WORKDIR /bot

COPY package*.json ./

RUN npm install --only=production

COPY . ./

CMD [ "npm","start" ]