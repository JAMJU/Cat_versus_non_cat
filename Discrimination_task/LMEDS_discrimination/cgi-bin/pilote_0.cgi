#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import experiment_runner
experiment_runner.runExperiment("test_french_english",
                                "pilote_french.txt",
                                "french.txt",
                                disableRefresh=False,
                                audioExtList=[".ogg", ".mp3",".wav"],
                                videoExtList=[".ogg", ".mp4"],
                                allowUtilityScripts=True,
                                allowUsersToRelogin=True,
                                individualSequences=True)
