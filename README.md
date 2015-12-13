# pythonista-tradervue
Routines to interact with [Tradervue](https://www.tradervue.com) from [Pythonista](http://omz-software.com/pythonista).

## Overview
The script here takes a number of arguments to direct how it should behave (see below table). Some actions may support additional args and those are documented in the action's specific documentation. 

This script uses the iOS keychain to store Tradervue credentials. While **not** available to other iOS applications. They **are** available to other Pythonista scripts. You can add multiple sets of credentials.

### URL Args
|arg|Default|Description|
|---|-------|-----------|
|action | set\_password | Specifies the action to take. Valid actions are: `set_password`, `delete_password`, `new_note`, `update_journal`.|
|user | (none) | The Tradervue username to use. When not specified, the user is prompted to enter this.|
|text | (clipboard contents) | The text to append to the journal entry|

## Actions
#### `set_password`
This action creates (or udpates an existing) Tradervue username/password combination in the keychain. The `text` argument is ignored. 

#### `delete_password`
This action deletes the credentials for the specified username. The `text` argument is ignored. 

#### `new_note`
This action creates a new Tradervue [note](http://blog.tradervue.com/2014/05/01/saving-notes/). 

#### `update_journal`
This action updates a Tradervue journal entry, creating it if necessary.

##### URL Args
|arg|Default|Description|
|---|-------|-----------|
|date | (today) | The date of the journal to modify in YYYYMMDD format. |
|overwrite | 0 | Set to 1 if the contents should overwrite the existing entry or 0 if they should be appended.|

## Setup
This is useless without Pythonista, so the first thing to do is to [go get that](https://itunes.apple.com/us/app/pythonista/id528579881?mt=8).

### Bootstrapping the installer
Now you have to get the files into Pythonista, which is a bit cumbersome. Here are some hopefully simple steps:

   * In the Pythonista file browser, create a new Empty Script
   * Paste the code below into that script and run it.

```
  import requests as r; o=open('tradervue_install.py','w'); o.write(r.get('http://bit.ly/1QlZmsJ').text); o.close()
```

### Installing pythonista-tradervue
After running the bootstrapping script above, you should have a file in your file browser named `tradervue_installer.py`. Run that script to install the utility.

After running the script, a top-level `tradervue` directory should have been created in your Pythonista file browser. Inside that directory are the following files:

   * README.md: This file
   * utils.py: The actual script you care about
   * tradervue: A directory containing the [Python Tradervue API](https://github.com/nall/py-tradervue-api)

If this all looks good, you can remove the `tradervue_install.py` script. 

### Setting up a Tradervue user
You can setup multiple Tradervue users, but it makes sense to at least have one. The credentials are stored in the iOS keychain and while other apps cannot access the credentials, not that other Pythonista scripts **can** access them. To store a set of credentials, run the `tradervue/utils.py` script. Its default action is `set_password`.

## Sample URLs

### Setting a password:
You don't have to specify a user (you'll be prompted):

    pythonista://tradervue/utils?action=run&argv=action%3Dset_password

Or you can specify a user like USERNAME:

    pythonista://tradervue/utils?action=run&argv=action%3Dset_password&argv=user%3DUSERNAME

### Deleting a password
You don't have to specify a user (you'll be prompted):

    pythonista://tradervue/utils?action=run&argv=action%3Ddelete_password

Or you can specify a user like USERNAME:

    pythonista://tradervue/utils?action=run&argv=action%3Ddelete_password&argv=user%3DUSERNAME

### Creating a new note
This assumes you've setup the credentials for USERNAME.

This will create a new note from the clipboard:
    pythonista://tradervue/utils?action=run&argv=action%3Dnew_note&argv=user%3DUSERNAME

This will create a new note from TEXT (which must be [URI encoded](http://www.w3schools.com/tags/ref_urlencode.asp))

    pythonista://tradervue/utils?action=run&argv=action%3Dnew_note&argv=user%3DUSERNAME&argv=text%3DTEXT

### Updating a journal entry
This assumes you've setup the credentials for USERNAME.

Append the clipboard to today's journal entry

    pythonista://tradervue/utils?action=run&argv=action%3Dupdate_journal&argv=user%3DUSERNAME

Overwrite today's journal entry with the clipboard

    pythonista://tradervue/utils?action=run&argv=action%3Dupdate_journal&argv=user%3DUSERNAME&argv=overwrite%3D1

Append the clipboard to the journal entry on Mar 8, 2013

    pythonista://tradervue/utils?action=run&argv=action%3Dupdate_journal&argv=user%3DUSERNAME&argv=date%3D20130308


