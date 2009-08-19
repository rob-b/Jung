
from south.db import db
from django.db import models
from schedule.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'TaskType'
        db.create_table('schedule_tasktype', (
            ('id', models.AutoField(primary_key=True)),
            ('title', models.CharField(_('Title'), unique=True, max_length=100)),
        ))
        db.send_create_signal('schedule', ['TaskType'])
        
        # Adding model 'Task'
        db.create_table('schedule_task', (
            ('id', models.AutoField(primary_key=True)),
            ('title', models.CharField(_('Title'), max_length=100)),
            ('slug', AutoSlugField(_('Slug'), editable=True, populate_from='title')),
            ('body', MarkdownField(_('Body'), blank=True)),
            ('author', models.ForeignKey(orm['auth.User'], related_name='tasks_created')),
            ('user', models.ForeignKey(orm['auth.User'])),
            ('task_type', models.ForeignKey(orm.TaskType)),
            ('body_rendered', models.TextField(editable=False)),
        ))
        db.send_create_signal('schedule', ['Task'])
        
        # Adding model 'Occurrence'
        db.create_table('schedule_occurrence', (
            ('id', models.AutoField(primary_key=True)),
            ('start_time', models.DateTimeField()),
            ('end_time', models.DateTimeField()),
            ('task', models.ForeignKey(orm.Task)),
        ))
        db.send_create_signal('schedule', ['Occurrence'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'TaskType'
        db.delete_table('schedule_tasktype')
        
        # Deleting model 'Task'
        db.delete_table('schedule_task')
        
        # Deleting model 'Occurrence'
        db.delete_table('schedule_occurrence')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'schedule.tasktype': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'title': ('models.CharField', ["_('Title')"], {'unique': 'True', 'max_length': '100'})
        },
        'schedule.task': {
            'author': ('models.ForeignKey', ["orm['auth.User']"], {'related_name': "'tasks_created'"}),
            'body': ('MarkdownField', ["_('Body')"], {'blank': 'True'}),
            'body_rendered': ('models.TextField', [],{'editable':'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'slug': ('AutoSlugField', ["_('Slug')"], {'editable': 'True', 'populate_from': "'title'"}),
            'task_type': ('models.ForeignKey', ["orm['schedule.TaskType']"], {}),
            'title': ('models.CharField', ["_('Title')"], {'max_length': '100'}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {})
        },
        'schedule.occurrence': {
            'Meta': {'ordering': "['-start_time']"},
            'end_time': ('models.DateTimeField', [], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'start_time': ('models.DateTimeField', [], {}),
            'task': ('models.ForeignKey', ["orm['schedule.Task']"], {})
        }
    }
    
    complete_apps = ['schedule']
