openmetrics-liveness-probe
============

Библиотека для обновления метрики значения времени жизни `{service_name}_{liveness_probe_name_postfix}` для сервиса `{service_name}`, когда считалось, что сервис жив.

Для начала необходимо объявить переменные окружения:
```
OPENMETRICS_LIVENESS_PROBE_HOST=0.0.0.0
OPENMETRICS_LIVENESS_PROBE_PORT=8000
OPENMETRICS_LIVENESS_PROBE_SERVICE_NAME=
OPENMETRICS_LIVENESS_PROBE_NAME_POSTFIX=liveness_probe_unixtime
```
Переменная окружения SERVICE_NAME должна быть обязательно объявлена, оставшиеся по умолчанию будут равны значениям, указанным в списке выше.

# Содержание

- [Установка](#Установка)

<a name='Установка'></a>
## Установка

Описание установки
- pip 
```
pip install openmetrics_liveness_probe
```