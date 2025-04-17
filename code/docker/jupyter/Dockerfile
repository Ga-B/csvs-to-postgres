# syntax=docker/dockerfile:1

FROM quay.io/jupyter/base-notebook:latest

USER root

RUN apt-get update && apt-get install --yes make

USER jovyan

COPY requirements.txt .
RUN mamba install --yes --file requirements.txt && \
    mamba clean --all -f --yes