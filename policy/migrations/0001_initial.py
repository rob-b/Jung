
from south.db import db
from django.db import models
from policy.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Programme'
        db.create_table('policy_programme', (
            ('id', models.AutoField(primary_key=True)),
            ('status', models.SmallIntegerField(_('status'))),
            ('name', models.CharField(_('Name'), max_length=150)),
            ('slug', AutoSlugField(populate_from='name', editable=True)),
            ('description', MarkdownField(_('Description'))),
            ('account', models.ForeignKey(orm.Account)),
            ('description_rendered', models.TextField(editable=False)),
        ))
        db.send_create_signal('policy', ['Programme'])
        
        # Adding model 'Project'
        db.create_table('policy_project', (
            ('id', models.AutoField(primary_key=True)),
            ('status', models.SmallIntegerField(_('status'))),
            ('name', models.CharField(_('Name'), max_length=150)),
            ('slug', AutoSlugField(populate_from='name', editable=True)),
            ('am', FK(related_name='am_for')),
            ('pm', FK(related_name='pm_for')),
            ('tech', FK(related_name='tech_lead_for')),
            ('design', FK(related_name='design_lead_for')),
            ('owner', FK(related_name='projects_owned')),
            ('programme', FK(to=orm.Programme)),
            ('account', FK(to=orm.Account, blank=False)),
            ('description', MarkdownField(_('Description'))),
            ('description_rendered', models.TextField(editable=False)),
        ))
        db.send_create_signal('policy', ['Project'])
        
        # Adding model 'Account'
        db.create_table('policy_account', (
            ('id', models.AutoField(primary_key=True)),
            ('status', models.SmallIntegerField(_('status'))),
            ('name', models.CharField(_('Name'), max_length=150)),
            ('slug', AutoSlugField(populate_from='name', editable=True)),
            ('colour', models.CharField(_('Colour'), max_length=6, blank=True)),
            ('description', MarkdownField(_('Description'))),
            ('description_rendered', models.TextField(editable=False)),
        ))
        db.send_create_signal('policy', ['Account'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Programme'
        db.delete_table('policy_programme')
        
        # Deleting model 'Project'
        db.delete_table('policy_project')
        
        # Deleting model 'Account'
        db.delete_table('policy_account')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'policy.programme': {
            'account': ('models.ForeignKey', ["orm['policy.Account']"], {}),
            'description': ('MarkdownField', ["_('Description')"], {}),
            'description_rendered': ('models.TextField', [],{'editable':'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', ["_('Name')"], {'max_length': '150'}),
            'slug': ('AutoSlugField', [], {'populate_from': "'name'", 'editable': 'True'}),
            'status': ('models.SmallIntegerField', ["_('status')"], {})
        },
        'policy.project': {
            'account': ('FK', [], {'to': "'Account'", 'blank': 'False'}),
            'am': ('FK', [], {'related_name': "'am_for'"}),
            'description': ('MarkdownField', ["_('Description')"], {}),
            'description_rendered': ('models.TextField', [],{'editable':'False'}),
            'design': ('FK', [], {'related_name': "'design_lead_for'"}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', ["_('Name')"], {'max_length': '150'}),
            'owner': ('FK', [], {'related_name': "'projects_owned'"}),
            'pm': ('FK', [], {'related_name': "'pm_for'"}),
            'programme': ('FK', [], {'to': "'Programme'"}),
            'slug': ('AutoSlugField', [], {'populate_from': "'name'", 'editable': 'True'}),
            'status': ('models.SmallIntegerField', ["_('status')"], {}),
            'tech': ('FK', [], {'related_name': "'tech_lead_for'"})
        },
        'policy.account': {
            'colour': ('models.CharField', ["_('Colour')"], {'max_length': '6', 'blank': 'True'}),
            'description': ('MarkdownField', ["_('Description')"], {}),
            'description_rendered': ('models.TextField', [],{'editable':'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', ["_('Name')"], {'max_length': '150'}),
            'slug': ('AutoSlugField', [], {'populate_from': "'name'", 'editable': 'True'}),
            'status': ('models.SmallIntegerField', ["_('status')"], {})
        }
    }
    
    complete_apps = ['policy']
