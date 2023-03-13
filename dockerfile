FROM python:3.10 as build

WORKDIR /opt/app
RUN python -m venv /opt/app/venv
ENV PATH="/opt/app/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt


FROM node:14

RUN apt update -y
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
#RUN apt update -y
#RUN apt install python3.10

WORKDIR /opt/app
COPY --from=build /opt/app/venv /venv

ENV PATH="/opt/app/venv/bin:$PATH"
ENV NODE_ENV=container

COPY package.json .
RUN yarn install

COPY . .
EXPOSE 8081
EXPOSE 8080
CMD yarn start