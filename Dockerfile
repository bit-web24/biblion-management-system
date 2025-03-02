FROM python:3.12.3-slim

WORKDIR /biblion_management_system

COPY ./requirements.txt /biblion_management_system/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /biblion_management_system/requirements.txt

COPY ./app /biblion_management_system/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
