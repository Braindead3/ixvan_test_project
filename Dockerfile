FROM python

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install pipenv and compilation dependencies
RUN pip install pipenv

# Install python dependencies
COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv install --system --deploy --ignore-pipfile