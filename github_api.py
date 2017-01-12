#!/usr/bin/env python3

# Scrape github for repositories that have been created by 
# users during a given time period.

import datetime
import os
import pickle
import time


from github import Github, GithubException

from hackers import lst


# 1. How to handle rate limiting at different access points; avoid disgusting anti-pattern.

# 2. How to hide secrets: my passwords, hs usernames, data
# 3. How to handle lightweight persistency - don't want to set-up a database, but scraping takes a long time.
# 4. Other ways to quantify repo quality.


### Bugs

# 1. Possibly skipping people when it crashes, is stopped.
# 2. Dealing with people who have attended multiple batches
# 3. Incorrect github names.



# The Github API stuff.
# This is 

githubAPI = Github('user', 'password')

def started_at_rc(dt, batch_dates):
    """
    Was this database started at Recurse Center?
    Check if the given date object fits between a pair of start/end dates. 
    """
    for start, end in batch_dates:
        if dt < end and dt > start:
            return True
    return False


def collect_repos(lst):
    """
    Collect all repos created during recurse center.
    """

    l = load_github()

    for username, batch_dates in lst:

        if not check_users(username):

            repos = repos_for_user(username)
            for repo in repos:
                if started_at_rc(repo['start_date'], batch_dates):
                    l.append(repo)

            save_github(l)

        save_user(username)
        
    return l



def check_rate_limit():
    if githubAPI.rate_limiting[0] == 0:
        sleep_time = githubAPI.rate_limiting_resettime - time.time()
        print('sleeping ' + str(sleep_time))
        time.sleep(sleep_time)
        return True
    else:
        return False


def repos_for_user(username):
    """
    Retrieve all repos for a user given...
    """
    # Oh my. So much rate limiting code here. 
    # Split this into separate items.

    l = []

    try:
        repos = [e for e in githubAPI.get_user(username).get_repos()]

    except GithubException as e:
        if check_rate_limit():
            repos = [e for e in githubAPI.get_user(username).get_repos()]

        elif e.status in (404, ): # repositories not found
            print(username)
            return []
        else:
            # Some other error. 
            import pdb; pdb.set_trace()
            x = 5

    except:
        print(username)
        return []

    for repo in repos:

        description = repo.description
        stars = repo.stargazers_count
        watchers = repo.watchers_count
        forks = repo.forks_count

        try:
            commits = repo.get_commits().reversed
        except GithubException as e:
            if check_rate_limit():
                commits = repo.get_commits().reversed
                
            elif e.status in (409, 451, 403): 
                # repository is empty (409), access is blocked (451), unavailable (problem on disk) (403)
                continue
            else:
                import pdb; pdb.set_trace()
                x = 5

        except:
            continue

        try: 
            c1 = commits[0]

        except GithubException as e:
            if check_rate_limit():
                c1 = commits[0]

            else:
                raise e
            
        try:
            date_string = c1.raw_data['commit']['committer']['date']
        except GithubException as e:
            if check_rate_limit():
                date_string = c1.raw_data['commit']['committer']['date']
        
        ds2 = date_string.split('T')[0]
        year, month, day = [int(e) for e in ds2.split('-')]
        dt = datetime.datetime(year, month, day)

        d = {
            'name': repo.name,
            'full_name': repo.full_name,
            'description': repo.description or '',
            'watchers': watchers,
            'stars': stars,
            'forks': forks,
            'start_date': dt,
            }

        l.append(d)

    return l


## Utility functions for pickling / unpickling various things.
## These exist because I don't want to have to set up a database.

def save_github(lst):
    print('pickling')
    f = open('repos.pickle', 'wb')
    pickle.dump(lst, f)
    f.close()


def load_github():
    try:
        f = open('repos.pickle', 'rb')
        l = pickle.load(f)
        return l
    except:
        return []


def check_empty_user():
    """
    Check that the users pickle exists.
    """

    if not os.path.exists('users.pickle'):
        s = set()
        f = open('users.pickle', 'wb')
        pickle.dump(s, f)
        f.close()
        


def save_user(username):
    """
    Save a username that has been searched.
    """
    check_empty_user()

    f = open('users.pickle', 'rb')
    s = pickle.load(f)
    s.add(username)

    f = open('users.pickle', 'wb')
    pickle.dump(s, f)
    f.close()


def check_users(username):

    check_empty_user()

    print('pickling')
    f = open('users.pickle', 'rb')
    s = pickle.load(f)
    return username in s


def main():
    """
    main function
    """

    repos = collect_repos(lst)



if __name__ == "__main__":
    main()

