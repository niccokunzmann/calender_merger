FROM python:alpine
EXPOSE 80

ADD calender_merger .
ADD requirements.txt .

RUN python -m pip install --no-cache-dir --disable-pip-version-check -r requirements.txt

CMD [ "python", "-m", "calender_merger", "80"]
