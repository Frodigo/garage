# Stage 1: Build the application
FROM node:20-slim AS builder

# Set the working directory
WORKDIR /usr/src/app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install all dependencies, including devDependencies
RUN npm install

# Copy the rest of the application files
COPY . .

# Compile TypeScript to JavaScript
RUN npm run build

# Stage 2: Create the final image
FROM node:20-slim

# Set the working directory
WORKDIR /usr/src/app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install only production dependencies
RUN npm install --only=production

# Copy the compiled files from the builder stage
COPY --from=builder /usr/src/app/dist ./dist

# Command to run the application
CMD ["node", "dist/server.js"]
