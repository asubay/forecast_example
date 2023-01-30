# ---- Base python ----
FROM python:3.9 AS base
# Create app directory
WORKDIR /app

# ---- Dependencies ----
FROM base AS dependencies
COPY requirements.txt ./

RUN pip install --upgrade pip

RUN apt-get update
# install app dependencies
RUN pip install -r requirements.txt

# ---- Copy Files/Build ----
FROM dependencies AS build
WORKDIR /app
COPY . /app
# Build / Compile if required

# --- Release with Alpine ----
FROM python:3.9 AS release
# Create app directory
WORKDIR /app

COPY --from=dependencies /app/requirements.txt ./
COPY --from=dependencies /root/.cache /root/.cache


# Install app dependencies
RUN pip install -r requirements.txt

COPY --from=build /app/ ./

CMD ["python", "main.py"]