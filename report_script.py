import argparse
import os
from os import path
from os.path import join
import json
import re
from collections import defaultdict, Counter

# Main Constants

LOGS = []
ENDING_OF_LOG = ".log"

# Reports Keys
COUNT_REQUEST_KEY_REPORT = "count_requests"
COUNT_BY_TYPE_REQUEST_KEY_REPORT = "count_by_type_requests"
TOP_IP_KEY_REPORT = "top_ip"
TOP_LONGEST_REQUEST_KEY_REPORT = "the_longest_requests"
TOP_CLIENT_ERROR_KEY_REPORT = "top_client_error_key_report"
TOP_SERVER_ERROR_KEY_REPORT = "top_server_error_key_report"

REPORT = {
    COUNT_REQUEST_KEY_REPORT: 0,
    COUNT_BY_TYPE_REQUEST_KEY_REPORT: defaultdict(int),
    TOP_IP_KEY_REPORT: defaultdict(int),
    TOP_LONGEST_REQUEST_KEY_REPORT: list(),
    TOP_CLIENT_ERROR_KEY_REPORT: defaultdict(list),
    TOP_SERVER_ERROR_KEY_REPORT: defaultdict(list)
}

NUMBER_OF_MOST_COMMON = 10

IP_KEY = "ip"
REQUEST_TYPE_KEY = "type_req"
DURATION_KEY = "duration"
URL_KEY = "url"
TIME_KEY = "time"
STATUS_KEY = "status"

parser = argparse.ArgumentParser()
parser.add_argument('--directorylog', help='directory of access log files')
parser.add_argument('--filelog', help='access log file in script directory or in --logdir param')
args = parser.parse_args()
dirlog = args.directorylog
filelog = args.filelog


def get_path_logs(dirlog, filelog):
    logs = []
    if not dirlog and not filelog:
        exit("Choose log files directory or log file")
    elif dirlog and not filelog:
        if path.exists(dirlog) and path.isdir(dirlog):
            exit(f"{dirlog} is not a directory")
        for root, dirs, files in os.walk(dirlog):
            for name in files:
                log_path = join(root, name)
                if name.endswith(ENDING_OF_LOG) and os.path.exists(log_path) and os.path.isfile(log_path):
                    logs.append(log_path)
    elif not dirlog and filelog and filelog.endswith(ENDING_OF_LOG):
        logs.append(filelog)
    elif dirlog and filelog and filelog.endswith(ENDING_OF_LOG):
        logs.append(join(dirlog, filelog))
    else:
        exit(f"directory:{dirlog} does not contains {ENDING_OF_LOG} files")
    return logs


def get_dict_by_line(line):
    def get_value_by_regex(regex, value, type_value=str):
        try:
            match = re.findall(regex, value)
            return type_value(match[0])
        except Exception as e:
            exit(f"Faulure to search by regex {regex} in {value}")

    regex_ip = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    regex_type_req = r"OPTIONS|GET|Head|POST|PUT|PATCH|DELETE|TRACE|HEAD|T"
    regex_duration = r'\s"?([^"]*)?"?$'
    regex_url = r'\".+\s(.+)\sHTTP'
    regex_time = r'\[(.+)\]'
    regex_status = r'\"\s(\d{3}|-)'

    dictionary = dict()

    dictionary[IP_KEY] = get_value_by_regex(regex_ip, line)
    dictionary[REQUEST_TYPE_KEY] = get_value_by_regex(regex_type_req, line)
    dictionary[DURATION_KEY] = get_value_by_regex(regex_duration, line, type_value=int)
    dictionary[URL_KEY] = get_value_by_regex(regex_url, line)
    dictionary[TIME_KEY] = get_value_by_regex(regex_time, line)
    dictionary[STATUS_KEY] = get_value_by_regex(regex_status, line, type_value=int)

    return dictionary


def get_lines(file_path):
    dict_lines = []
    try:
        with open(file_path) as f:
            lines = f.readlines()
    except Exception as e:
        exit(f"Failure of reading {f}:{e}")
    for line in lines:
        d = get_dict_by_line(line)
        dict_lines.append(d)
    return dict_lines


def get_count_of_requests(lines):
    return len(lines)


def get_count_by_type_request(lines):
    req_type_cnt = defaultdict(int)
    for line in lines:
        type_req = line[REQUEST_TYPE_KEY]
        req_type_cnt[type_req] += 1
    return req_type_cnt


def get_top_ip(lines):
    ips = [line[IP_KEY] for line in lines]
    count = Counter(ips)
    top = count.most_common(NUMBER_OF_MOST_COMMON)
    return dict(top)


def get_max_duration(lines):
    sort_by_duration = sorted(lines, key=lambda duration: duration[DURATION_KEY])[:NUMBER_OF_MOST_COMMON]
    dur_list = list()
    for line in sort_by_duration:
        dur_list.append(
            {
                REQUEST_TYPE_KEY: line.get(REQUEST_TYPE_KEY),
                URL_KEY: line.get(URL_KEY),
                IP_KEY: line.get(IP_KEY),
                DURATION_KEY: line.get(DURATION_KEY)
            }
        )

    return dur_list


def most_common_record_by_duration(lines):
    report_long_req = lines + REPORT[TOP_LONGEST_REQUEST_KEY_REPORT]
    return sorted(report_long_req, key=lambda d: d[DURATION_KEY], reverse=True)[:NUMBER_OF_MOST_COMMON]


def get_common_error(lines, start_err, end_err):
    dictionary_client_err = dict()
    for err in range(start_err, end_err + 1):
        dictionary_client_err[err] = list(filter(lambda l: l[STATUS_KEY] == err, lines))

        def order_by_len(item):
            return len(item[1])

    sorted_by_cnt_error = sorted(dictionary_client_err.items(), key=order_by_len, reverse=True)[:NUMBER_OF_MOST_COMMON]

    return dict(sorted_by_cnt_error)


for log in get_path_logs(dirlog, filelog):
    dict_lines = get_lines(log)
    count_request = get_count_of_requests(dict_lines)
    count_type_of_requests = get_count_by_type_request(dict_lines)
    top_ips = get_top_ip(dict_lines)
    duration_lines = get_max_duration(dict_lines)

    top_client_error_lines = get_common_error(dict_lines, 400, 499)
    top_server_error_lines = get_common_error(dict_lines, 500, 599)

    REPORT[COUNT_REQUEST_KEY_REPORT] = REPORT[COUNT_REQUEST_KEY_REPORT] + count_request
    REPORT[COUNT_BY_TYPE_REQUEST_KEY_REPORT] = count_type_of_requests
    REPORT[TOP_IP_KEY_REPORT] = top_ips
    REPORT[TOP_LONGEST_REQUEST_KEY_REPORT] = most_common_record_by_duration(duration_lines)
    REPORT[TOP_CLIENT_ERROR_KEY_REPORT] = top_client_error_lines
    REPORT[TOP_SERVER_ERROR_KEY_REPORT] = top_server_error_lines

with open('report.json', 'w') as fp:
    json.dump(REPORT, fp, indent=3)
