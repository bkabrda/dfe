FROM {{ base_img_reg }}/{{ base_img_name }}:{{ base_img_tag }}

RUN {{ installer }} install httpd && \
    {{ installer }} clean all

COPY {{ configfile }} /etc/httpd/conf.d

EXPOSE 80

CMD exec /usr/sbin/apachectl -DFOREGROUND
