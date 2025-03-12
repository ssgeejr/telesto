# Use the official PHP Apache image
FROM php:8.2-apache

# Install mysqli and pdo_mysql extensions
RUN docker-php-ext-install mysqli pdo pdo_mysql

# Enable Apache mod_rewrite (if needed)
RUN a2enmod rewrite

# Set the working directory
WORKDIR /var/www/html

# Copy application files
COPY src/ /var/www/html/

# Set appropriate permissions
RUN chown -R www-data:www-data /var/www/html

# Restart Apache to apply changes
RUN service apache2 restart

# Expose port 80
EXPOSE 80

# Start Apache server
CMD ["apache2-foreground"]
