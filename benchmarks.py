import tempfile
import time
import os
from datetime import datetime
import random
import logging
import csv
from enum import Enum

BENCH_FILE = "bench_write.bin"
STUNNEL_MOUNT_DIR = "/home/ec2-user/efs-stunnel"
PROXY_MOUNT_DIR = "/home/ec2-user/efs-proxy"
LOG_FILE = "fs-health-check.log"
PROXY_MOUNT = "efs-proxy"
STUNNEL_MOUNT = "stunnel"
OUTPUT_CSV = "bench_writes.csv"

logger = logging.getLogger(__name__)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)


class LatenciesResultCsv:
    """
    Encapsulates logic to record benchmark results in a CSV file.
    """

    def __init__(self, csv_file):
        self.csv_file = open(csv_file, 'a')
        fieldnames = ['timestamp', 'mount_type', 'io_size', 'latency_us']
        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=fieldnames)
        self.csv_writer.writeheader()

    def put_latencies(self, timestamp, mount_type, io_size, latency_us):
        """
        Records an entry into the output CSV file.

        :param mount_type: 'stunnel' or 'efs-proxy'
        :param io_size: The size in bytes of the write.
        :param latency_us: The write latency in microseconds.
        """
        self.csv_writer.writerow({'timestamp': timestamp, 'mount_type': mount_type, 'io_size': io_size, 'latency_us': latency_us})

    def __del__(self):
        if hasattr(self, 'csv_file') and not self.csv_file.closed:
            self.csv_file.close()


def bench_write(mount_dir, io_size):
    temp_file = open(os.path.join(mount_dir, BENCH_FILE), "wb", 0)
    bytes_data = os.urandom(io_size)
    start = datetime.now()
    temp_file.write(bytes_data)
    os.fsync(temp_file)
    write_latency = (datetime.now() - start)
    logger.debug(f"Wrote {io_size} bytes to {temp_file}")
    temp_file.close()
    os.remove(temp_file.name)

    return write_latency.microseconds, start


def main():
    output_csv = LatenciesResultCsv(OUTPUT_CSV)
    logger.info("Starting write benchmarks")
    while True:
        for io_size in [1024, 9 * 1024]:
            proxy_write, proxy_bench_ts = bench_write(PROXY_MOUNT_DIR, io_size)
            stunnel_write, stunnel_bench_ts = bench_write(STUNNEL_MOUNT_DIR, io_size)
            output_csv.put_latencies(proxy_bench_ts, PROXY_MOUNT, io_size, proxy_write)
            output_csv.put_latencies(stunnel_bench_ts, STUNNEL_MOUNT, io_size, stunnel_write)

    
if __name__ == "__main__":
    main()
