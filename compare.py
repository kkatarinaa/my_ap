#!/usr/bin/python3
import ast
import numpy as np
import argparse
import re


def lev_dist(s1, s2):
    arr = np.zeros((len(s1) + 1, len(s2) + 1), int)
    for i in range(len(s1) + 1):
        for j in range(len(s2) + 1):
            if i == 0 and j == 0:
                arr[i][j] = 0
            elif j == 0:
                arr[i][j] = i
            elif i == 0:
                arr[i][j] = j
            else:
                m = 1
                if s1[i - 1] == s2[j - 1]:
                    m = 0
                arr[i][j] = min(arr[i][j - 1] + 1, arr[i - 1]
                                [j] + 1, arr[i - 1][j - 1] + m)
    return arr[-1][-1]


class AntiPlagiat:
    class Transformer(ast.NodeTransformer):
        def visit_Name(self, node):
            new_node = node
            new_node.id = 'nm'
            return new_node

        def visit_arg(self, node):
            new_node = node
            new_node.arg = 'arg'
            return new_node

        def visit_Import(self, node):
            return None

    def __init__(self, file1, file2):
        self.Input(file1, file2)
        self.Normalize()
        self.Compare()

    def Input(self, file1, file2):
        '''accepting data from files'''
        with open(file1, 'r') as input1, open(file2, 'r') as input2:
            self.s1 = input1.read()
            self.s2 = input2.read()

    def Normalize(self):
        '''removing unnecessary'''
        normalized = []
        for s in (self.s1, self.s2):
            s = re.sub(r'"""[\s\S]*?"""', '', s)
            s = re.sub(r"'''[\s\S]*?'''", '', s)
            s = ast.unparse(AntiPlagiat.Transformer().visit(ast.parse(s)))
            normalized.append(s)
        self.s1, self.s2 = normalized

    def Compare(self):
        self.similarity = 1 - \
            lev_dist(self.s1, self.s2) / max(len(self.s1), len(self.s2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    args = parser.parse_args()
    with open(args.input, 'r') as fin, open(args.output, 'w') as fout:
        for line in fin:
            try:
                file1, file2 = line.split()
                fout.write(f'{AntiPlagiat(file1, file2).similarity}\n')
            except SyntaxError:
                fout.write('There is a syntax error\n')
            except FileNotFoundError:
                fout.write('File not found\n')
            except:
                fout.write('Something went wrong\n')

