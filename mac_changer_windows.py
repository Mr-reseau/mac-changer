#!/usr/bin/env python3

import argparse
import re
import subprocess
import sys

MAC_REGEX = re.compile(r'^[0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5}$')


def parse_args():
    parser = argparse.ArgumentParser(
        description='Change the MAC address of a network interface on Windows'
    )
    parser.add_argument(
        '--interface', '-i',
        required=True,
        help='Network adapter name as shown by Get-NetAdapter'
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
    command = (
        f'powershell -Command "(Get-NetAdapter -Name \'{interface}\').MacAddress"'
    )
    return run_command(command).strip()


def set_network_address(interface, mac_address):
    value = mac_address.replace(':', '')
    command = (
        'powershell -Command "Set-NetAdapterAdvancedProperty '
        f'-Name \'{interface}\' -RegistryKeyword NetworkAddress '
        f'-RegistryValue \'{value}\'"'
    )
    return run_command(command)


def restart_interface(interface):
    run_command(f'netsh interface set interface name=\"{interface}\" admin=disable')
    run_command(f'netsh interface set interface name=\"{interface}\" admin=enable')


if __name__ == '__main__':
    try:
        args = parse_args()
        validate_mac(args.mac)
        current_mac = get_current_mac(args.interface)
        print(f'Current MAC for {args.interface}: {current_mac}')
        set_network_address(args.interface, args.mac)
        restart_interface(args.interface)
        final_mac = get_current_mac(args.interface)
        print(f'MAC address changed for {args.interface} to {final_mac}')
    except ValueError as exc:
        print(f'Input error: {exc}', file=sys.stderr)
        sys.exit(1)
    except RuntimeError as exc:
        print(f'Runtime error: {exc}', file=sys.stderr)
        sys.exit(1)
