#!/usr/bin/env python3

import argparse
import subprocess
import sys


def parse_args():
    parser = argparse.ArgumentParser(description='Change the MAC address of a network interface')
    parser.add_argument('--interface', '-i', required=True, help='Network interface name')
    parser.add_argument('--mac', '-m', required=True, help='New MAC address (format: AA:BB:CC:DD:EE:FF)')
    return parser.parse_args()


def run_command(command):
    print(f'Running: {command}')
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print('Error:', result.stderr.strip(), file=sys.stderr)
        sys.exit(result.returncode)
    return result.stdout.strip()


def change_mac(interface, new_mac):
    run_command(f'sudo ip link set dev {interface} down')
    run_command(f'sudo ip link set dev {interface} address {new_mac}')
    run_command(f'sudo ip link set dev {interface} up')
    print(f'MAC address changed for {interface} to {new_mac}')


if __name__ == '__main__':
    args = parse_args()
    change_mac(args.interface, args.mac)
