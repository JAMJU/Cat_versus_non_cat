#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import experiment_runner
experiment_runner.runExperiment("test_french_english",
                                "sequence_english_0.txt",
                                "english.txt",
                                disableRefresh=False,
                                audioExtList=[".mp3",".wav"],
                                videoExtList=[".mp4"],
                                allowUtilityScripts=True,
                                allowUsersToRelogin=True,
                                individualSequences=True)
