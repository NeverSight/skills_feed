---
name: jenkins
description: Interact with the Jenkins CI to get build and test job results
---

# Commands you can use to interact with Jenkins

```
# Fetch the Jenkins job results
jenkins_build_data.py <Jenkins job URL> --include=stages

# You can download test results and console output:
jenkins_build_data.py <Jenkins stage job URL> --include=console,tests

# In case the truncated console log does not provide enough information, download the full log
jenkins_build_data.py <Jenkins stage job URL> --include=full-console

# Usage:
# jenkins_build_data.py [-h] [--include INCLUDE] [--download SPEC] [--download-dir DOWNLOAD_DIR] [--json] [-q] url
#
# INCLUDE can be: console,tests,artifacts,stages,full-console
```

# In case the commands jenkins_build_data.py is missing

Ask the user to clone the zeug_cmk git repository and add it to their PATH.
See also: https://wiki.lan.checkmk.net/x/4zBSCQ
