FROM python:3.12.3-slim

WORKDIR /biblion_management_system

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock /biblion_management_system/

RUN poetry install --no-root

COPY ./app /biblion_management_system/app

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
