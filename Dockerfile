# Docker configuration for backend development. Not created for production use.
# It does not include front-end .
# Main production build is done using Dockerfile in the root of the project
FROM breneser/mssql-python-nodejs

WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code