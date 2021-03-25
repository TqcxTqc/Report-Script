#REPORT SCRIPT

#Домашнее задание
Цель:

    Написать скрипт анализа access.log для apache или nginx

Требования к реализации

    Должна быть возможность указать директорию где искать логи или конкретный файл
    Должна быть возможность выбрать все файлы логов отпарсить или только заданный
    В случае если файл не может быть обработан, то скрипт должен завершится с ошибкой
    Для access.log должна собираться следующая информация:

    общее количество выполненных запросов
    количество запросов по типу: GET - 20, POST - 10 и т.п.
    топ 10 IP адресов, с которых были сделаны запросы
    топ 10 самых долгих запросов, должно быть видно метод, url, ip, время запроса
    топ 10 запросов, которые завершились клиентской ошибкой, должно быть видно метод, url, статус код, ip адрес
    топ 10 запросов, которые завершились ошибкой со стороны сервера, должно быть видно метод, url, статус код, ip адрес

    Собранная статистика должна быть сохранена в json файл
    Должен быть README файл, который описывает как работает скрипт

Описание работы скрипта:

**Запуск скрипта**
    
Запуск по файлу

    python3 report_script --filelog access.log

Запуск по директории

    python3 report_script --directorylog path_of_directory

Отчет сгенерируется в формате json

Пример отчета:

        {
    "count_requests": 3216980,
    "count_by_type_requests": {
        "GET": 2247848,
        "POST": 918853,
        "HEAD": 49971,
        "PUT": 70,
        "Head": 3,
        "T": 195,
        "OPTIONS": 39,
        "DELETE": 1
    },
    "top_ip": {
        "193.106.31.130": 235209,
        "198.50.156.189": 167812,
        "5.112.235.245": 166722,
        "5.114.231.216": 158258,
        "5.113.18.208": 157674,
        "91.218.225.68": 134376,
        "79.62.229.212": 114799,
        "149.56.83.40": 97533,
        "5.114.64.184": 94043,
        "5.113.216.211": 89125
    },
    "the_longest_requests": [
        {
            "type_req": "POST",
            "url": "/administrator/index.php",
            "ip": "5.140.162.230",
            "duration": 100
        },
        {
            "type_req": "GET",
            "url": "/images/phocagallery/almhuette/thumbs/phoca_thumb_m_almhuette_raith_006.jpg",
            "ip": "188.23.30.77",
            "duration": 100
        },
        {
            "type_req": "POST",
            "url": "/administrator/index.php",
            "ip": "91.200.12.22",
            "duration": 100
        },
        {
            "type_req": "GET",
            "url": "/administrator/",
            "ip": "37.115.83.143",
            "duration": 100
        },
        {
            "type_req": "POST",
            "url": "/administrator/index.php",
            "ip": "5.44.168.146",
            "duration": 100
        },
        {
            "type_req": "GET",
            "url": "/administrator/",
            "ip": "195.114.153.125",
            "duration": 100
        },
        {
            "type_req": "GET",
            "url": "/administrator/",
            "ip": "213.24.135.214",
            "duration": 100
        },
        {
            "type_req": "GET",
            "url": "/administrator/",
            "ip": "31.23.252.223",
            "duration": 100
        },
        {
            "type_req": "GET",
            "url": "/administrator/",
            "ip": "94.51.23.211",
            "duration": 100
        },
        {
            "type_req": "POST",
            "url": "/administrator/index.php",
            "ip": "145.255.172.40",
            "duration": 100
        }
    ],
    "top_client_error_key_report": {
        "404": [
            {
                "ip": "191.182.199.16",
                "type_req": "GET",
                "duration": 1951,
                "url": "/templates/_system/css/general.css",
                "time": "12/Dec/2015:19:02:36 +0100",
                "status": 404
            },
            {
                "ip": "188.45.108.168",
                "type_req": "GET",
                "duration": 4138,
                "url": "/templates/_system/css/general.css",
                "time": "12/Dec/2015:19:44:06 +0100",
                "status": 404
            },
            {
                "ip": "188.45.108.168",
                "type_req": "GET",
                "duration": 4362,
                "url": "/favicon.ico",
                "time": "12/Dec/2015:19:44:15 +0100",
                "status": 404
            },
            {
                "ip": "157.55.39.3",
                "type_req": "GET",
                "duration": 8540,
                "url": "/icons/text.gif",
                "time": "13/Dec/2015:01:01:19 +0100",
                "status": 404
            },
            {
                "ip": "212.95.7.131",
                "type_req": "GET",
                "duration": 4063,
                "url": "/templates/_system/css/general.css",
                "time": "13/Dec/2015:11:28:41 +0100",
                "status": 404
            },
            {
                "ip": "40.77.167.66",
                "type_req": "GET",
                "duration": 8184,
                "url": "/apache-log/error.log.44.gz",
                "time": "13/Dec/2015:12:05:25 +0100",
                "status": 404
            },
            {
                "ip": "185.104.219.254",
                "type_req": "GET",
                "duration": 7924,
                "url": "/apache-log/access.log.69.gz",
                "time": "13/Dec/2015:15:56:36 +0100",
                "status": 404
            },
            {
                "ip": "157.55.39.8",
                "type_req": "GET",
                "duration": 4319,
                "url": "/apache-log/error.log.55.gz",
                "time": "13/Dec/2015:16:14:58 +0100",
                "status": 404
            }
        ]
    },
    "top_server_error_key_report": {
        "500": [
            {
                "ip": "83.167.113.100",
                "type_req": "GET",
                "duration": 4039,
                "url": "/administrator/",
                "time": "13/Dec/2015:02:30:28 +0100",
                "status": 500
            },
            {
                "ip": "109.197.194.109",
                "type_req": "GET",
                "duration": 4402,
                "url": "/administrator/",
                "time": "13/Dec/2015:02:33:01 +0100",
                "status": 500
            },
            {
                "ip": "176.49.68.156",
                "type_req": "GET",
                "duration": 4508,
                "url": "/administrator/",
                "time": "14/Dec/2015:02:32:35 +0100",
                "status": 500
            },
            {
                "ip": "66.249.69.112",
                "type_req": "GET",
                "duration": 9095,
                "url": "/",
                "time": "15/Dec/2015:02:35:41 +0100",
                "status": 500
            },
            {
                "ip": "212.7.217.50",
                "type_req": "GET",
                "duration": 4560,
                "url": "/administrator/",
                "time": "15/Dec/2015:02:37:15 +0100",
                "status": 500
            },
            {
                "ip": "85.115.224.206",
                "type_req": "GET",
                "duration": 3214,
                "url": "/administrator/",
                "time": "16/Dec/2015:02:36:39 +0100",
                "status": 500
            },
            {
                "ip": "195.16.111.40",
                "type_req": "GET",
                "duration": 1834,
                "url": "/administrator/",
                "time": "18/Dec/2015:02:40:22 +0100",
                "status": 500
            },
            {
                "ip": "94.50.192.129",
                "type_req": "GET",
                "duration": 3536,
                "url": "/administrator/",
                "time": "18/Dec/2015:02:42:07 +0100",
                "status": 500
            }
        ]
    }
    }
         
