---
title: Getting Started With Python Automation
date: 2024-01-15
---
# Getting Started With Python Automation

Automation doesn't have to be complicated. Some of the most useful scripts I've written are under 50 lines.

## Where to Start

Pick something annoying you do manually at least once a week. That's your first automation target. It doesn't have to be impressive — it just has to save you time.

## A Simple Example

Here's a script that renames all files in a folder to lowercase:

```python
from pathlib import Path

for f in Path(".").iterdir():
    if f.is_file():
        f.rename(f.parent / f.name.lower())
```

That's it. Eleven lines. Useful forever.

## What's Next

Once you're comfortable with files and folders, the next step is working with APIs — pulling data from the web and doing something with it.
