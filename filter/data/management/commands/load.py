from django.core.management import BaseCommand

from data.models import * 
from data.process import *


import re
import json
import pandas as pd

class Command(BaseCommand):


    def handle(self, **option):
         
        # self.step1()
        # self.step2()
        self.step3()
        # self.step4()

    

    def step3(self):
        names = ProductName.objects.filter(level=3)

        record = []
        for i in names:
            var = specs_split(i.name)
            
            p = ProductNameSpecs(
                source=i.name,
                name=var['name'] if 'name' in var else None,
                level=4,
                volumn=var['volumn'] if 'volumn' in var else None,
                weight=var['weight'] if 'weight' in var else None,
                amount=var['amount'] if 'amount' in var else None,
                length=var['length'] if 'length' in var else None,
                unit=var['unit'] if 'unit' in var else None,
            )

            if not p.name:
                remark = remarks2(i.name)
            else:
                remark = remarks1(p.name)

            if remark:
                p.name = remark['name']
                p.remark = remark['remark']

            record.append(p)

            if len(record) == 500:
                ProductNameSpecs.objects.bulk_create(record)
                record = []

        ProductNameSpecs.objects.bulk_create(record)


    def step2(self):
        names = ProductName.objects.filter(level=2)

        b = {}

        for i in names:
            name = i.name
            new = specs_process(name)
            if new != name:
                print(name, '  --->  ', new)

            if new in b:
                b[new].append(name)
            else:
                b[new] = [name]

        print(len(b))
        self.insert2(b, 3)


    def step1(self):
        path = '/Users/dsc/Downloads/食品安全追溯/2018/product.csv'
        data = pd.read_csv(path, dtype='unicode')

        product_name = data['产品名称'].value_counts()

        a = product_name.to_dict()
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


    def insert2(self, b, level):
        results = []
        for i in b.keys():
            p = ProductName(name=i, count=len(b[i]), level=level, parent=' || '.join(b[i]))
            results.append(p)

            if len(results) == 200:
                ProductName.objects.bulk_create(results)
                results = []


        ProductName.objects.bulk_create(results)


    def insert1(self, a):
        results = []
        for i in a.keys():
            p = ProductName(name=i, count=a[i], level=1)
            results.append(p)

            if len(results) == 200:
                ProductName.objects.bulk_create(results)
                results = []


        ProductName.objects.bulk_create(results)
