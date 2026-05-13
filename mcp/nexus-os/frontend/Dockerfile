FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

# Expose the vite port
EXPOSE 5173

# Run the vite dev server, host 0.0.0.0 is needed for docker port mapping
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
