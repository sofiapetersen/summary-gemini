FROM node:24-alpine as build

WORKDIR /app

COPY package.json yarn.lock* package-lock.json* ./

RUN npm install 

COPY . .

ENV VUE_APP_API_URL=http://backend:5000

RUN npm run build

FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]