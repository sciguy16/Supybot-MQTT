###
# Copyright (c) 2017, David Young
# All rights reserved.
#
#
###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.ircmsgs as ircmsgs

import threading
import paho.mqtt.client as mqtt

try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('MQTT')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x

def dbg(irc,m):
 irc.queueMsg(ircmsgs.privmsg('sciguy16',m))

class MQTT(callbacks.Plugin):
    """listens to an mqtt stream and dumps messages into the channel

hiiiiiiii"""
    threaded=True
    def __init__(self,irc):
        self.irc=irc
        self.__parent = super(MQTT,self)
        self.__parent.__init__(irc)
        dbg(self.irc,'make')
        self.t=threading.Thread(target=self.SocketWatch,args=())
        dbg(irc,'ya')
        self.t.start()
    
    def hello(self,irc,msg,args):
        """says hello"""
        irc.reply("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
        irc.queueMsg(ircmsgs.privmsg('#hello', 'yo'))
    hello=wrap(hello)

    def SocketWatch(self):
           cl=mqtt.Client()
           cl.on_connect=self.On_connect
           cl.on_message=self.On_message
           cl.connect("172.21.3.31",1883)
           cl.loop_start()
           self.cl=cl
    
    def On_connect(self,cl,userdata,flags,rc):
           dbg(self.irc,'Connected to MQTT broker')
           cl.subscribe("kazuki")

    def On_message(self,cl,userdata,msg):
#           dbg(self.irc,'pppyay')
#           dbg(self.irc,str(msg.payload)[2:-1])
        self.irc.queueMsg(ircmsgs.privmsg('#hello',str(msg.payload)[2:-1]))
    
    def die(self,cmd=False):
           self.log.debug("MQTT dying")
           self.cl.loop_stop()
           if not cmd:
               callbacks.Plugin.die(self)

Class = MQTT
