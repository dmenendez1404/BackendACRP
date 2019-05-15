FROM python
ENV PYTHONUNBUFFERED 1
RUN mkdir /api_service
WORKDIR /api_service
COPY . /api_service/
RUN pip install --upgrade pip -i http://192.168.10.15:8081/repository/pypi/simple --trusted-host 192.168.10.15
RUN pip install -r requirements.txt -i http://192.168.10.15:8081/repository/pypi/simple --trusted-host 192.168.10.15
ENTRYPOINT python /api_service/manage.py migrate && python /api_service/manage.py runserver 0.0.0.0:8000
EXPOSE 8000
