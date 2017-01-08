# What's popular at recurse center?

import datetime
import os
import pickle
import time


from github import Github, GithubException

from hackers import lst


# 1. How to handle rate limiting at different access points.
# 2. How to hide secrets: my passwords, hs usernames, data
# 3. How to handle lightweight persistency - don't want to set-up a database, but scraping takes a long time.
# 4. Other ways to quantify repo quality.


### Bugs

# 1. Possibly skipping people when it crashes, is stopped.
# 2. Dealing with people who have attended multiple batches
# 3. Incorrect github names.


g = Github('user', 'password')



def repos_for_user(username):
    l = []

    try:
        repos = [e for e in g.get_user(username).get_repos()]
    except GithubException as e:
        if g.rate_limiting[0] == 0:

            sleep_time = g.rate_limiting_resettime - time.time()
            print('sleeping ' + str(sleep_time))
            time.sleep(sleep_time)

            repos = [e for e in g.get_user(username).get_repos()]

        elif e.status in (404, ): # not found
            print(username)
            return []
        else:
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
            if g.rate_limiting[0] == 0:
                sleep_time = g.rate_limiting_resettime - time.time()
                print('sleeping ' + str(sleep_time))
                time.sleep(sleep_time)
                

            elif e.status in (409, 451, 403): # repository is empty, access is blocked, unavailable (problem on disk)
                continue
            else:
                import pdb; pdb.set_trace()
                x = 5
        except:
            continue

        try: 
            c1 = commits[0] # need to get the first commit, not the last.
        except GithubException as e:
            if g.rate_limiting[0] == 0:

                sleep_time = g.rate_limiting_resettime - time.time()
                print('sleeping ' + str(sleep_time))
                time.sleep(sleep_time)

                
                c1 = commits[0] # try again.

            else:
                raise e
            
            
        try:
            date_string = c1.raw_data['commit']['committer']['date']
        except GithubException as e:
            if g.rate_limiting[0] == 0:
                sleep_time = g.rate_limiting_resettime - time.time()
                print('sleeping ' + str(sleep_time))
                time.sleep(sleep_time)
                date_string = c1.raw_data['commit']['committer']['date']


        
        ds2 = date_string.split('T')[0]

        try:
            year, month, day = [int(e) for e in ds2.split('-')]
        except:
            import pdb; pdb.set_trace()

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

    if not os.path.exists('users.pickle'):
        s = set()
        f = open('users.pickle', 'wb')
        pickle.dump(s, f)
        f.close()
        


def save_user(username):
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

    
    


def started_at_rc(dt, batch_dates):
    for start, end in batch_dates:
        if dt < end and dt > start:
            return True
    return False


def collect_repos(lst):

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


def main():

    repos = collect_repos(lst)



if __name__ == "__main__":
    main()

