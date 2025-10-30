#!/usr/bin/env bash
# -------------------------------------------------------------------------
# CCC CODE support script
# -------------------------------------------------------------------------
# Website:       https://wordops.net
# GitHub:        https://github.com/WordOps/WordOps
# Copyright (c) 2024 - WordOps
# This script is licensed under M.I.T
# -------------------------------------------------------------------------
# curl -sL git.io/fjAp3 | sudo -E bash -
# -------------------------------------------------------------------------
# Version 3.21.0 - 2024-05-29
# -------------------------------------------------------------------------

if [ -f /var/log/ccw/ccc-code.log ]; then
    cd /var/log/ccw/ || exit 1
    sed -E 's/([a-zA-Z0-9.-]+\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/domain.anonymized/g' /var/log/ccw/ccc-code.log >/var/log/ccw/ccc-code-issue.log
    ccw_link=$(curl -sL --upload-file ccc-code-issue.log https://transfer.vtbox.net/ccc-code.txt)
    echo
    echo "Here the link to provide in your github issue : $ccw_link"
    echo
    cd || exit 1
fi

# Zuletzt bearbeitet: 2025-10-30
