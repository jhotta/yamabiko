#! /usr/bin/env python

from datadog import initialize, api
import time

options = {
    'api_key': '81df64ebed3a1ddf6ebf3b148e70b29e',
    'app_key': 'a18c26f402f1fd0901eb291e21db769c6648cb5a'
}

initialize(**options)


def cpu_idle_query(now):
    query = 'system.cpu.idle{*} by {host}'
    try:
        a = api.Metric.query(start=now - 20, end=now, query=query)['series'][-1]['pointlist']
    except:
        a = api.Metric.query(start=now - 40, end=now, query=query)['series'][-1]['pointlist']

    print(a[-1])
    return (a[-1][-1])


def main():
    now = int(time.time())
    print(cpu_idle_query(now))


if __name__ == '__main__':
    main()
