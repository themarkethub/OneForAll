#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Insightly API Test Script
# Brian McConnell <brian@insightly.com>
#
# This Python module implements a test suite against the API. This allows users to create
# whatever test cases they want in addition to the standard set of tests we run against
# API endpoints.
#
# USAGE:
#
# i = Insightly()
# mobile_failures = i.test_mobile()
# v21_failures = i.test_v21()
# v22_failures = i.test_v22()
#
# NOTE:
#
# If you run the test suite, we recommend running it against a test instance with dummy data,
# as there is the potential for data loss or the insertion of dummy records.
#
# The test suite is primarily intended for use in QA testing.
# 

import datetime
import string
import time
from insightly import Insightly

dummy_comment = {u'TITLE':u'こんにちは世界',u'BODY':u'The body'}
dummy_contact = {u'FIRST_NAME':u'こんにちは世界', u'LAST_NAME':u'Barzle'}
dummy_email = {}
dummy_event = {u'TITLE':u'こんにちは世界',u'START_DATE_UTC':'2015-12-01 15:15:12',u'END_DATE_UTC':'2015-12-13 16:15:00'}
dummy_lead = dummy_contact
dummy_note = {u'TITLE':u'こんにちは世界',u'BODY':u'The body'}
dummy_organisation = {u'ORGANISATION_NAME':u'こんにちは世界'}
dummy_opportunity = {u'OPPORTUNITY_NAME':u'こんにちは世界','OPPORTUNITY_STATE':'OPEN'}
dummy_project = {u'PROJECT_NAME':u'こんにちは世界',u'STATUS':u'Not Started'}

def average_time(apikey='', dev='https://mobileapi.insightly.com', repetitions=10):
    f = open('timer.txt','w')
    
    versions = ['mobile','2.2']
    
    for v in versions:
        i = Insightly(apikey=apikey, version=v)
        users = i.users
        user_id = None
        if users is not None:
            user_id = users[0]['USER_ID']
        i.cruds('contacts', 'CONTACT_ID', dummy_contact, file_handle=f, repetitions=repetitions)
        i.cruds('events','EVENT_ID', dummy_event, file_handle=f, repetitions=repetitions)
        i.cruds('leads','LEAD_ID', dummy_lead, file_handle=f, repetitions=repetitions)
        i.cruds('organisations','ORGANISATION_ID', dummy_organisation, file_handle=f, repetitions=repetitions)
        i.cruds('opportunities','OPPORTUNITY_ID', dummy_opportunity, file_handle=f, repetitions=repetitions)
        i.cruds('projects','PROJECT_ID',dummy_project, file_handle=f, repetitions=repetitions)
        if user_id is not None:
            i.cruds('tasks','TASK_ID',
                    {u'TITLE':'Test',u'STATUS':u'NOT STARTED',u'COMPLETED':False,u'PUBLICLY_VISIBLE':True,u'RESPONSIBLE_USER_ID':user_id},
                    file_handle=f, repetitions=repetitions)
        
        f.write('\n')
        f.write('\nTESTS RUN:   ' + str(i.tests_run))
        f.write('\nTESTS PASSED:' + str(i.tests_passed))
        f.write('\nPASS RATE:   ' + str(100 * float(i.tests_passed) / float(i.tests_run)))
        f.write('\n\n')

def test_mobile(apikey='', dev='https://mobileapi.insightly.com'):
    i = Insightly(apikey=apikey, version='mobile', dev=dev, test=True)
    i.tests_run = 0
    i.tests_passed = 0
    
    # Check incremental update endpoints
    stats = i.read('IncrementalUpdateStats?updated_after_utc=2015-11-01')
    # TODO: Ask Evgeny about behavior for CheckRecords
    
    # Get a user id for use with endpoints that need a user assigned
    users = i.read('users', top=1)
    user_id = users[0]['USER_ID']
    responsible_user_id = user_id
    
    # Check commments endpoints
    comments = i.read('Comments?updated_after_utc=2015-11-01&top=10')
    i.record_count('comments')
    if len(comments) > 0:
        comment = comments[0]
        comment_id = comment['COMMENT_ID']
        comment = i.read('Comments', comment_id)
        if type(comment) is list:
            comment = comment[0]
        details = i.read('Comments', comment_id, 'full')
        comment = i.update('comments', comment)
        i.upload('comments', comment_id, 'apollo17.jpg')
        i.delete('comments', comment_id)
    
    # Check contacts endpoints
    
    contacts = i.read('Contacts?updated_after_utc=2015-10-01&top=10')
    i.record_count('contacts')
    if len(contacts) > 0:
        contact = contacts[0]
        contact = i.update('contacts', contact)
        contact_id = contact['CONTACT_ID']
        contact = i.read('Contacts', contact_id)
        if type(contact) is list:
            contact = contact[0]
        i.create_child('contacts', contact_id, 'follow', {})
        i.delete('contacts', contact_id, 'follow')
        i.create_child('contacts', contact_id, 'notes', dummy_note)
        i.upload('contacts', contact_id, 'apollo17.jpg')
        i.upload_image('contacts', contact_id, 'apollo17.jpg')
        i.delete('contacts', contact_id, 'image')
        details = i.read('Contacts', contact_id, 'full')
        contact = i.update('Contacts', contact)
        contact = dummy_contact
        contact = i.create('Contacts', contact)
        contact_id = contact['CONTACT_ID']
        organizations = i.read('organisations',top=5)
        if organizations is not None:
            if len(organizations) > 0:
                organization = organizations[0]
                organization_id = organization['ORGANISATION_ID']
                link = i.create_child('contacts',contact_id,'links',{'ORGANISATION_ID':organization_id})
                if link is not None:
                    i.delete('contacts',contact_id,sub_type='links',sub_type_id=link['LINK_ID'])
        try:
            second_contact_id = contacts[1]['CONTACT_ID']
            contact_link = i.create_child('contacts', contact_id, 'contactlinks',
                                  {'FIRST_CONTACT_ID':contact_id, 'SECOND_CONTACT_ID': second_contact_id,
                                   'RELATIONSHIP_ID':1})
            if link is not None:
                i.delete('contacts', contact_id, 'contactlinks', contact_link['CONTACT_LINK_ID'])
        except:
            pass
        # add test for contactlinks child endpoint, not clear for docs how to implement this one
        i.delete('Contacts', contact_id)

    # Check /emails endpoints
    
    emails = i.read('emails')
    i.record_count('emails')
    if len(emails) > 0:
        email = emails[0]
        email_id = email['EMAIL_ID']
        email = i.get('emails', email_id)
        details = i.read('emails', email_id, 'full')
        i.create_child('emails', email_id, 'follow', {})
        i.delete('emails', email_id, sub_type='follow')
        i.create_child('emails', email_id, 'comments', dummy_comment)
        
        contacts = i.read('contacts', top=1)
        contact_id = contacts[0]['CONTACT_ID']
        email_link = i.create_child('emails', email_id, 'emaillinks', {u'CONTACT_ID':contact_id})
        if email_link is not None:
            email_link_id = email_link['EMAIL_LINK_ID']
            i.delete('emails', email_id, 'emaillinks', email_link_id)
        
    # Check /events endpoints
    i.record_count('events')
    events = i.read('events')
    if len(events) > 0:
        event_id = events[0]['EVENT_ID']
        event = i.get('events', event_id)
        details = i.read('events', event_id, 'full')
        event = i.update('events', event)
        event = i.create('events',dummy_event)
        if event is not None:
            event_id = event['EVENT_ID']
            contacts = i.read('contacts', top=1)
            contact_id = contacts[0]['CONTACT_ID']
            event_link = i.create_child('events', event_id, 'eventlinks',{'CONTACT_ID':contact_id})
            if event_link is not None:
                i.delete('events', event_id, sub_type='eventlinks', sub_type_id=event_link['EVENT_LINK_ID'])
            i.delete('events',event['EVENT_ID'])
            
    # Check /fileattachments endpoints   
    file_attachments = i.read('fileattachments')
    if len(file_attachments) > 0:
        file_id = file_attachments[0]['FILE_ID']
        file_attachment = i.read('fileattachments', file_id)
        i.delete('fileattachments', file_id)
        
    # Check /leads endpoints
    i.record_count('leads')
    leads = i.read('leads')
    if len(leads) > 0:
        lead_id = leads[0]['LEAD_ID']
        lead = i.get('leads', lead_id)
        lead = i.update('leads', lead)
        i.create_child('leads', lead_id, 'follow', {})
        i.delete('leads', lead_id, sub_type='follow')
    lead = i.create('leads',dummy_lead)
    if lead is not None:
        i.upload('leads', lead_id, 'apollo17.jpg')
        i.upload_image('leads', lead_id, 'apollo17.jpg')
        i.create_child('leads', lead_id, 'notes', dummy_note)
        i.delete('leads', lead_id)    

    # Check /notes endpoints
    i.record_count('notes')
    notes = i.read('notes')
    if len(notes) > 0:
        note_id = notes[0]['NOTE_ID']
        details = i.get('notes', note_id, 'full')
        note = i.get('notes', note_id)
        note = i.update('notes', note)
        i.create_child('notes', note_id, 'follow', {})
        i.delete('notes', note_id, sub_type='follow')
        i.create_child('notes', note_id, 'comments', dummy_comment)
        i.upload('notes', note_id, 'apollo17.jpg')
        contacts = i.read('contacts')
        if len(contacts) > 0:
            contact_id = contacts[0]['CONTACT_ID']
            link = i.create_child('notes', note_id, 'notelinks', {'CONTACT_ID':contact_id})
            if link is not None:
                i.delete('notes', note_id, sub_type='notelinks', sub_type_id=link['NOTE_LINK_ID'])
                
    opportunities = i.read('opportunities')
    i.record_count('opportunities')
    if len(opportunities) > 0:
        opportunity_id = opportunities[0]['OPPORTUNITY_ID']
        opportunity = i.get('opportunities', opportunity_id)
        details = i.get('opportunities', opportunity_id, 'full')
    opportunity = dummy_opportunity
    opportunity['RESPONSIBLE_USER_ID'] = responsible_user_id
    opportunity = i.create('opportunities', opportunity)
    if opportunity is not None:
        opportunity = i.update('opportunities', opportunity)
        opportunity_id = opportunity['OPPORTUNITY_ID']
        i.update('opportunities/' + str(opportunity_id) + '/state', {'FOR_OPPORTUNITY_STATE':'Abandoned'})
        statehistory = i.read('opportunities', opportunity_id, 'statehistory')
        i.create_child('opportunities', opportunity_id, 'follow', {})
        i.delete('opportunities', opportunity_id, sub_type='follow')
        i.create_child('opportunities', opportunity_id, 'notes', dummy_note)
        i.upload('opportunities', opportunity_id, 'apollo17.jpg')
        contacts = i.read('contacts')
        if len(contacts) > 0:
            contact_id = contacts[0]['CONTACT_ID']
            link = i.create_child('opportunities', opportunity_id, 'links', {'CONTACT_ID':contact_id})
            if link is not None:
                i.delete('opportunities', opportunity_id, sub_type='links', sub_type_id=link['LINK_ID'])
        i.delete('opportunities', opportunity_id)
        
    # Check /Organisations endpoints    
    
    organisations = i.read('organisations')
    i.record_count('organisations')
    if len(organisations) > 0:
        organisation_id = organisations[0]['ORGANISATION_ID']
        link_organisation_id = organisation_id
        organisation = i.get('organisations', organisation_id)
        details = i.get('organisations', organisation_id, 'full')
    organisation = i.create('organisations', dummy_organisation)
    if organisation is not None:
        organisation = i.update('organisations', organisation)
        organisation_id = organisation['ORGANISATION_ID']
        i.create_child('organisations', organisation_id, 'follow', {})
        i.delete('organisations', organisation_id, sub_type='follow')
        i.upload_image('organisations', organisation_id, 'apollo17.jpg')
        i.upload('organisations', organisation_id, 'apollo17.jpg')
        i.create_child('organisations', organisation_id, 'notes', dummy_note)
        link = i.create_child('organisations', organisation_id, 'links', {'CONTACT_ID': contact_id})
        if link is not None:
            i.delete('organisations', organisation_id, sub_type='links', sub_type_id=link['LINK_ID'])
        link = i.create_child('organisations', organisation_id, 'organisationlinks',
                              {'FIRST_ORGANISATION_ID':organisation_id, 'SECOND_ORGANISATION_ID':link_organisation_id,
                               'RELATIONSHIP_ID':1})
        if link is not None:
            i.delete('organisations', organisation_id, sub_type='organisationlinks', sub_type_id=link['ORG_LINK_ID'])
        i.delete('organisations', organisation_id)
    
    projects = i.read('projects')
    i.record_count('projects')
    if projects is not None:
        project = projects[0]
        project_id = project['PROJECT_ID']
        project = i.get('projects', project_id)
        details = i.read('projects', project_id, 'full')
    pipeline_stages = i.read('pipelinestages')
    if pipeline_stages is not None:
        pipeline_id = pipeline_stages[0]['PIPELINE_ID']
        stage_id = pipeline_stages[0]['STAGE_ID']
    else:
        pipeline_id = None
        stage_id = None
    project = dummy_project
    project['RESPONSIBLE_USER_ID'] = responsible_user_id
    project = i.create('projects', project)
    if project is not None:
        if pipeline_id is not None:
            project['PIPELINE_ID'] = pipeline_id
            project['STAGE_ID'] = stage_id
        project = i.update('projects', project)
        project_id = project['PROJECT_ID']
        i.create_child('projects', project_id, 'follow', {})
        i.delete('projects', project_id, sub_type='follow')
        i.create_child('projects', project_id, 'notes', dummy_note)
        file_attachments = i.read('projects', project_id, 'fileattachments')
        i.upload('projects', project_id, 'apollo17.jpg')
        contacts = i.read('contacts', top=1)
        contact_id = contacts[0]['CONTACT_ID']
        link = i.create_child('projects', project_id, 'links', {'CONTACT_ID':contact_id})
        if link is not None:
            i.delete('projects', project_id, sub_type='links', sub_type_id=link['LINK_ID'])
        i.delete('projects', project_id)
        
    # Check /tags/{object} endpoints
    
    tagged_objects = ['contacts', 'leads', 'opportunities', 'organisations', 'projects']
    
    for t in tagged_objects:
        i.read('tags/' + t)
        
    # Check tasks endpoints
    
    tasks = i.read('tasks/myopen')
    tasks = i.read('tasks')
    i.record_count('tasks')
    if len(tasks) > 0:
        task = tasks[0]
        task_id = task['TASK_ID']
        tasks = i.read('tasks/' + str(task_id) + '/full')
        task = i.get('tasks', task_id)
        task = i.update('tasks', task)
        task = i.create('tasks', {u'TITLE':'Test',u'STATUS':u'NOT STARTED',u'COMPLETED':False,u'PUBLICLY_VISIBLE':True,u'RESPONSIBLE_USER_ID':user_id})
        if task is not None:
            task = i.update('tasks', task)
            task_id = task['TASK_ID']
            i.create_child('tasks', task_id, 'follow', {})
            i.delete('tasks', task_id, sub_type='follow')
            comment = i.create_child('tasks', task_id, 'comments', {'TITLE':'Foo','BODY':'Bar'})
            contacts = i.read('contacts', top=1)
            contact_id = contacts[0]['CONTACT_ID']
            link = i.create_child('tasks', task_id, 'tasklinks', {'CONTACT_ID':contact_id})
            if link is not None:
                link_id = link['TASK_LINK_ID']
                i.delete('tasks', task_id, sub_type='tasklinks', sub_type_id=link_id)
            i.delete('tasks', task_id)
        
    # Check system tables endpoints
    
    countries = i.read('countries')
    currencies = i.read('currencies')
    custom_fields = i.read('customfields')
    custom_field_groups = i.read('customfieldgroups')
    file_categories = i.read('filecategories')
    lead_sources = i.read('leadsources')
    lead_statuses = i.read('leadstatuses')
    opportunity_categories = i.read('opportunitycategories')
    opportunity_state_reasons = i.read('opportunitystatereasons')
    pipelines = i.read('pipelines')
    pipeline_stages = i.read('pipelinestages')
    project_categories = i.read('projectcategories')
    relationships = i.read('relationships')
    task_categories = i.read('taskcategories')
    teams = i.read('teams')
    team_id = teams[0]['TEAM_ID']
    team = i.read('teams', team_id)
    team_members = i.read('teammembers/my')
    users = i.read('users')
    user_id = users[0]['USER_ID']
    user = i.read('users', user_id)
    
    # Check misc/other endpoints
    
    accounts = i.read('accounts')
    task_links = i.read('tasklinks')
    note_links = i.read('notelinks')
    event_links = i.read('eventlinks')
    links = i.read('links')
    contact_links = i.read('contactlinks')
    organization_links = i.read('organisationlinks')
        
    print str(i.tests_passed) + ' of ' + str(i.tests_run) + ' passed for mobile API'
    print ''
    print 'Slow Endpoints ' + str(len(i.slow_endpoints))
    for s in i.slow_endpoints:
        print s
    print ''
    if len(i.test_failures) > 0:
        print 'Test Failures'
        print ''
        for f in i.test_failures:
            print f
            
    return i.test_failures
    
def test_v21(apikey='', dev=None):
    i = Insightly(apikey=apikey, version='2.1', dev=dev, test=True)
    i.tests_run = 0
    i.tests_passed = 0
    
    # Get a user id for use with endpoints that need a user assigned
    users = i.read('users', top=1)
    user_id = users[0]['USER_ID']    

    # test contacts
    contacts = i.read('contacts')
    if contacts is not None:
        contact_id = contacts[0]['CONTACT_ID']
        contact = i.get('contacts', contact_id)
    contact = i.create('contacts', dummy_contact)
    if contact is not None:
        contact = i.update('contacts', contact)
        contact_id = contact['CONTACT_ID']
        i.upload_image('contacts', contact_id, 'apollo17.jpg')
        tasks = i.read('contacts', contact_id, sub_type='tasks')
        emails = i.read('contacts', contact_id, sub_type='emails')
        organizations = i.read('organisations',top=5)
        if organizations is not None:
            if len(organizations) > 0:
                organization = organizations[0]
                organization_id = organization['ORGANISATION_ID']
                contact['LINKS'] = [{'ORGANISATION_ID':organization_id}]
                contact = i.update('contacts', contact)
        i.delete('contacts', contact_id)
    countries = i.read('countries')
    currencies = i.read('currencies')
    custom_fields = i.read('customfields')
    if custom_fields is not None:
        custom_field_id = custom_fields[0]['CUSTOM_FIELD_ID']
        custom_field = i.read('customfields', custom_field_id)
    emails = i.read('emails')
    if emails is not None:
        email_id = emails[0]['EMAIL_ID']
        email = i.read('emails', email_id)
        comments = i.read('emails', email_id, sub_type='/comments')
    events = i.read('events')
    file_categories = i.read('filecategories')
    if file_categories is not None:
        file_category_id = file_categories[0]['CATEGORY_ID']
        file_category = i.read('filecategories', file_category_id)
    leads = i.read('leads')
    if leads is not None:
        lead_id = leads[0]['LEAD_ID']
        lead = i.read('leads', lead_id)
    lead = i.create('leads', dummy_lead)
    if lead is not None:
        lead_id = lead['LEAD_ID']
        lead['FIRST_NAME']='foozle'
        lead = i.update('leads', lead)
        i.upload_image('leads', lead_id, 'apollo17.jpg')
        i.delete('leads', lead_id, sub_type='image')
        notes = i.read('leads', lead_id, sub_type='notes')
        tasks = i.read('leads', lead_id, sub_type='tasks')
        emails = i.read('leads', lead_id, sub_type='emails')
        i.delete('leads', lead_id)
    lead = i.create('leads', dummy_lead)
    if lead is not None:
        lead_id = lead['LEAD_ID']
        response = i.create_child('leads', lead_id, 'convert', {'OPPORTUNITY_NAME':'Convert Me'})
    leadsources = i.read('leadsources')
    lead_source = i.create('leadsources', {u'LEAD_SOURCE':u'Foozle Barzle'})
    if lead_source is not None:
        lead_source['LEAD_SOURCE'] = 'Barzle Foozle'
        lead_source_id = lead_source['LEAD_SOURCE_ID']
        lead_source = i.update('leadsources', lead_source)
        i.delete('leadsources', lead_source_id)
    lead_statuses = i.read('leadstatuses')
    lead_status = i.create('leadstatuses', {u'LEAD_STATUS':u'Foozle'})
    if lead_status is not None:
        lead_status_id = lead_status['LEAD_STATUS_ID']
        lead_status['LEAD_STATUS']='Barzle'
        lead_status['STATUS_TYPE']=1
        lead_status = i.update('leadstatuses', lead_status)
        i.delete('leadstatuses', lead_status_id)
    notes = i.read('notes')
    if notes is not None:
        note_id = notes[0]['NOTE_ID']
        note = i.read('notes', note_id)
        comments = i.read('notes', note_id, sub_type='comments')
    opportunities = i.read('opportunities')
    if opportunities is not None:
        opportunity_id = opportunities[0]['OPPORTUNITY_ID']
        opportunity = i.read('opportunities', opportunity_id)
        opportunity = i.create('opportunities', dummy_opportunity)
        if opportunity is not None:
            opportunity['OPPORTUNITY_NAME'] = 'Barzle'
            opportunity_id = opportunity['OPPORTUNITY_ID']
            opportunity = i.update('opportunities', opportunity)
            i.upload_image('opportunities', opportunity_id, 'apollo17.jpg')
            i.delete('opportunities', opportunity_id, 'image')
            notes = i.read('opportunities', opportunity_id, sub_type='notes')
            opportunity_state_reasons = i.read('opportunities', opportunity_id, sub_type='statehistory')
            tasks = i.read('opportunities', opportunity_id, sub_type='tasks')
            emails = i.read('opportunities', opportunity_id, sub_type='emails')
            i.delete('opportunities', opportunity_id)
    opportunity_categories = i.read('opportunitycategories')
    opportunity_state_reasons = i.read('opportunitystatereasons')
    
    organisations = i.read('organisations')
    if organisations is not None:
        organisation_id = organisations[0]['ORGANISATION_ID']
        organisation = i.read('organisations', organisation_id)
        organisation = i.create('organisations', dummy_organisation)
        if organisation is not None:
            organisation_id = organisation['ORGANISATION_ID']
            organisation['ORGANISATION_NAME']='Bar Corporation'
            organisation = i.update('organisations', organisation)
            i.upload_image('organisations', organisation_id, 'apollo17.jpg')
            i.delete('organisations', organisation_id, sub_type='image')
            notes = i.read('organisations', organisation_id, sub_type='notes')
            emails = i.read('organisations', organisation_id, sub_type='emails')
            tasks = i.read('organisations', organisation_id, sub_type='tasks')
            i.delete('organisations', organisation_id)
    
    pipelines = i.read('pipelines')
    if pipelines is not None:
        pipeline_id = pipelines[0]['PIPELINE_ID']
        pipeline = i.read('pipelines', pipeline_id)
        
    pipeline_stages = i.read('pipelinestages')
    if pipeline_stages is not None:
        stage_id = pipeline_stages[0]['STAGE_ID']
        pipeline_stage = i.read('pipelinestages', stage_id)
    else:
        stage_id = None
        pipeline_id = None
    
    projects = i.read('projects')
    if projects is not None:
        project_id = projects[0]['PROJECT_ID']
        project = i.read('projects', project_id)
        project = i.create('projects', dummy_project)
        if project is not None:
            project_id = project['PROJECT_ID']
            project['PROJECT_NAME']='Barzle Corporation'
            if stage_id is not None:
                project['PIPELINE_ID'] = pipeline_id
                project['STAGE_ID'] = stage_id
            project = i.update('projects', project)
            i.upload_image('projects', project_id, 'apollo17.jpg')
            i.delete('projects', project_id, sub_type='image')
            notes = i.read('projects', project_id, sub_type='notes')
            tasks = i.read('projects', project_id, sub_type='tasks')
            emails = i.read('projects', project_id, sub_type='emails')
            i.delete('projects', project_id)
    relationships = i.read('relationships')
    task_categories = i.read('taskcategories')
    tasks = i.read('tasks')
    if tasks is not None:
        task_id = tasks[0]['TASK_ID']
        task = i.read('tasks', task_id)
    users = i.read('users')
    if users is not None:
        user_id = users[0]['USER_ID']
        user = i.read('users', user_id)
    else:
        user_id = None
    #me = i.read('users/me')
    if user_id is not None:
        task = i.create('tasks', {u'TITLE':'Test',u'STATUS':u'NOT STARTED',u'COMPLETED':False,u'PUBLICLY_VISIBLE':True,u'RESPONSIBLE_USER_ID':user_id, u'OWNER_USER_ID':user_id})
        if task is not None:
            task_id = task['TASK_ID']
            task = i.update('tasks', task)
            comments = i.read('tasks', task_id, sub_type='comments')
            i.delete('tasks', task_id)
    team_members = i.read('teammembers')
    if team_members is not None:
        team_member_id = team_members[0]['PERMISSION_ID']
        team_member = i.read('teammembers', team_member_id)
    
    teams = i.read('teams')
    if teams is not None:
        team_id = teams[0]['TEAM_ID']
        team = i.read('teams', team_id)
        team = i.create('teams',{u'TEAM_NAME':u'Team Foo',u'ANONYMOUS_TEAM':False})
        if team is not None:
            team_id = team['TEAM_ID']
            team['TEAM_NAME'] = 'Team Bar'
            team = i.update('teams', team)
            i.delete('teams', team_id)
        
    failures = list()
    
    print(str(i.tests_passed) + ' out of ' + str(i.tests_run) + ' passed')
    if len(i.test_failures) > 0:
        print ('')
        print ('Test Failures')
        for f in i.test_failures:
            print (f)
            failures.append(f)
            
    return i.test_failures

def test_v22(apikey='', dev=None):
    i = Insightly(apikey=apikey, version='2.2', dev=dev, test=True)
    i.tests_run = 0
    i.tests_passed = 0
    
    # test permissions, create object with visible_to=owner, switch API key, view
    
    apikeys = list()
    
    try:
        f = open('api-keys.csv','r')
        text = f.read()
        rows = string.split(text,'\n')
        for r in rows:
            cols = string.split(r,',')
            if len(cols) == 5:
                apikeys.append(cols[4])
    except:
        apikeys = None
    
    if apikeys is not None:
        i.apikey = apikeys[0]
        contact = dummy_contact
        contact[u'VISIBLE_TO'] = u'OWNER'
        contact = i.create('contacts', contact)
        contact_id = contact['CONTACT_ID']
        i.apikey = apikeys[1]
        i.tests_run += 1
        try:
            contact = i.get('contacts', contact_id)
            i.printline('FAIL: /contacts permissions')
        except:
            i.tests_passed += 1
            i.printline('PASS: /contacts permissions')
            
        i.apikey = apikeys[0]
        contacts = i.search('contacts','first_name=' + dummy_contact['FIRST_NAME'])
        i.delete('contacts', contact_id)
        
        event = dummy_event
        event[u'PUBLICLY_VISIBLE'] = False
        event = i.create('events', event)
        event_id = event['EVENT_ID']
        i.apikey = apikeys[1]
        i.tests_run += 1
        try:
            event = i.get('events', event_id)
            i.printline('FAIL: /events permissions')
        except:
            i.tests_passed += 1
            i.printline('PASS: /events permissions')
        
        i.apikey = apikeys[0]
        i.delete('events', event_id)
        
        lead = dummy_lead
        lead[u'VISIBLE_TO'] = u'OWNER'
        lead = i.create('leads', lead)
        lead_id = lead['LEAD_ID']
        leads = i.search('leads','first_name=' + dummy_lead['FIRST_NAME'])
        i.apikey = apikeys[1]
        i.tests_run += 1
        try:
            lead = i.get('leads', lead_id)
            i.printline('FAIL: /leads permissions')
        except:
            i.tests_passed ++ 1
            i.printline('PASS: /leads permissions')
            
        i.apikey = apikeys[0]
        i.delete('leads', lead_id)
        
        opportunity = dummy_opportunity
        opportunity[u'VISIBLE_TO'] = u'OWNER'
        opportunity = i.create('opportunities', opportunity)
        opportunity_id = opportunity['OPPORTUNITY_ID']
        opportunities = i.search('opportunities', 'opportunity_name=' + dummy_opportunity['OPPORTUNITY_NAME'])
        i.apikey = apikeys[1]
        i.tests_run += 1
        try:
            opportunity = i.get('opportunities', opportunity_id)
            i.printline('FAIL: /opportunities permissions')
        except:
            i.tests_passed ++ 1
            i.printline('PASS: /opportunities permissions')
            
        i.apikey = apikeys[0]
        i.delete('opportunities', opportunity_id)
            
        organisation = dummy_organisation
        organisation[u'VISIBLE_TO'] = u'OWNER'
        organisation = i.create('organisations', organisation)
        organisation_id = organisation['ORGANISATION_ID']
        organizations = i.search('organisations', 'organisation_name=' + dummy_organisation['ORGANISATION_NAME'])
        i.apikey = apikeys[1]
        i.tests_run += 1
        try:
            organisation = i.get('organisations', organisation_id)
            i.printline('FAIL: /organisations permissions')
        except:
            i.tests_passed += 1
            i.printline('PASS: /organisations permissions')
            
        i.apikey = apikeys[0]
        i.delete('organisations', organisation_id)
        
        project = dummy_project
        project[u'VISIBLE_TO'] = u'OWNER'
        project = i.create('projects', project)
        project_id = project['PROJECT_ID']
        projects = i.search('projects', 'project_name=' + dummy_project['PROJECT_NAME'])
        i.apikey = apikeys[1]
        i.tests_run += 1
        try:
            project = i.get('projects', project_id)
            i.printline('FAIL: /projects permissions')
        except:
            i.tests_passed += 1
            i.printline('PASS: /projects permissions')
            
        i.apikey = apikeys[0]
        i.delete('projects', project_id)
    
    # test activity sets
    activity_sets = i.read('activitysets')
    if activity_sets is not None:
        activity_set_id = activity_sets[0]['ACTIVITYSET_ID']
        activity_set = i.read('activitysets', id=activity_set_id)
    # test contacts
    contacts = i.read('contacts')
    if contacts is not None:
        if len(contacts) > 0:
            contact_id = contacts[0]['CONTACT_ID']
            contact = i.get('contacts', contact_id)
    contact = {'FIRST_NAME':u'Test',u'LAST_NAME':u'ミスターマコーネル'}
    contact = i.create('contacts', contact)
    if contact is not None:
        contact = i.update('contacts', contact)
        contact_id = contact['CONTACT_ID']
        i.upload_image('contacts', contact_id, 'apollo17.jpg')
        address = i.create_child('contacts', contact_id, 'addresses', {u'ADDRESS_TYPE':u'HOME',u'CITY':u'San Francisco', u'STATE':u'CA', u'COUNTRY':u'United States'})
        if address is not None:
            address_id = address['ADDRESS_ID']
            i.delete('contacts',contact_id,sub_type='addresses',sub_type_id=address_id)
        contactinfo = i.create_child('contacts', contact_id, 'contactinfos', {u'TYPE':u'EMAIL',u'SUBTYPE':u'Home',u'DETAIL':u'foo@bar.com'})
        if contactinfo is not None:
            contact_info_id = contactinfo['CONTACT_INFO_ID']
            i.delete('contacts', contact_id, sub_type='contactinfos', sub_type_id = contact_info_id)
        contact_date = {u'OCCASION_NAME':u'Birthday',u'OCCASION_DATE':'2016-05-02T12:00:00Z'}
        contact_date = i.create_child('contacts', contact_id, 'dates', contact_date)
        if contact_date is not None:
            date_id = contact_date['DATE_ID']
            i.delete('contacts', contact_id, sub_type='dates', sub_type_id=date_id)
        tag = {u'TAG_NAME':'foo'}
        i.create_child('contacts', contact_id, 'tags', tag)
        i.delete('contacts', contact_id,sub_type='tags', sub_type_id = 'foo')
        note = {'TITLE':'Test', 'BODY':'This is the body'}
        note = i.create_child('contacts', contact_id, 'notes', note)
        events = i.read('contacts', contact_id, sub_type='events')
        file_attachments = i.read('contacts', contact_id, sub_type='fileattachments')
        i.upload('contacts', contact_id, 'apollo17.jpg')
        i.create_child('contacts', contact_id, 'follow', {})
        i.delete('contacts', contact_id, sub_type='follow')
        tasks = i.read('contacts', contact_id, sub_type='tasks')
        emails = i.read('contacts', contact_id, sub_type='emails')
        organizations = i.read('organisations',top=5)
        if organizations is not None:
            if len(organizations) > 0:
                organization = organizations[0]
                organization_id = organization['ORGANISATION_ID']
                link = i.create_child('contacts',contact_id,'links',{'ORGANISATION_ID':organization_id})
                if link is not None:
                    i.delete('contacts',contact_id,sub_type='links',sub_type_id=link['LINK_ID'])
        # TODO: figure out contactlinks endpoint, not well documented
        i.delete('contacts', contact_id)
    countries = i.read('countries')
    currencies = i.read('currencies')
    custom_field_groups = i.read('customfieldgroups')
    custom_fields = i.read('customfields')
    if custom_fields is not None:
        custom_field_id = custom_fields[0]['CUSTOM_FIELD_ID']
        custom_field = i.read('customfields', custom_field_id)
    emails = i.read('emails')
    if emails is not None:
        email_id = emails[0]['EMAIL_ID']
        email = i.read('emails', email_id)
        i.create_child('emails', email_id, 'tags', {u'TAG_NAME':'foo'})
        i.delete('emails', email_id, sub_type='tags', sub_type_id = 'foo')
        comments = i.read('emails', email_id, sub_type='/comments')
    events = i.read('events')
    file_categories = i.read('filecategories')
    if file_categories is not None:
        file_category_id = file_categories[0]['CATEGORY_ID']
        file_category = i.read('filecategories', file_category_id)
    follows = i.read('follows')    
    instance = i.read('instance')
    leads = i.read('leads')
    if leads is not None:
        lead_id = leads[0]['LEAD_ID']
        lead = i.read('leads', lead_id)
    lead = i.create('leads', {u'FIRST_NAME':u'foo', u'LAST_NAME':u'bar'})
    if lead is not None:
        lead_id = lead['LEAD_ID']
        lead['FIRST_NAME']='foozle'
        lead = i.update('leads', lead)
        i.upload_image('leads', lead_id, 'apollo17.jpg')
        i.delete('leads', lead_id, sub_type='image')
        i.create_child('leads', lead_id, 'tags', {'TAG_NAME':'foo'})
        i.delete('leads', lead_id, sub_type='tags', sub_type_id='foo')
        i.create_child('leads', lead_id, 'follow', {})
        i.delete('leads', lead_id, sub_type='follow')
        notes = i.read('leads', lead_id, sub_type='notes')
        i.create_child('leads', lead_id, 'notes', {u'TITLE':u'foo',u'BODY':u'This is the body'})
        events = i.read('leads', lead_id, sub_type='events')
        file_attachments = i.read('leads', lead_id, sub_type='fileattachments')
        i.upload('leads', lead_id, 'apollo17.jpg')
        tasks = i.read('leads', lead_id, sub_type='tasks')
        emails = i.read('leads', lead_id, sub_type='emails')
        i.delete('leads', lead_id)
    leadsources = i.read('leadsources')
    lead_source = i.create('leadsources', {u'LEAD_SOURCE':u'Foozle Barzle'})
    if lead_source is not None:
        lead_source['LEAD_SOURCE'] = 'Barzle Foozle'
        lead_source_id = lead_source['LEAD_SOURCE_ID']
        lead_source = i.update('leadsources', lead_source)
        i.delete('leadsources', lead_source_id)
    lead_statuses = i.read('leadstatuses')
    lead_status = i.create('leadstatuses', {u'LEAD_STATUS':u'Foozle'})
    if lead_status is not None:
        lead_status_id = lead_status['LEAD_STATUS_ID']
        lead_status['LEAD_STATUS']='Barzle'
        lead_status['STATUS_TYPE']=1
        lead_status = i.update('leadstatuses', lead_status)
        i.delete('leadstatuses', lead_status_id)
    notes = i.read('notes')
    if notes is not None:
        note_id = notes[0]['NOTE_ID']
        note = i.read('notes', note_id)
        file_attachments = i.read('notes', note_id, sub_type='fileattachments')
        i.create_child('notes', note_id, 'follow', {})
        i.delete('notes', note_id, sub_type='follow')
        comments = i.read('notes', note_id, sub_type='comments')
    opportunities = i.read('opportunities')
    if opportunities is not None:
        opportunity_id = opportunities[0]['OPPORTUNITY_ID']
        opportunity = i.read('opportunities', opportunity_id)
        opportunity = i.create('opportunities', {u'OPPORTUNITY_NAME':u'Foozle',u'OPPORTUNITY_STATE':u'OPEN'})
        if opportunity is not None:
            opportunity['OPPORTUNITY_NAME'] = 'Barzle'
            opportunity_id = opportunity['OPPORTUNITY_ID']
            opportunity = i.update('opportunities', opportunity)
            i.upload_image('opportunities', opportunity_id, 'apollo17.jpg')
            i.delete('opportunities', opportunity_id, 'image')
            i.create_child('opportunities', opportunity_id, 'tags', {u'TAG_NAME':u'foo'})
            i.delete('opportunities', opportunity_id, sub_type='tags', sub_type_id='foo')
            notes = i.read('opportunities', opportunity_id, sub_type='notes')
            i.create_child('opportunities', opportunity_id, 'notes', {u'TITLE':'foo',u'BODY':'This is a test'})
            events = i.read('opportunities', opportunity_id, sub_type='events')
            file_attachments = i.read('opportunities', opportunity_id, sub_type='fileattachments')
            i.upload('opportunities', opportunity_id, 'apollo17.jpg')
            i.create_child('opportunities', opportunity_id, 'follow', {})
            i.delete('opportunities', opportunity_id, sub_type='follow')
            # add call to update opportunity state/state reason here
            opportunity_state_reasons = i.read('opportunities', opportunity_id, sub_type='statehistory')
            tasks = i.read('opportunities', opportunity_id, sub_type='tasks')
            emails = i.read('opportunities', opportunity_id, sub_type='emails')
            email = i.read('opportunities', opportunity_id, sub_type='linkemailaddress')
            i.delete('opportunities', opportunity_id, sub_type='pipeline')
            i.delete('opportunities', opportunity_id)
    opportunity_categories = i.read('opportunitycategories')
    opportunity_state_reasons = i.read('opportunitystatereasons')
    
    organisations = i.read('organisations')
    if organisations is not None:
        organisation_id = organisations[0]['ORGANISATION_ID']
        organisation = i.read('organisations', organisation_id)
        organisation = i.create('organisations', dummy_organisation)
        if organisation is not None:
            organisation_id = organisation['ORGANISATION_ID']
            organisation['ORGANISATION_NAME']='Bar Corporation'
            organisation = i.update('organisations', organisation)
            address = i.create_child('organisations', organisation_id, 'addresses', {u'CITY':u'San Francisco', u'STATE':u'CA', u'COUNTRY':u'United States', 'ADDRESS_TYPE':'Work'})
            if address is not None:
                address_id = address['ADDRESS_ID']
                i.delete('organisations', organisation_id, sub_type='addresses', sub_type_id=address_id)
            contactinfo = i.create_child('organisations', organisation_id, 'contactinfos', {u'TYPE':u'EMAIL',u'SUBTYPE':u'Home',u'DETAIL':u'foo@bar.com'})
            if contactinfo is not None:
                contact_info_id = contactinfo['CONTACT_INFO_ID']
                i.delete('organisations', organisation_id, sub_type='contactinfos', sub_type_id=contact_info_id)
            odate = i.create_child('organisations', organisation_id, 'dates', {u'OCCASION_NAME':u'Birthday','OCCASION_DATE':'2016-05-02T12:00:00Z'})
            if odate is not None:
                date_id = odate['DATE_ID']
                i.delete('organisations', organisation_id, sub_type='dates', sub_type_id=date_id)
            i.create_child('organisations', organisation_id, 'tags', {u'TAG_NAME':u'foo'})
            i.delete('organisations',organisation_id, sub_type='tags', sub_type_id='foo')
            i.upload_image('organisations', organisation_id, 'apollo17.jpg')
            i.delete('organisations', organisation_id, sub_type='image')
            notes = i.read('organisations', organisation_id, sub_type='notes')
            i.create_child('organisations', organisation_id, 'notes', {u'TITLE':'Title',u'BODY':'This is the body'})
            events = i.read('organisations', organisation_id, sub_type='events')
            file_attachments = i.read('organisations', organisation_id, sub_type='fileattachments')
            i.upload('organisations', organisation_id, 'apollo17.jpg')
            i.create_child('organisations', organisation_id, 'follow', {})
            i.delete('organisations', organisation_id, sub_type='follow')
            emails = i.read('organisations', organisation_id, sub_type='emails')
            tasks = i.read('organisations', organisation_id, sub_type='tasks')
            i.delete('organisations', organisation_id)
    
    pipelines = i.read('pipelines')
    if pipelines is not None:
        pipeline_id = pipelines[0]['PIPELINE_ID']
        pipeline = i.read('pipelines', pipeline_id)
        
    pipeline_stages = i.read('pipelinestages')
    if pipeline_stages is not None:
        stage_id = pipeline_stages[0]['STAGE_ID']
        pipeline_stage = i.read('pipelinestages', stage_id)
    else:
        stage_id = None
        pipeline_id = None
    
    projects = i.read('projects')
    if projects is not None:
        project_id = projects[0]['PROJECT_ID']
        project = i.read('projects', project_id)
        project = i.create('projects', {u'PROJECT_NAME':u'Foo Corporation',u'STATUS':u'Not Started'})
        if project is not None:
            project_id = project['PROJECT_ID']
            project['PROJECT_NAME']='Barzle Corporation'
            if stage_id is not None:
                project['PIPELINE_ID'] = pipeline_id
                project['STAGE_ID'] = stage_id
            project = i.update('projects', project)
            i.upload_image('projects', project_id, 'apollo17.jpg')
            i.delete('projects', project_id, sub_type='image')
            i.create_child('projects', project_id, 'tags', {'TAG_NAME':'foo'})
            i.delete('projects', project_id, sub_type='tags', sub_type_id='foo')
            notes = i.read('projects', project_id, sub_type='notes')
            i.create_child('projects', project_id, 'notes', {'TITLE':'Foo','BODY':'This is the body'})
            events = i.read('projects', project_id, sub_type='events')
            file_attachments = i.read('projects', project_id, sub_type='fileattachments')
            i.create_child('projects', project_id, 'follow', {})
            i.delete('projects', project_id, sub_type='follow')
            milestones = i.read('projects', project_id, sub_type='milestones')
            tasks = i.read('projects', project_id, sub_type='tasks')
            emails = i.read('projects', project_id, sub_type='emails')
            email = i.read('projects', project_id, sub_type='linkemailaddress')
            i.delete('projects', project_id, sub_type='pipeline')
            i.delete('projects', project_id)
    relationships = i.read('relationships')
    tags = i.read('tags?record_type=contacts')
    task_categories = i.read('taskcategories')
    tasks = i.read('tasks')
    if tasks is not None:
        task_id = tasks[0]['TASK_ID']
        task = i.read('tasks', task_id)
    users = i.read('users')
    if users is not None:
        user_id = users[0]['USER_ID']
        user = i.read('users', user_id)
    else:
        user_id = None
    me = i.read('users/me')
    if user_id is not None:
        task = i.create('tasks', {u'TITLE':u'こんにちは世界',u'STATUS':u'NOT STARTED',u'COMPLETED':False,u'PUBLICLY_VISIBLE':True,u'RESPONSIBLE_USER_ID':user_id})
        if task is not None:
            tasks = i.search('tasks','title=' + task['TITLE'])
            task['TITLE'] = task['TITLE'] + 'foo'
            task_id = task['TASK_ID']
            task = i.update('tasks', task)
            i.create_child('tasks', task_id, 'follow', {})
            i.delete('tasks', task_id, sub_type='follow')
            comments = i.read('tasks', task_id, sub_type='comments')
            i.delete('tasks', task_id)
    team_members = i.read('teammembers')
    if team_members is not None:
        team_member_id = team_members[0]['PERMISSION_ID']
        team_member = i.read('teammembers', team_member_id)
    
    teams = i.read('teams')
    if teams is not None:
        team_id = teams[0]['TEAM_ID']
        team = i.read('teams', team_id)
        team = i.create('teams',{u'TEAM_NAME':u'Team Foo',u'ANONYMOUS_TEAM':False})
        if team is not None:
            team_id = team['TEAM_ID']
            team['TEAM_NAME'] = 'Team Bar'
            team = i.update('teams', team)
            i.delete('teams', team_id)
            
    #
    # Next, create a few objects, add links between them, and then delete them
    #
    
    contact_id = None
    organisation_id = None
    project_id = None
    opportunity_id = None
    
    contact = i.create('contacts',{u'FIRST_NAME':u'Foo',u'LAST_NAME':u'Bar'})
    if contact is not None:
        contact_id = contact['CONTACT_ID']
    organisation = i.create('organisations',{u'ORGANISATION_NAME':u'Foo Corporation'})
    if organisation is not None:
        organisation_id = organisation['ORGANISATION_ID']
    project = i.create('projects',{u'PROJECT_NAME':u'Foo Corporation',u'STATUS':u'NOT STARTED'})
    if project is not None:
        project_id = project[u'PROJECT_ID']
    opportunity = i.create('opportunities',{u'OPPORTUNITY_NAME':u'Foo Corporation',u'OPPORTUNITY_STATE':u'OPEN'})
    if opportunity is not None:
        opportunity_id = opportunity['OPPORTUNITY_ID']
    
    contact = i.create_child('contacts', contact_id, 'links', {u'ORGANISATION_ID':organisation_id})
    organisation = i.create_child('organisations', organisation_id, 'links', {u'PROJECT_ID':project_id})
    project = i.create_child('projects', project_id, 'links', {u'ORGANISATION_ID':organisation_id})
    opportunity = i.create_child('opportunities', opportunity_id, 'links', {u'CONTACT_ID':contact_id})
    
    if contact_id is not None:
        i.delete('contacts', contact_id)
    if organisation_id is not None:
        i.delete('organisations', organisation_id)
    if project_id is not None:
        i.delete('projects', project_id)
    if opportunity_id is not None:
        i.delete('opportunities', opportunity_id)
            
    failures = list()
    
    print(str(i.tests_passed) + ' out of ' + str(i.tests_run) + ' passed')
    if len(i.test_failures) > 0:
        print ('')
        print ('Test Failures')
        for f in i.test_failures:
            print (f)
            failures.append(f)
            
    print(str(len(i.slow_endpoints)) + ' slow endpoints') 
    for s in i.slow_endpoints:
        print(s)
        
    return i.test_failures