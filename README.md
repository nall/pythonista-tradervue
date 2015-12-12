# pythonista-tradervue
Routines to interact with [Treadervue](https://www.tradervue.com) from [Pythonista](http://omz-software.com/pythonista).

## Overview
The script here takes a number of arguments to direct how it should behave (see below table). Some actions may support additional args and those are documented in the action's specific documentation. 

This script uses the iOS keychain to store Tradervue credentials. While **not** available to other iOS applications. They **are** available to other Pythonista scripts. You can add multiple sets of credentials.

### URL Args
|arg|Default|Description|
|---|-------|-----------|
|action | update\_passwd | Requests Tradervue credentials from the user and updates them in the iOS keychain. Valid actions are: `update_passwd`, `delete_passwd`, `new_note`, `update_journal`.|
|user | (none) | The Tradervue username to use. When not specified, the user is prompted to enter this.|
|text | (clipboard contents) | The text to append to the journal entry|

## Actions
### `update_passwd`
This action creates (or udpates an existing) Tradervue username/password combination in the keychain. The `text` argument is ignored. 

### `delete_passwd`
This action deletes the credentials for the specified username. The `text` argument is ignored. 

### `new_note`
This action creates a new Tradervue [note](http://blog.tradervue.com/2014/05/01/saving-notes/). 

### `update_journal`
This action creates a new Tradervue [note](http://blog.tradervue.com/2014/05/01/saving-notes/). 

#### URL Args
|arg|Default|Description|
|---|-------|-----------|
|date | (today) | The date of the journal to modify in YYYY-MM-DD format. |
|overwrite | false | True if the contents should overwrite the existing entry or false if they should be appended.|

