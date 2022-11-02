FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
# COPY test_content/ /opt/Robot/
RUN pip install --no-cache-dir -r requirements.txt

# RUN pip install connexion[swagger-ui]

EXPOSE 8080
CMD [ "python", "webapps/app.py"]
