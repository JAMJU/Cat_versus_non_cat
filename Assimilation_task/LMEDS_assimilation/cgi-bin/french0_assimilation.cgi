#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import experiment_runner
experiment_runner.runExperiment("test_assimilation_french_english",
                                "assimilation_french.txt",
                                "french.txt",
                                disableRefresh=False,
                                audioExtList=[".ogg", ".mp3",".wav"],
                                videoExtList=[".ogg", ".mp4"],
                                allowUtilityScripts=True,
                                allowUsersToRelogin=True,
                                individualSequences=True)

