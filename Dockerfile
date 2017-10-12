FROM jrottenberg/ffmpeg:3.3-alpine

MAINTAINER Simon Erhardt <me+docker@rootlogin.ch>

ARG VCS_REF
ARG BUILD_DATE

LABEL org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.vcs-url="https://github.com/chrootLogin/ffprocess"

ADD ffprocess.py /usr/local/bin/ffprocess.py
ADD requirements.txt /tmp/requirements.txt

RUN apk add --no-cache -U \
  alpine-sdk \
  bash \
  python3 \
  python3-dev \
  tini \
  && pip3 install -r /tmp/requirements.txt \
  && rm -f /tmp/requirements.txt \
  && apk del \
  alpine-sdk \
  python3-dev

VOLUME /data

ENTRYPOINT ["/sbin/tini", "--", "python3", "/usr/local/bin/ffprocess.py", "/data"]
