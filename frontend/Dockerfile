FROM node:18-alpine

WORKDIR /app

COPY package.json .

RUN npm install
RUN npm install uuid axios react-markdown react-icons clsx @types/uuid

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
