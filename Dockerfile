# Use the official Ruby image from the Docker Hub
FROM ruby:3.1

# Install necessary packages
RUN apt-get update && \
    apt-get install -y build-essential curl python3 python3-venv && \
    curl https://sh.rustup.rs -sSf | sh -s -- -y && \
    . $HOME/.cargo/env && \
    rustup default stable && \
    apt-get clean

# Set the working directory
WORKDIR /srv/jekyll

# Copy the Gemfile and Gemfile.lock into the container
COPY Gemfile Gemfile.lock ./

# Install the required gems
RUN bundle install

# Copy the rest of the application code into the container
COPY . .

# Create and activate a virtual environment
RUN python3 -m venv /srv/jekyll/venv

# Install Python dependencies in the virtual environment
RUN /srv/jekyll/venv/bin/pip install Flask==3.0.3 Flask-Bcrypt==1.0.1 gunicorn==22.0.0 python-dotenv==1.0.1

# Expose the ports the apps run on
EXPOSE 4000
EXPOSE 5000

# Start the Jekyll server and Flask application
CMD ["sh", "-c", "/srv/jekyll/venv/bin/gunicorn --bind 0.0.0.0:$PORT app:app & bundle exec jekyll serve --host 0.0.0.0 --port 4000"]
