## Пример сбора метрик из сервиса

Метрики отправляются в ручку /metrics

curl localhost:8082/

curl localhost:8082/metrics

далее запуск ui:

docker-compose up -d


Prometheus теперь будет доступен по адресу http://localhost:9090,

а Grafana по адресу http://localhost:3000.

Шаг 1: Зайдите в Grafana

Перейдите на http://localhost:3000, по умолчанию логин и пароль: admin / admin.


Шаг 2: Добавьте источник данных Prometheus

Перейдите в Connection -> Data Sources

Выберите Prometheus.

В поле URL введите: http://prometheus:9090.

Нажмите Save & Test.


http://localhost:3000/dashboard/new?from=now-6h&to=now&timezone=browser&editPanel=1

[отображений метрик](grafana_example.png)