# Use official PHP 8.2 with Apache 2.4 as the base image
FROM php:8.2-apache

# Update package list and install necessary extensions for MySQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && docker-php-ext-install pdo pdo_mysql

# Enable Apache rewrite module (optional, for flexibility)
RUN a2enmod rewrite

# Set working directory to Apache's web root
WORKDIR /var/www/html

# Copy your PHP files into the container
COPY ./src /var/www/html/

# Expose port 80 for web access
EXPOSE 80

# Start Apache in the foreground
CMD ["apache2-foreground"]