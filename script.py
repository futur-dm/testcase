import argparse
import json
from tabulate import tabulate
from datetime import datetime
from collections import defaultdict


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', nargs='+', help='Путь до файлов')
    parser.add_argument('--report', nargs='+', choices=['average', 'User-Agent'], help='Тип - отчет')
    parser.add_argument('--date', help='Дата (YYYY-MM-DD) для формирования отчета')

    return parser.parse_args()


def read_logs(filepaths, date_flag=None):
    endpoints = defaultdict(lambda : {'count': 0, 'total_time': 0.0})
    for filepath in filepaths:
        with open(filepath, 'r') as file:
            for f in file:
                info = json.loads(f)
                url = info.get('url')
                response_time = info.get('response_time')
                date_str = info.get('@timestamp')
                if date_str:
                    try:
                        record_date = datetime.strptime(date_str[:10], "%Y-%m-%d").date()
                    except Exception:
                        pass
                if date_flag:
                    if record_date != date_flag:
                        continue
                if url and response_time is not None:
                    endpoints[url]['count'] += 1
                    endpoints[url]['total_time'] += response_time

    return endpoints

def average(endpoints):
    report = []

    for url, stats in endpoints.items():
        average_time = stats['total_time'] / stats['count'] if stats['count'] and stats['count'] > 0 else 0
        report.append([url, stats['count'], round(average_time, 3)])
        report.sort(key=lambda x: x[0])

    return report

def get_user_agents(filepaths):
    agents = defaultdict(lambda : {'count': 0})

    for filepath in filepaths:
        with open(filepath, 'r') as file:
            for f in file:
                info = json.loads(f)
                agent = info.get('http_user_agent')
                if agent:
                    agents[agent]['count'] += 1
    return agents

def main():
    args = parse_arguments()
    date_flag = None
    if args.date:
        try:
            date_flag = datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError:
            print("Ошибка: Неверный формат даты, используйте YYYY-MM-DD")
            return

    endpoints = read_logs(args.file, None)
    agents = get_user_agents(args.file)

    headers = []

    if 'average' in args.report:
        report = average(endpoints)
        print(tabulate(report, headers=['Endpoint', 'Count', 'Average response time']))
    if 'User-Agent' in args.report:
        agent_report = [[agent, stats['count']] for agent, stats in agents.items()]
        print("\nUser-Agent statistics:")
        print(tabulate(agent_report, headers=['User-Agent', 'Count']))

if __name__ == "__main__":
    main()
