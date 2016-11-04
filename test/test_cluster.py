#!/usr/bin/env python
import argparse
import logging
import string
import time
import random

from collections import Counter

import gevent
from kazoo import client
from kazoo.exceptions import NoNodeError, SessionExpiredError
from kazoo.handlers.threading import KazooTimeoutError

WAIT_TIME = .005
ID_SIZE = 4
MAX_POOL_SIZE = 340

logging.basicConfig()


def clear_foos(zk):
    foos = zk.get_children('/')
    for f in foos:
        if 'foo' in f:
            print "found {} for deletion".format(f)
            try:
                zk._delete_recursive(f)
            except NoNodeError, e:
                print 'error deleting {}: {}'.format(f, e)
                continue


def pound_host(hostname):
    seq = 0
    id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(ID_SIZE))
    zk = client.KazooClient(hostname)
    zk.start()
    try:
        while True:
            seq += 1
            f1 = '/foo{}{}'.format(id, seq)
            f2 = f1+'/bar'
            try:
                zk.create(f1)
                time.sleep(WAIT_TIME)
                zk.create(f2)
                time.sleep(WAIT_TIME)
                zk.delete(f2)
                time.sleep(WAIT_TIME)
                zk.delete(f1)
                time.sleep(WAIT_TIME)
            finally:
                print 'seq: {}'.format(id+str(seq))
                zk._delete_recursive(f1)
    finally:
        clear_foos(zk)


def make_connection(hostname, i):

    logging.info('creating connection ', i)
    zk = client.KazooClient(hostname)
    try:
        zk.start(timeout=.3)
    except KazooTimeoutError:
        logging.debug('connection {}, TIMEOUT'.format(i))
        return "Timeout"
    return "OK"


def test_number_of_connections(hostname, pool_size=MAX_POOL_SIZE, hold=True):
    threads = []

    for i in xrange(pool_size):
        threads.append(gevent.spawn(make_connection, hostname, i))

    gevent.joinall(threads)

    c = Counter()
    for t in threads:
        print t.value
        c.update([t.value])
    print c

    if hold:
        raw_input('Holding connections open. Press any key to close connections end...')

    return c


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--host', default='zookeeper.stage.w1.us.quixey.com')
    parser.add_argument('-t', '--test-connections', action='store_true')
    parser.add_argument('-c', '--connections', default=MAX_POOL_SIZE, type=int)
    parser.add_argument('-n', '--no-hold', action='store_false', default=True)
    args = parser.parse_args()

    if args.test_connections:
        if args.connections > MAX_POOL_SIZE:
            print "Max Connections: {}. Setting to Max Connections, now.".format(MAX_POOL_SIZE)
            args.connections = MAX_POOL_SIZE
        test_number_of_connections(args.host, args.connections, args.no_hold)
    else:
        while True:
            try:
                pound_host(args.host)
            except (SessionExpiredError, KazooTimeoutError) as e:
                print 'client terminated: restarting now'


if __name__ == "__main__":
    main()
