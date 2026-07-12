FROM ghcr.io/cirruslabs/flutter:stable AS build

WORKDIR /app/desktop

COPY desktop/pubspec.yaml desktop/pubspec.lock ./
RUN flutter pub get

COPY desktop/ ./
RUN flutter build web --release \
    --dart-define=BASE_URL= \
    --no-wasm-dry-run

FROM nginx:alpine

ENV PROXY_UPSTREAM=host.docker.internal:5000
ENV ADMIN_PASSWORD=srp-admin

COPY desktop/nginx/nginx.conf.template /etc/nginx/templates/default.conf.template
COPY desktop/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
COPY --from=build /app/desktop/build/web /usr/share/nginx/html

EXPOSE 80

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
