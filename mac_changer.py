#!/usr/bin/env python3

import argparse
import os
import re
import subprocess
import sys


MAC_REGEX = re.compile(r'^[0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5}$')


def parse_args():
    parser = argparse.ArgumentParser(
        description='Change the MAC address of a network interface on Linux'
    )
    parser.add_argument(
        '--interface', '-i',
        required=True,
        help='Network interface name (e.g. eth0, wlan0)'
    )
    parser.add_argument(
        '--mac', '-m',
        required=True,
        help='New MAC address in format AA:BB:CC:DD:EE:FF'
    )
    return parser.parse_args()


def validate_mac(mac_address):
    if not MAC_REGEX.match(mac_address):
        raise ValueError('MAC address must be in format AA:BB:CC:DD:EE:FF')


def check_root():
    if os.name != 'posix':
        raise EnvironmentError('This script is designed for Linux/Unix environments.')
    if os.geteuid() != 0:
        raise PermissionError('This script must be run as root. Use sudo.')


def run_command(command):
    print(f'Running: {command}')
    result = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or 'Command failed')
    return result.stdout.strip()


def get_current_mac(interface):
    output = run_command(f'ip link show dev {interface}')
    for line in output.splitlines():
        line = line.strip()
        if line.startswith('link/ether'):
            return line.split()[1]
    return None


def change_mac(interface, new_mac):
    print(f'Current MAC for {interface}: {get_current_mac(interface) or "unknown"}')
    run_command(f'ip link set dev {interface} down')
    run_command(f'ip link set dev {interface} address {new_mac}')
    run_command(f'ip link set dev {interface} up')
    current_mac = get_current_mac(interface)
    print(f'MAC address changed for {interface} to {current_mac}')


if __name__ == '__main__':
    try:
        args = parse_args()
        validate_mac(args.mac)
        check_root()
        change_mac(args.interface, args.mac)
    except ValueError as exc:
        print(f'Input error: {exc}', file=sys.stderr)
        sys.exit(1)
    except PermissionError as exc:
        print(f'Permission error: {exc}', file=sys.stderr)
        sys.exit(1)
    except EnvironmentError as exc:
        print(f'Environment error: {exc}', file=sys.stderr)
        sys.exit(1)
    except RuntimeError as exc:
        print(f'Runtime error: {exc}', file=sys.stderr)
        sys.exit(1)
