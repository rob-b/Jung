
from south.db import db
from django.db import models
from schedule.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Task.status'
        db.add_column('schedule_task', 'status', orm['schedule.Task:status'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Task.status'
        db.delete_column('schedule_task', 'status')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'policy.account': {
            'colour': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'description': ('MarkdownField', ["_('Description')"], {}),
            'description_rendered': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'slug': ('AutoSlugField', [], {'populate_from': "'name'", 'editable': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'policy.programme': {
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['policy.Account']"}),
            'description': ('MarkdownField', ["_('Description')"], {}),
            'description_rendered': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'slug': ('AutoSlugField', [], {'populate_from': "'name'", 'editable': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'policy.project': {
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['policy.Account']", 'null': 'True'}),
            'account_manager': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'am_for'", 'null': 'True', 'to': "orm['auth.User']"}),
            'description': ('MarkdownField', ["_('Description')"], {}),
            'description_rendered': ('django.db.models.fields.TextField', [], {}),
            'design_lead': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'design_lead_for'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'projects_owned'", 'null': 'True', 'to': "orm['auth.User']"}),
            'programme': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['policy.Programme']", 'null': 'True', 'blank': 'True'}),
            'project_manger': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'pm_for'", 'null': 'True', 'to': "orm['auth.User']"}),
            'slug': ('AutoSlugField', [], {'populate_from': "'name'", 'editable': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {}),
            'technical_lead': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tech_lead_for'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'schedule.occurrence': {
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.Task']"})
        },
        'schedule.task': {
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tasks_created'", 'to': "orm['auth.User']"}),
            'body': ('MarkdownField', ["_('Body')"], {'blank': 'True'}),
            'body_rendered': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['policy.Project']"}),
            'slug': ('AutoSlugField', ["_('Slug')"], {'editable': 'True', 'populate_from': "'title'"}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'task_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['schedule.TaskType']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'schedule.tasktype': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }
    
    complete_apps = ['schedule']
