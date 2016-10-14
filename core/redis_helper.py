#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis


class redis_helper:

    def __init__(self):
        # self.pool = redis.ConnectionPool(host='192.168.71.128', port=6379)
        self.pool = redis.ConnectionPool(host='192.168.127.129', port=6379)
        self.r = redis.Redis(connection_pool=self.pool)
