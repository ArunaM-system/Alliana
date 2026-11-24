FROM node:20-alpine

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy source code
COPY . .

# Expose dev server port
EXPOSE 5173

# Run the dev server (Vite or CRA)
CMD ["npm", "run", "dev"]
