#!/usr/bin/python
# -*- coding: utf-8 -*-

from default import Cleaner
from settings import *
from utils import notify, debug


def autostart():
    """
    Starts the cleaning service.
    """
    cleaner = Cleaner()

    service_sleep = 4  # Lower than 4 causes too much stress on resource limited systems such as RPi
    ticker = 0
    delayed_completed = False

    while not cleaner.monitor.abortRequested():
        if get_setting(service_enabled):
            scan_interval_ticker = get_setting(scan_interval) * 60 / service_sleep
            delayed_start_ticker = get_setting(delayed_start) * 60 / service_sleep

            if delayed_completed and ticker >= scan_interval_ticker:
                results, _ = cleaner.clean_all()
                notify(results)
                ticker = 0
            elif not delayed_completed and ticker >= delayed_start_ticker:
                delayed_completed = True
                results, _ = cleaner.clean_all()
                notify(results)
                ticker = 0

            cleaner.monitor.waitForAbort(service_sleep)
            ticker += 1
        else:
            cleaner.monitor.waitForAbort(service_sleep)

    debug(u"Abort requested. Terminating.")
    return


    
class Main():
    def __init__( self ):
        debug(u"init main")
        self._service_setup()
        while not xbmc.abortRequested:
            xbmc.sleep(1000)

    def _service_setup( self ):
        debug(u"installing service")
        self.Player = MyPlayer(action = self._service_janitor)

    def _service_janitor( self, video_type, expired_videos ):
        debug(u"service janitor")
        # mark as watched
        debug(u"{0} to clean : {1} ({2})".format(video_type, expired_videos[u"title"], expired_videos[u"filename"]),xbmc.LOGNOTICE)
        try:
            cleaner = Cleaner()
            results, _ = cleaner.clean_all(video_type=video_type, expired_videos=expired_videos)
            # do janitor
            notify(results)
        except:
            debug(u"failed to do janitor on video {0} (filename= {1} )".format(expired_videos[u"filename"],expired_videos[u"title"]), xbmc.LOGNOTICE)
        
   
# monitor notifications
class MyPlayer(xbmc.Monitor):
    def __init__( self, *args, **kwargs ):
        debug(u"Player Class Init")
        xbmc.Monitor.__init__( self )
        self.action = kwargs[u"action"]
        
    def onNotification( self, sender, method, data ):
        if sender == u"xbmc":
            # Replace with next condition to enable clean after marked seen in library
            # if method == "Player.OnStop" or method == "VideoLibrary.OnUpdate":
            if method == u"Player.OnStop":
                
                debug(u"xbmc {0}".format(method))
                result = json.loads(data)
                if method == u"Player.OnStop" or ( method == u"VideoLibrary.OnUpdate" and "playcount" in result ):
                    # if viewing in file mode and playback stopped at the end
                    if "item" in result and "title" in result["item"] and result["end"]:
                        if result["item"]["type"] == "episode" or result["item"]["type"] == "movie" or result["item"]["type"] == "musicvideo":
                            # mark episode as watched
                            expired_videos = {"filename":result["item"]["file"],"title":result["item"]["title"]}
                            self.action(result["item"]["type"] + "s",expired_videos)
                    elif method == u"Player.OnStop":
                        # wait 1s before marking episode
                        xbmc.sleep(1000)

if __name__ == "__main__":
    debug(u"loading main service")
    if get_setting(instant_enabled):
        debug(u"service instant clean")
        Main()
    else:
        debug(u"run once")
        autostart()
