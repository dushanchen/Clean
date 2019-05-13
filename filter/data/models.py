# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class ProductName(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '商品类目'

		indexes = [
			models.Index(
                fields=['level'],
                name='level_idx',
            ),
            models.Index(
                fields=['name'],
                name='name_idx',
            ),
		]
	name = models.CharField(max_length=500)
	count = models.IntegerField()
	level = models.IntegerField()

	parent = models.TextField(max_length=10000, null=True)
	create_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class ProductNameSpecs(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '商品类目二'

	source = models.CharField(max_length=500)
	name = models.CharField(max_length=500, null=True)
	volumn = models.CharField(max_length=100, null=True)
	weight = models.CharField(max_length=100, null=True)
	amount = models.CharField(max_length=100, null=True)
	length = models.CharField(max_length=100, null=True)
	unit = models.CharField(max_length=20, null=True)
	remark = models.CharField(max_length=200, null=True)

	level = models.IntegerField()
	create_time = models.DateTimeField(auto_now_add=True)


class Enterprise(models.Model):
	class Meta:
		verbose_name = verbose_name_plural = '公司名称'
		indexes = [
			models.Index(
                fields=['level'],
                name='enterprise_level_idx',
            ),
            models.Index(
                fields=['name'],
                name='enterprise_name_idx',
            ),
		]
	name = models.CharField(max_length=200)
	count = models.IntegerField()
	level = models.IntegerField()

	parent = models.CharField(max_length=200)
	create_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class EnterpriseSplit(models.Model):
	class Meta:
		verbose_name_plural = verbose_name = '公司名称分析'
		indexes = [
			models.Index(
                fields=['level'],
                name='EnterpriseSplit_level_idx',
            ),
            models.Index(
                fields=['name'],
                name='EnterpriseSplit_name_idx',
            ),
		]
	source = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	child = models.CharField(max_length=100, null=True)
	province = models.CharField(max_length=20, null=True)
	area = models.CharField(max_length=100, null=True)
	type = models.CharField(max_length=100, null=True)

	remark = models.CharField(max_length=100, null=True)

	level = models.IntegerField()
	create_time = models.DateTimeField(auto_now_add=True)
