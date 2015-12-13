# vim: ft=python tabstop=2 shiftwidth=2 expandtab

# Copyright (c) 2015, Jon Nall
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of pythonista-tradervue nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import clipboard
import console
import keychain
import logging
import re
import sys
from datetime import datetime, date

sys.path.insert(0, os.path.realpath(os.join(os.getwd(), 'tradervue')))
from tradervue import Tradervue, TradervueLogFormatter

LOG = None
DEBUG = 0 # 1 for normal debug, 2 for HTTP debug as well
KEYCHAIN_ID = 'tradervue'
USER_AGENT = "Pythonista Tradervue (jon.nall@gmail.com)"

def get_args(argv):
  args = { 'action': 'set_password',
             'user': None,
             'text': clipboard.get(),
             'date': date.today().strftime('%Y%m%d'),
        'overwrite': "0" }
  for a in argv:
    pairs = a.split(':')
    for p in pairs:
      (k, v) = p.split('=', 2)
      if k not in args:
        raise ValueError("Invalid argument '%s'" % (k))
      args[k] = v

  if args['user'] is None:
    args['user'] = console.input_alert("Tradervue Username")
  if not re.match(r'^\d{8}$', args['date']):
    raise ValueError("Invalid date format '%s'. Must be YYYYMMDD" % (args['date']))

  if int(args['overwrite']) == 0:
    args['overwrite'] = False
  else:
    args['overwrite'] = True

  args['date'] = datetime.strptime(args['date'], '%Y%m%d')

  return args

def set_password(args):
  p = console.password_alert("Tradervue Credentials", args['user'])
  keychain.set_password(KEYCHAIN_ID, args['user'], p)
  return True

def delete_password(args):
  if keychain.get_password(KEYCHAIN_ID, args['user']) is None:
    LOG.error("No password was set for %s" % (args['user']))
    return False
  else:
    keychain.delete_password(KEYCHAIN_ID, args['user'])
    LOG.info("Deleted credentials for %s" % (args['user']))
    return True

def new_note(args, tv):
  note_id = tv.create_note(args['text'])
  if note_id is None:
    LOG.error("Failed to create new note")
    return False
  else:
    LOG.info("Created new note with ID %s" % (note_id))
    return True

def update_journal(args, tv):
  datestring = args['date'].strftime('%Y-%m-%d')

  # Check if we have an existing entry on the date. If not, just create it
  # Otherwise overwrite it if args['overwrite'] is set or append to it if not
  #
  journal = tv.get_journal(date = args['date'])
  if journal is None:
    journal_id = tv.create_journal(args['date'], args['text'])
    if journal_id is None:
      LOG.error("Failed to create journal on %s" % (datestring))
      return False
    else:
      LOG.info("Created new journal on %s with ID %s" % (datestring, journal_id))
      return True
  else:
    verb = 'Appended'
    text = journal['notes']
    if args['overwrite']:
      verb = 'Overwrite'
      text = ''
    text += "\n%s" % (args['text'])
    print text

    if tv.update_journal(journal['id'], text):
      LOG.info("%s journal on %s (ID %s)" % (verb, journal['id'], datestring))
      return True
    else:
      LOG.error("Failed to update journal on %s (ID %s)" % (datestring, journal['id']))
      return False

def main():
  global LOG
  LOG = logging.getLogger()
  LOG.setLevel(logging.INFO)
  if DEBUG > 1:
    LOG.setLevel(logging.DEBUG)
  c = logging.StreamHandler()
  c.setFormatter(TradervueLogFormatter())
  LOG.addHandler(c)

  args = get_args(sys.argv[1:])

  actions = { 'set_password': set_password,
           'delete_password': delete_password,
                  'new_note': new_note,
            'update_journal': update_journal }

  ok = False
  if args['action'] not in actions:
    raise ValueError("Invalid action '%s'" % (args['action']))
  elif args['action'].endswith('_password'):
    ok = actions[args['action']](args)
  else:
    p = keychain.get_password(KEYCHAIN_ID, args['user'])
    if p is None:
      # Request one from the user
      p = console.password_alert("Tradervue Credentials", args['user'])
    else:
      tv = Tradervue(args['user'], p, USER_AGENT, verbose_http = True if DEBUG > 1 else False)
      ok = actions[args['action']](args, tv)

  return 0 if ok else 1

if __name__ == "__main__":
  sys.exit(main())
