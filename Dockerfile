FROM python:3.7-slim

WORKDIR /src
EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "--timeout=10", "--workers=2", "web.app:app"]

RUN pip3 install \
  gunicorn \
  flask \
  webargs==4.1.2 \
  requests

COPY . /src
RUN cd /src && python3 setup.py develop
