#!/usr/bin/env python
import argparse
import time
import random
import string

from kazoo import client
from kazoo.exceptions import NoNodeError

WAIT_TIME = .005
ID_SIZE = 4


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





def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--host', default='zookeeper.stage.w1.us.quixey.com')
    args = parser.parse_args()

    pound_host(args.host)


if __name__ == "__main__":
    main()
