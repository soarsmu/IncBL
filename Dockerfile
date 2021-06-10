FROM python:3.7
RUN bash env_config.sh
CMD ["python local.py ./", "", "", ""]
