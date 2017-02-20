#!/usr/bin/env python3

# Unpack the pickle. 
# This is just a convenience script to print out the results.

import pickle

def top_repos(lst, key, count):
    """
    Make a list of top repos
    """

    lx = sorted(lst, key=lambda d: -d[key])[:count]

    print('\n{}\n'.format(key))
    for item in lx:
        print("{} {}".format(str(item[key]), item['full_name']))





def load_repos():
    """
    Load the repos
    """
    # Use with I guess. Who cares.
    f = open('repos.pickle', 'rb')
    l = pickle.load(f)
    f.close()
    return l


def main():


    repos = load_repos()

    format_repo = lambda repo: '{}:\t{}\n'.format(repo['full_name'], repo['description'])

    for repo in sorted(repos, key=lambda d: d['full_name']):
        description = repo['description'].lower()
        if 'contra' in description or 'dance' in description:
            print(format_repo(repo))
        
        '''
        if description and repo['stars'] > 3:
            if 'p' in description:
                print(
        '''
    

    #top_repos(repos, 'stars', 50)
    #top_repos(repos, 'forks', 50)





if __name__ == "__main__":
    main()
