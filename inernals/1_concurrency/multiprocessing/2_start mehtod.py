# To select a start method you use the set_start_method() but it can be used once in a program
import multiprocessing as mp

def foo(q):
    q.put('hello')

if __name__ == '__main__':
    mp.set_start_method('spawn')
    q = mp.Queue()
    p = mp.Process(target=foo, args=(q,))
    p.start()
    print(q.get())
    p.join()



# or alternatively we can use get_context
import multiprocessing as mp

def foo(q):
    q.put('hello')

if __name__ == '__main__':
    ctx = mp.get_context('spawn')
    q = ctx.Queue()
    p = ctx.Process(target=foo, args=(q,))
    p.start()
    print(q.get())
    p.join()


# Note that objects related to one context may not be compatible with processes for a different context. In particular, locks created using the fork context cannot be passed to processes started using the spawn or forkserver start methods.

