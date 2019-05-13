from django.core.management import BaseCommand
from django.db import connection

from data.models import * 
from data.process import *
from data.process_enterprise import *

import re
import json
import datetime
import threadpool
import pandas as pd


class Command(BaseCommand):


    def handle(self, **option):
         

        # self.step1()
        # self.step2()
        self.step3()
        # self.step4()
    def step3(self):
        names = self.fetch()
        self.split_thread(names)

    def step2(self):
        enterprise = Enterprise.objects.filter(level=2)

        names = [_.name for _ in enterprise]

        self.split_thread(names)

    def split_thread(self, names):
        pool = threadpool.ThreadPool(5) 

        requests = threadpool.makeRequests(self.split_, names) 
        [pool.putRequest(_) for _ in requests]
        pool.wait()

    def split_(self, name):
        # es = []
        # for name in names:
        name = strip_process(name)
        i = name
        i = complete(i)
        r = remark(i)
        e = EnterpriseSplit(
            source=name,
            name=r['name'],
            remark=' || '.join(r['remark']) if r['remark'] else None,
            area=r['area'] if 'area' in r else None,
            province=r['province'] if 'province' in r else None,
            level=4,
        )

        c = child(e.name)
        e.name = c['name']
        e.child = c['child']

        if not e.area and not e.province:
            c = city(e.name)
            e.name = c['name']
            e.province = c['province'] if 'province' in c else None
            e.area = c['area'] if 'area' in c else None

        t = type(e.name)

        e.name = t['name']
        e.type = t['type'] if 'type' in t else None

        if 'remark' in t and t['remark']:
            if not e.remark:
                e.remark = t['remark'] 
            else:
                e.remark = e.remark + ' || '+t['remark']
        if e.type:
            # es.append(e)
            e.save()
        # if len(es) == 300:
        #     EnterpriseSplit.objects.bulk_create(es)
        #     es = []

        # EnterpriseSplit.objects.bulk_create(es)  



    def step1(self):
        path = '/Users/dsc/Downloads/食品安全追溯/2018/enterprise.csv'
        data = pd.read_csv(path, dtype='unicode')

        enterprise_name = data['企业名称'].value_counts()

        a = enterprise_name.to_dict()
        print(len(a))

        # self.insert1(a)

        b = {}
        for i in a.keys():
            print(i)
            new = strip_process(i)
             
            if new in b:
                b[new].append(i)
            else:
                b[new] = [i]
             
        print(len(b))
        self.insert2(b, 2)


    def insert1(self, a):
        results = []
        for i in a.keys():
            p = Enterprise(name=i, count=a[i], level=1)
            results.append(p)

            if len(results) == 500:
                Enterprise.objects.bulk_create(results)
                results = []


        Enterprise.objects.bulk_create(results)


    def insert2(self, a, level):
        results = []

        for i in a.keys():
            p = Enterprise(name=i, count=len(a[i]), level=level, parent=' || '.join(a[i]))
            results.append(p)

            if len(results) == 500:
                Enterprise.objects.bulk_create(results)
                results = []


        Enterprise.objects.bulk_create(results)


    def fetch(self):
        names = []
        cursor=connection.cursor()
        sql = 'select distinct a.provider_name from (select distinct provider_name from thunder_accountin) a \
            left join data_enterprisesplit b \
            on a.provider_name = b.source \
            where b.id is null'

        cursor.execute(sql)
        
        raw = cursor.fetchall() #读取所
        
        for _ in raw:
            names.append(_[0])
        print(len(names))
        sql = 'select distinct a.manufacturer from \
            (select distinct manufacturer from thunder_accountin where manufacturer is not null and manufacturer!=provider_name) a\
            left join data_enterprisesplit b on a.manufacturer = b.source where b.id is null'

        cursor.execute(sql)
        
        raw = cursor.fetchall() #读取所
        
        for _ in raw:
            names.append(_[0])
        print(len(names))

        sql = 'select distinct a.manufacturer from (select distinct manufacturer from thunder_accountout where manufacturer is not null ) a\
        left join data_enterprisesplit b on  a.manufacturer = b.source where b.id is null'

        cursor.execute(sql)
        
        raw = cursor.fetchall() #读取所
        
        for _ in raw:
            names.append(_[0])
        print(len(names))

        sql = ' select distinct a.purchaser_name from (select distinct purchaser_name from thunder_accountout where purchaser_name is not null ) a\
            left join data_enterprisesplit b on  a.purchaser_name = b.source where b.id is null'

        cursor.execute(sql)
        
        raw = cursor.fetchall() #读取所
        
        for _ in raw:
            names.append(_[0])
        print(len(names))

        return names