FROM ghcr.io/cirruslabs/flutter:stable AS build

WORKDIR /app/desktop

COPY desktop/pubspec.yaml desktop/pubspec.lock ./
RUN flutter pub get

COPY desktop/ ./
RUN flutter build web --release --dart-define=BASE_URL= --no-wasm-dry-run

FROM nginx:alpine

ENV PROXY_UPSTREAM=host.docker.internal:5000

COPY desktop/nginx/nginx.conf.template /etc/nginx/templates/default.conf.template
COPY --from=build /app/desktop/build/web /usr/share/nginx/html

EXPOSE 80
