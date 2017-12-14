from mgpy import MGBuilder, ActionBuilder, ThreadedScheduler



def get2() -> 'two':
    return 2


def get3() -> 'three':
    return 3


def get5() -> 'five':
    return 5


def get7() -> 'seven':
    return 7


def get18(two: 'two', three: 'three') -> 'eighteen':
    return two*three*three


def get20(two: 'two', five: 'five') -> 'twenty':
    return two*two*five


def get21(three: 'three', seven: 'seven') -> 'twentyone':
    return three*seven


def print_result(eighteen: 'eighteen', twenty: 'twenty', twentyone: 'twentyone'):
    print('Eighteen:%d' % eighteen)
    print('Twenty:%d' % twenty)
    print('Twentyone:%d' % twentyone)


def make_pn():
    return MGBuilder()\
        .add(ActionBuilder(get2).read_annotations().once().build())\
        .add(ActionBuilder(get3).read_annotations().once().build())\
        .add(ActionBuilder(get5).read_annotations().once().build())\
        .add(ActionBuilder(get7).read_annotations().once().build())\
        .add(ActionBuilder(get18).read_annotations().build())\
        .add(ActionBuilder(get20).read_annotations().build())\
        .add(ActionBuilder(get21).read_annotations().build())\
        .add(ActionBuilder(print_result).read_annotations().build())\
        .build()


def main():
    pn = make_pn()
    scheduler = ThreadedScheduler(pn, print_all_states_full=False)
    scheduler.run()
    scheduler.join()

    print('PN is dead')


if __name__ == '__main__':
    main()
