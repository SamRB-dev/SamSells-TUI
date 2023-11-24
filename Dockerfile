FROM python:latest
ADD requirements.txt .
ADD . ./
RUN pip install -r requirements.txt
CMD [ "python", "./SamSells.py" ]