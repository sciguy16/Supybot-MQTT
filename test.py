###
# Copyright (c) 2017, David Young
# All rights reserved.
#
#
###

from supybot.test import *


class MQTTTestCase(PluginTestCase):
    plugins = ('MQTT',)
    def testHello(self):
        self.assertNotError('hello')
