import argparse
import ipinfo
import settings
import time
import threading

from utils import get_pretty_time

from tabulate import tabulate


# IPInfo response
#
# {
#     'ip': '216.239.36.21', 
#     'hostname': 'any-in-2415.1e100.net', 
#     'country': 'US', 
#     'org': 'AS15169 Google LLC', 
#     'country_name': 'United States', 
#     'latitude': '38.0088',
#     'longitude': '-122.1175'
# }

_404 = 'N/A'

_headers = ['IP', 'Hostname', 'Country', 'Org', 'Lat', 'Lon', 'Time']
_handler = ipinfo.getHandler(settings.IPINFO_API_KEY)

_total_time = 0
_total_table = []
_total_threads = []


def clean_buffer():
    global _total_time
    _total_time = 0

    global _total_table
    _total_table = []


def get_sync_ip_detail(ip):
    try:
        # Show ip
        print(f'\tResolving {ip}...')

        # Get start time
        start_time = time.time()
 
        # Get details from IPInfo API
        ip_details = _handler.getDetails(ip)
        ip_details = ip_details.all
 
        # Get end time
        end_time = time.time()
 
        # Get diff
        diff_time = end_time - start_time
 
        # Get pretty country
        country = f"{ip_details.get('country_name', _404)} ({ip_details.get('country', _404)})"
 
        # Build table
        global _total_table
        _total_table.append([ip, ip_details.get('hostname', _404), country, ip_details.get('org', _404), 
            ip_details.get('latitude', _404), ip_details.get('longitude', _404),
            get_pretty_time(diff_time)]
        )
 
        global _total_time
        _total_time += diff_time
    except: pass


def show_ip_detail():
    # Build table
    table = _total_table
    table.append(['', '', '', '', '', '', get_pretty_time(_total_time)])

    # Show table
    print('\n\nScan Complete!\n\n')
    print(tabulate(table, headers=_headers))

    # Clean buffer to prevent a race condition pseudo
    clean_buffer()


def show_sync_ip_detail(ip):
    get_sync_ip_detail(ip)

    # Show results
    show_ip_detail()


def show_sync_multiple_ip_detail(ips):
    for ip in ips:
        try:
            get_sync_ip_detail(ip)
        except: pass

    # Show results
    show_ip_detail()


def show_async_multiple_ip_detail(ips):
    global _total_threads

    for ip in ips:
        thread = threading.Thread(target=get_sync_ip_detail, args=(ip,))
        _total_threads.append(thread)

    for thread in _total_threads:
        thread.start()

    for thread in _total_threads:
        thread.join()

    # Show results
    show_ip_detail()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ip details by IPInfo')
    parser.add_argument('--no-sync', nargs='?', const=True, default=False, 
                              type=bool, help='use multithreading')

    parser_group = parser.add_mutually_exclusive_group(required=True)
    parser_group.add_argument('--ip', help='single ip')
    parser_group.add_argument('--ips', help='multiple ips', nargs='*')
    
    args = parser.parse_args()

    print('---- Running IPINFO Scan ----')
    print('--- Written by Julio Realpe ---')

    if args.ip:
        show_sync_ip_detail(args.ip)
    else:
        if args.no_sync:
            print('\tUsing multithreading...')
            show_async_multiple_ip_detail(args.ips)
        else:
            show_sync_multiple_ip_detail(args.ips)
