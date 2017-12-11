import ConfigParser
from trakt import Trakt
from tvshowtime import TVShowTime
from datetime import date

def update_history():
    # result = tvshow_manager.to_watch()
    # print result
    trakt_manager = Trakt()
    tvshow_manager = TVShowTime()
    
    print 'Fetching Trakt.tv watched history...'
    history = trakt_manager.get_history()

    checkin_list = []
    list_shows = {}
    for ep in history:

        show = {
            "show_id": ep['show']['ids']['tvdb'],
            "season": ep['episode']['season'],
            "episode": ep['episode']['number']
        }

        # filter by greater ep and season
        filter_list = filter(lambda x: x['season'] >= show['season'] and x['show_id'] == show['show_id'] and x['episode'] > show['episode'], checkin_list)
        if len(filter_list) == 0:
            checkin_list.append(show)

    print 'Saving progress on TVShowTime'
    print tvshow_manager.save_progress(checkin_list)

def collect_new_followed():
    print 'Collection new followed series to trakt.tv'
    trakt_manager = Trakt()
    tvshow_manager = TVShowTime()

    result = tvshow_manager.to_watch()

    watchlist = []
    for s in result['episodes']:

        print 'Processing ' + s['show']['name'] + '...'
        show = {
            "title": s['show']['name'],
            "ids": {
                "tvdb": s['show']['id']
            }
        }
    
        if s['season_number'] == 1 and s['number'] == 1:
            watchlist.append(show)
    
    obj = { "shows": watchlist }
    trakt_manager.add_to_watchlist(obj)
    print 'Collected'

def handler(event,context):
    parser = ConfigParser.ConfigParser()
    parser.read('config.ini')

    trakt_manager = Trakt()
    
    if not trakt_manager.is_token_valid():
        print 'Your access has been revoked or invalidated, please authenticate again.'
    else:
        update_history()
        collect_new_followed()


if __name__ == '__main__':
    # handler()

    parser = ConfigParser.ConfigParser()
    parser.read('config.ini')

    trakt_manager = Trakt()
    
    if not trakt_manager.is_token_valid():
        print 'Your access has been revoked or invalidated, please authenticate again.'
    else:
        update_history()
        collect_new_followed()

    
    