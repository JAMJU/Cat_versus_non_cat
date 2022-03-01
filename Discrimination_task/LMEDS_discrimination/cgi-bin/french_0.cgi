#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import experiment_runner
experiment_runner.runExperiment("test_french_english",
                                "sequence_french_0.txt",
                                "french.txt",
                                disableRefresh=False,
                                audioExtList=[".mp3",".wav"],
                                videoExtList=[".mp4"],
                                allowUtilityScripts=True,
                                allowUsersToRelogin=True,
                                individualSequences=True)

