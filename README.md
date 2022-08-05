openmetrics-liveness-probe
============

Библиотека для получения времени, когда сервис в последний раз считался живым.
Результат экспортируется в формате OpenMetrics. Пример вывода:

```
# HELP liveness_probe_unixtime Unixtime последней liveness probe
# TYPE liveness_probe_unixtime gauge
liveness_probe_unixtime{service="test"} 1.659455742252334e+09
```

В многопоточном режиме:
```
# HELP liveness_probe_unixtime Multiprocess metric
# TYPE liveness_probe_unixtime gauge
liveness_probe_unixtime{pid="12821",service="example"} 1.6596198592194734e+09
liveness_probe_unixtime{pid="13521",service="example"} 1.6796198592194734e+09
```

Для начала необходимо объявить переменные окружения:
```
OPENMETRICS_LIVENESS_PROBE_ENABLED=True
OPENMETRICS_LIVENESS_PROBE_HOST=0.0.0.0
OPENMETRICS_LIVENESS_PROBE_PORT=8000
OPENMETRICS_LIVENESS_PROBE_SERVICE_NAME=example
OPENMETRICS_LIVENESS_PROBE_NAME_POSTFIX=liveness_probe_unixtime
OPENMETRICS_LIVENESS_PROBE_ENABLE_DEFAULT_PROMETHEUS_METRICS=False
PROMETHEUS_MULTIPROC_DIR=None
```

Все переменные по-умолчанию будут равны значениям, указанным в списке выше, Но переменная окружения ``SERVICE_NAME`` должна быть обязательно изменена.

Переменная окружения ``ENABLE_DEFAULT_PROMETHEUS_METRICS`` включает метрики по-умолчанию доступные в ``prometheus_client``: 
``PROCESS_COLLECTOR``, ``PLATFORM_COLLECTOR``, ``GC_COLLECTOR``.    
По-умолчанию их отображение выключено.

Переменная окружения ``PROMETHEUS_MULTIPROC_DIR`` позволяет запускать prometheus сервер в многопоточном режиме. По умолчанию эта переменная равна ``None.`` Для активации этого режима нужно задать путь для переменной окружения ``PROMETHEUS_MULTIPROC_DIR``, например: ``/tmp``.

# Содержание

- [Установка](#Установка)

<a name='Установка'></a>
## Установка

Описание установки
- pip 
```
pip install openmetrics_liveness_probe
```
