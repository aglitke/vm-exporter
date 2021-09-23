FROM quay.io/bitnami/python

COPY servexz.py /

CMD [ "/servexz.py" ]