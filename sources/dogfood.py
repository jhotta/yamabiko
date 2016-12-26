#! /usr/bin/env python

from datadog import initialize, api
import time

options = {
    'api_key': '81df64ebed3a1ddf6ebf3b148e70b29e',
    'app_key': 'a18c26f402f1fd0901eb291e21db769c6648cb5a'
}

initialize(**options)


def cpu_idle_query(now):
    query = 'system.cpu.idle{*} by {*}'
    try:
        api_call_response = api.Metric.query(start=now - 60, end=now, query=query)
        metric_value = api_call_response['series'][-1]['pointlist'][-1][-1]
    except:
        metric_value = "not able to get the value"

    return metric_value


def get_metric_value(now, metric):

    if metric.lower() == 'cpu':
        response = cpu_idle_query(now)
    elif metric.lower() == 'hdd':
        response = 'not available'
    else:
        response = None

    return response


def main():
    now = int(time.time())
    metrics = ['CPU', 'HDD', 'Memory']

    for metric in metrics:
        print get_metric_value(now, metric)


if __name__ == '__main__':
    main()
