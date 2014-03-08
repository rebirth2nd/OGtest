# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Store'
        db.create_table(u'shop_store', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'shop', ['Store'])

        # Adding model 'Manufacturer'
        db.create_table(u'shop_manufacturer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('category', self.gf('django.db.models.fields.CharField')(default='MISC', max_length=100)),
        ))
        db.send_create_signal(u'shop', ['Manufacturer'])

        # Adding model 'Product'
        db.create_table(u'shop_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('store', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Store'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('manufacturer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Manufacturer'])),
            ('dollar_price', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'shop', ['Product'])


    def backwards(self, orm):
        # Deleting model 'Store'
        db.delete_table(u'shop_store')

        # Deleting model 'Manufacturer'
        db.delete_table(u'shop_manufacturer')

        # Deleting model 'Product'
        db.delete_table(u'shop_product')


    models = {
        u'shop.manufacturer': {
            'Meta': {'object_name': 'Manufacturer'},
            'category': ('django.db.models.fields.CharField', [], {'default': "'MISC'", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'shop.product': {
            'Meta': {'object_name': 'Product'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'dollar_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Manufacturer']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['shop.Store']"})
        },
        u'shop.store': {
            'Meta': {'object_name': 'Store'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['shop']