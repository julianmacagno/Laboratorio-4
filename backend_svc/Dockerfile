FROM python:2.7-alpine
RUN apk add build-base python2-dev
RUN apk add --update py-pip
RUN pip install --upgrade pip
ADD . /usr/backend_svc/
WORKDIR /usr/backend_svc/src/
RUN pip install --no-cache-dir -r ../requirements.txt
EXPOSE 8081
CMD [ "python", "app.py" ]