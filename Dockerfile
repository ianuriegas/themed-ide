# Use the official Nginx image as the base
FROM nginx:alpine

# Copy the IDE files to the Nginx web root
COPY ide/ /usr/share/nginx/html/

# Expose port 80 for web traffic
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"] 