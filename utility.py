#!/usr/bin/env python
# original author: Ian
# original e-mail: stmayue@gmail.com
#___________________________________
# current author: Calum (AverageHomosapien)
# description: Utility functions for the prioritized experience replay


def list_to_dict(in_list):
    return dict((i, in_list[i]) for i in range(0, len(in_list)))


def exchange_key_value(in_dict):
    return dict((in_dict[i], i) for i in in_dict)


def main():
    pass


if __name__ == '__main__':
    main()
