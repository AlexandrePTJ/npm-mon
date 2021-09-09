FROM python:3

ARG NPMMON_ROOT=/npmmon
ENV NPMMON_CONFIG=$NPMMON_ROOT/config.yml

WORKDIR /usr/src/app

COPY requirements.txt .
COPY npmmon npmmon
COPY main.py .

RUN pip install --no-cache-dir -r requirements.txt && \
    mkdir -p $NPMMON_ROOT/cache && \
    mkdir -p $NPMMON_ROOT/logs

COPY config_docker.yml.tpl $NPMMON_CONFIG
RUN sed -Ei "s|__DOCKER_NPMMON_ROOT__|$NPMMON_ROOT|g" $NPMMON_CONFIG

CMD python main.py -c $NPMMON_CONFIG -w
VOLUME ["$NPMMON_ROOT/cache", "$NPMMON_ROOT/logs"]
