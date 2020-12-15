# set base image (host OS)
FROM python:3

# set the working directory in the container
WORKDIR /usr/app/src

# copy the dependencies file to the working directory
COPY src/requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ .

# command to run on container start
# CMD ["sh", "-c", "python3 ./main.py -d /usr/app/config -c configuration.json -b j1939_orig.dbc" ]