# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.7

# Install manually all the missing libraries
##RUN apt-get install --fix-missing -y xvfb 
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl firefox-esr


 # Chrome instalation 
#RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
#RUN rm google-chrome-stable_current_amd64.deb
# Check chrome version
#RUN echo "Chrome: " && google-chrome --version
#RUN apt-get install python3-pip -y
#RUN apt-get install cmake -y

# Install Python dependencies.
COPY requirements.txt requirements.txt
RUN python3.7 -m pip install -r requirements.txt

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .
COPY .env $APP_HOME/.env


# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 main:app