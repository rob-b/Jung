
from south.db import db
from django.db import models
from schedule.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Task.project'
        db.add_column('schedule_task', 'project', models.ForeignKey(orm['policy.Project']))
        
    
    def backwards(self, orm):
        
        # Deleting field 'Task.project'
        db.delete_column('schedule_task', 'project_id')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'schedule.tasktype': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'title': ('models.CharField', ["_('Title')"], {'unique': 'True', 'max_length': '100'})
        },
        'policy.project': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'schedule.task': {
            'author': ('models.ForeignKey', ["orm['auth.User']"], {'related_name': "'tasks_created'"}),
            'body': ('MarkdownField', ["_('Body')"], {'blank': 'True'}),
            'body_rendered': ('models.TextField', [],{'editable':'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'project': ('models.ForeignKey', ["orm['policy.Project']"], {}),
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
