#!/usr/bin/python3
# coding: utf-8

class Parent(object):

    def hi(self):
        print('Parent hi')

    # 抽象方法
    def print(self):
        raise Exception('子类必须实现此方法')


class Child(Parent):

    def hi(self):
        print('Child hi')

    def print(self):
        print('child print')



if __name__ == '__main__':
    c1 = Child()
    c1.print()
