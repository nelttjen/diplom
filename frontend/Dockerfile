FROM node:current-alpine as build

WORKDIR /app/frontend/

COPY package*.json /app/frontend/
RUN npm install

ENV PATH /app/frontend/node_modules/.bin:$PATH

COPY . /app/frontend/
RUN npm run build

CMD ["npm", "start"]