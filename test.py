import trakt

def main():
    tmanager = trakt.Trakt()
    tmanager.auth()

if __name__ == '__main__':
    main()
