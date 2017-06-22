#!/usr/bin/python
# -*- coding: utf-8 -*-

import utils
from xbmc import translatePath

# Exhaustive list of constants as used by the addon's settings
service_enabled = u"service_enabled"
delete_folders = u"delete_folders"
ignore_extensions = u"ignore_extensions"
instant_enabled = u"instant_enabled"

clean_related = u"clean_related"
delayed_start = u"delayed_start"
scan_interval = u"scan_interval"

notifications_enabled = u"notifications_enabled"
notify_when_idle = u"notify_when_idle"
debugging_enabled = u"debugging_enabled"

default_action = u"default_action"
cleaning_type = u"cleaning_type"
clean_kodi_library = u"clean_kodi_library"
clean_movies = u"clean_movies"
clean_tv_shows = u"clean_tv_shows"
clean_music_videos = u"clean_music_videos"
clean_when_idle = u"clean_when_idle"

enable_expiration = u"enable_expiration"
expire_after = u"expire_after"

clean_when_low_rated = u"clean_when_low_rated"
minimum_rating = u"minimum_rating"
ignore_no_rating = u"ignore_no_rating"

clean_when_low_disk_space = u"clean_when_low_disk_space"
disk_space_threshold = u"disk_space_threshold"
disk_space_check_path = u"disk_space_check_path"

holding_folder = u"holding_folder"
create_subdirs = u"create_subdirs"

not_in_progress = u"not_in_progress"

keep_hard_linked = u"keep_hard_linked"

exclusion_enabled = u"exclusion_enabled"
exclusion1 = u"exclusion1"
exclusion2 = u"exclusion2"
exclusion3 = u"exclusion3"
exclusion4 = u"exclusion4"
exclusion5 = u"exclusion5"
             
movies_indiv_settings = "movies_indiv_settings"
movies_cleaning_type = "movies_cleaning_type"
movies_holding_folder = "movies_holding_folder"
movies_enable_expiration = "movies_enable_expiration"
movies_expire_after = "movies_expire_after"

movies_clean_when_low_rated = "movies_clean_when_low_rated"
movies_minimum_rating = "movies_minimum_rating"
movies_ignore_no_rating = "movies_ignore_no_rating"

movies_not_in_progress = "movies_not_in_progress"

movies_keep_hard_linked = "movies_keep_hard_linked"

episodes_indiv_settings = "episodes_indiv_settings"
episodes_cleaning_type = "episodes_cleaning_type"
episodes_holding_folder = "episodes_holding_folder"
episodes_enable_expiration = "episodes_enable_expiration"
episodes_expire_after = "episodes_expire_after"

episodes_clean_when_low_rated = "episodes_clean_when_low_rated"
episodes_minimum_rating = "episodes_minimum_rating"
episodes_ignore_no_rating = "episodes_ignore_no_rating"

episodes_not_in_progress = "episodes_not_in_progress"

episodes_keep_hard_linked = "episodes_keep_hard_linked"

musicvideos_indiv_settings = "musicvideos_indiv_settings"
musicvideos_cleaning_type = "musicvideos_cleaning_type"
musicvideos_holding_folder = "musicvideos_holding_folder"
musicvideos_enable_expiration = "musicvideos_enable_expiration"
musicvideos_expire_after = "musicvideos_expire_after"

musicvideos_keep_hard_linked = "musicvideos_keep_hard_linked"

bools = [service_enabled, delete_folders, clean_related, notifications_enabled, notify_when_idle, debugging_enabled,
         clean_kodi_library, clean_movies, clean_tv_shows, clean_music_videos, clean_when_idle, enable_expiration,
         clean_when_low_rated, ignore_no_rating, clean_when_low_disk_space,
         not_in_progress, keep_hard_linked, exclusion_enabled]
strings = [ignore_extensions, cleaning_type, default_action]
numbers = [delayed_start, scan_interval, expire_after, minimum_rating, disk_space_threshold]
paths = [disk_space_check_path, holding_folder, exclusion1, exclusion2, exclusion3, exclusion4,
         exclusion5]
individualParam = [ movies_enable_expiration, movies_expire_after, movies_clean_when_low_rated, movies_minimum_rating, movies_ignore_no_rating,
                    movies_not_in_progress, movies_keep_hard_linked, movies_cleaning_type, movies_holding_folder,
                    episodes_indiv_settings, episodes_enable_expiration, episodes_expire_after, episodes_clean_when_low_rated, episodes_minimum_rating, 
                    episodes_ignore_no_rating, episodes_not_in_progress, episodes_keep_hard_linked,episodes_cleaning_type, episodes_holding_folder,
                    musicvideos_indiv_settings, musicvideos_enable_expiration, musicvideos_expire_after,musicvideos_keep_hard_linked,
                    musicvideos_cleaning_type, musicvideos_holding_folder]
         
def get_setting(setting,video_type = "all"):
    """
    Get the value for a specified setting.

    Note: Make sure to check the return type of the setting you get.

    :param setting: The setting you want to retrieve the value of.
    :return: The value corresponding to the provided setting. This can be a float, a bool, a string or None.
    """
    settingSave = setting
    if video_type != "all":
        setting = video_type + "_" + setting
        if not(setting in individualParam) or utils.ADDON.getSetting(video_type + "_indiv_settings") != "true":
            setting = settingSave
    if settingSave in bools:
        return bool(utils.ADDON.getSetting(setting) == u"true")
    elif settingSave in numbers:
        return float(utils.ADDON.getSetting(setting))
    elif settingSave in strings:
        return unicode(utils.ADDON.getSetting(setting), encoding="utf-8")
    elif settingSave in paths:
        return unicode(translatePath(utils.ADDON.getSetting(setting).decode("utf-8")), encoding="utf-8")
    else:
        raise ValueError(u"Failed loading {0} value. Type {1} cannot be handled."
                         .format(setting, unicode(type(setting), encoding="utf-8")))


def load_all():
    """
    Get the values for all settings.

    Note: Make sure to check the return type of settings you get.

    :rtype: dict
    :return: All settings and their current values.
    """
    settings = dict()
    for s in bools + strings + numbers + paths:
        settings[s] = get_setting(s)
    return settings

    