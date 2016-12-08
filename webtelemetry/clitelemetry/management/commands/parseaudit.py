from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from clitelemetry.models import Session
from clitelemetry.models import Event
from subprocess import Popen
from subprocess import PIPE
import re
import datetime
import pytz


class Command(BaseCommand):
    help = 'Parses the audit log specified.'

    def add_arguments(self, parser):
        parser.add_argument('logfile', type=str)

    def handle(self, *args, **options):
        logfile = options['logfile']

        # un logfile through ausearch for interpretation
        p = Popen(['ausearch','-if',logfile,'-i'],stdout=PIPE,stderr=PIPE)
        out, err = p.communicate()
        lines = out.split('\n')

        # Aggregate event entries into a single dict
        evt_pattern = r"type=(\w+) msg=audit\((.+):([0-9]+)\) : (.*)"
        events = {}
        for l in lines:
            mgrp = re.match(evt_pattern,l.strip())

            if not mgrp:
                continue

            evt_type = mgrp.group(1)
            evt_date = mgrp.group(2)
            evt_id = mgrp.group(3)

            evt_date = datetime.datetime.strptime(evt_date,'%m/%d/%Y %H:%M:%S.%f')
            evt_date = pytz.timezone(settings.TIME_ZONE).localize(evt_date)

            if evt_id not in events:
                events[evt_id] = {
                    'date': evt_date
                }

            evt = events[evt_id]
            evt[evt_type] = {}
            evt_cmp = evt[evt_type]
            evt_data = mgrp.group(4)

            if evt_type == 'PROCTITLE':
                k, v = evt_data.split('=', 1)
                evt_cmp[k] = v
            else:
                for d in evt_data.split():
                    try:
                        k, v = d.split('=', 1)
                        evt_cmp[k] = v
                    except:
                        pass

        # Add parsed events to db
        for evt_id, data in events.iteritems():
            # Create/update Session
            if ('USER_START' in data.keys()):
                evt_cmp = data['USER_START']
                term_cmps = evt_cmp['terminal'].split('/')
                terminal = ''.join(term_cmps[-2:])
                session_dict = {
                    'user': evt_cmp['uid'],
                    'host': evt_cmp['hostname'],
                    'terminal': terminal
                }

                sessions = Session.objects.filter(**session_dict).order_by('-start')

                session_dict['start'] = data['date']
                if sessions.count() == 0:
                    session = Session.objects.create(**session_dict)
                elif sessions[0].end:
                    session = Session.objects.create(**session_dict)
                continue

            elif ('USER_END' in data.keys()):
                evt_cmp = data['USER_END']
                term_cmps = evt_cmp['terminal'].split('/')
                terminal = ''.join(term_cmps[-2:])
                try:
                    session = Session.objects.filter(user=evt_cmp['uid'],terminal=terminal)[0]
                except IndexError:
                    continue
                session.end = data['date']
                session.save()
                continue

            # Not an event we're interested in
            if 'SYSCALL' not in data.keys():
                continue

            # Get Session if created
            try:
                session = Session.objects.filter(
                    start__lte=data['date'],
                    # end__gte=data['date'],
                    terminal=data['SYSCALL']['tty'],
                    user=data['SYSCALL']['uid']
                    ).order_by('-start')[0]
            except IndexError:
                continue

            event_dict = {
                'audit_id': evt_id,
                'session': session,
                'cwd': data['CWD']['cwd'],
                'time': data['date'],
                'cmd': data['PROCTITLE']['proctitle'],
                'exit': data['SYSCALL']['exit'],
                'success': data['SYSCALL'] == 'yes'
            }
            event, created = Event.objects.get_or_create(**event_dict)

        self.stdout.write(self.style.SUCCESS('Successfully parsed log at "%s"' % logfile))
