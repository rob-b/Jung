
from south.db import db
from django.db import models
from policy.models import *

class Migration:

    def forwards(self, orm):

        # Adding field 'Project.account_manager'
        db.add_column('policy_project', 'account_manager',
                      FK(related_name='account_manager_for'))

        # Adding field 'Project.design_lead'
        db.add_column('policy_project', 'design_lead', FK(related_name='design_lead_for'))

        # Adding field 'Project.project_manger'
        db.add_column('policy_project', 'project_manger',
                      FK(related_name='project_manager_for'))

        # Adding field 'Project.technical_lead'
        db.add_column('policy_project', 'technical_lead',
                      FK(related_name='technical_lead_for'))

        # Deleting field 'Project.tech'
        db.delete_column('policy_project', 'tech_id')

        # Deleting field 'Project.am'
        db.delete_column('policy_project', 'am_id')

        # Deleting field 'Project.pm'
        db.delete_column('policy_project', 'pm_id')

        # Deleting field 'Project.design'
        db.delete_column('policy_project', 'design_id')

    def backwards(self, orm):

        # Deleting field 'Project.account_manager'
        db.delete_column('policy_project', 'account_manager_id')

        # Deleting field 'Project.design_lead'
        db.delete_column('policy_project', 'design_lead_id')

        # Deleting field 'Project.project_manger'
        db.delete_column('policy_project', 'project_manger_id')

        # Deleting field 'Project.technical_lead'
        db.delete_column('policy_project', 'technical_lead_id')

        # Adding field 'Project.tech'
        db.add_column('policy_project', 'tech', FK(related_name='tech_lead_for'))

        # Adding field 'Project.am'
        db.add_column('policy_project', 'am', FK(related_name='am_for'))

        # Adding field 'Project.pm'
        db.add_column('policy_project', 'pm', FK(related_name='pm_for'))

        # Adding field 'Project.design'
        db.add_column('policy_project', 'design', FK(related_name='design_lead_for'))


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
            'account_manager': ('FK', [], {'related_name': "'am_for'"}),
            'description': ('MarkdownField', ["_('Description')"], {}),
            'description_rendered': ('models.TextField', [],{'editable':'False'}),
            'design_lead': ('FK', [], {'related_name': "'design_lead_for'"}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', ["_('Name')"], {'max_length': '150'}),
            'owner': ('FK', [], {'related_name': "'projects_owned'"}),
            'programme': ('FK', [], {'to': "'Programme'"}),
            'project_manger': ('FK', [], {'related_name': "'pm_for'"}),
            'slug': ('AutoSlugField', [], {'populate_from': "'name'", 'editable': 'True'}),
            'status': ('models.SmallIntegerField', ["_('status')"], {}),
            'technical_lead': ('FK', [], {'related_name': "'tech_lead_for'"})
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
