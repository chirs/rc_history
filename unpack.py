import pickle

def top_repos(lst, key, count):
    lx = sorted(lst, key=lambda d: -d[key])[:count]


    print(key)
    print()
    for item in lx:
        print(str(item[key]) + " " + item['full_name'])
    print()

def load_repos():
    print('pickling')
    f = open('repos.pickle', 'rb')
    l = pickle.load(f)
    f.close()
    return l


def main():

    #repos = collect_repos(lst0)

    print()

    repos = load_repos()

    top_repos(repos, 'stars', 50)
    top_repos(repos, 'forks', 50)
    #import pdb; pdb.set_trace()
    #x = 5



if __name__ == "__main__":
    main()
