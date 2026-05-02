Create a git commit message and save it to the file msg
The location of file msg should be inferred from the path
in prefix.txt

For example if the path in prefix.txt is
engineering/foundations/mechanics/statics/force-diagrams

Then the location of the file msg relative to where your current
directory (where codex is running) is
../../../../../msg

If prefix.txt is empty then the file msg should be created in
the current directory.

Use commit.template as the format of the commit message. If in doubt,
look at the format of the previous commit (or even the previous 2-3
commits,) to get an idea of how
to format the commit message.

Look in the file TODO.txt for features markeed with an asterisk. These are
the features being worked on for this commit. They should be placed under
the FEATURE(s) section of the commit message.

Use 'git status' to see which files have been staged for commit. DO NOT USE
'git status --short'.

These files should be listed in the FILES(s) sesction of the commit message.
For every file you add to this directory, you must prepend a prefix (if
it exists) to the the filename that refelects the location of the file in the repository.
The prefix path can be found in the file prefix.txt. 

The only execptions to this rule is TODO.txt. No prefix should be
added to that file.

For example if the prefix path in prefix.txt is:
engineering/foundations/mechanics/statics/force-diagrams
and git status shows two files staged for commit:

TODO.txt
src/forces/__init__.py

Then the FILE(s) section will contain the following entries:

TODO.txt
engineering/foundations/mechanics/statics/force-diagrams/src/forces/__init__.py


As another example, if the prefix file is empty, then the FILE() section
should conain the same output as status.txt. i.e:

TODO.txt
src/forces/__init__.py

Finally, look at the file related.txt for commit ids of commits that are
related to this commit. Use language similar to the language in those
commits when you create the commit message. Use plain language. Avoid
jargon. DO NOT exceed 70 characters per line. The only exceptions are for
the first line, and, long path names to files.

Note: You must ONLY document changes to files staged for commit. Nothing
else. If there are NO FILES staged for commite, then stop and print out
a message saying that there are no file staged for commit.
