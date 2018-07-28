## Multiple Configurations Organized In Scopes

``` ini
[journal]
editor = nano
basepath = ~/journals
filename = %Y/%m/%d/%NAME.md
template = ## %A, %d.%m.%Y (KW %W) 

[notes]
editor = nano
basepath = ~/notes
filename = %NAME.md
template = ## %NAME
```


## Install Dependencies

`$ sudo pip install -r requirements.txt`


## Make An Executable For Each Scope 

`$ ln -s /opt/notes/main.py ~/bin/notes`\
`$ ln -s /opt/notes/main.py ~/bin/journal`
    

## Edit Notes

`$ notes idm`
- scope: from appname
- name: idm
- date: defaults to today

`$ notes`
- scope: defaults to appname (notes)
- name: defaults to scope (notes)
- date: defaults to today

`$ notes mynotes idm`
- scope: mynotes
- name: idm
- date: defaults to today

`$ notes mynotes idm +1`
- scope: mynotes
- name: idm
- date: tomorrow

`$ notes mynotes idm -1w`
- scope: mynotes
- name: idm
- date: 1 week before

`$ notes mynotes idm +1y -1d`
- scope: mynotes
- name: idm
- date: yesterday in a year


## Search In Notes

`$ notes --find lel`
- search in 'notes' basedir for lel

`$ notes --find-all lel`
- search in every beasedir for lel
