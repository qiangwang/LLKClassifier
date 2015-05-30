# -*- coding:utf-8 -*-

import re

class Error(Exception):
    pass

class LLKClassifier:
    def __init__(self, category, tokenizer):
        self.category = category
        self.tokenizer = tokenizer

        self.keywords = {}
        self.badwords = {}

    def add_keyword(self, keyword, sub_category, keyword_type):
        keyword = self.normalize_word(keyword)
        if not keyword:
            raise Error('normalized keyword is empty')

        if not sub_category:
            raise Error('sub_category is empty')

        if keyword_type not in ('n', 'a', 'b'):
            raise Error('keyword_type is not in (n, a, b)')

        self.keywords.setdefault(keyword, {})
        self.keywords[keyword][sub_category] = keyword_type

        self.tokenizer.add_word(keyword)

        return True

    def del_keyword(self, keyword, sub_category):
        keyword = self.normalize_word(keyword)
        if keyword not in self.keywords:
            return False

        if sub_category not in self.keywords[keyword]:
            return False

        del self.keywords[keyword][sub_category]

        return True
        
    def add_badword(self, badword):
        badword = self.normalize_word(badword)
        if not badword:
            raise Error('normalized badword is empty')

        self.badwords[badword] = True

        return True

    def del_badword(self, badword):
        badword = self.normalize_word(badword)
        if badword not in self.badwords:
            return False

        del self.badwords[badword]

        return True

    def normalize_word(self, word):
        if isinstance(word, str):
            word = word.decode('utf-8')
        return word.lower().strip()
    
    def normalize_text(self, text):
        text = text.lower().strip()
        for badword in self.badwords:
            text = re.sub(badword, '', text)
        return text

    def tokenize(self, text):
        def rm_dup(seq):
            s = set()
            s_add = s.add
            return [x for x in seq if not (x in s or s_add(x))]

        tokens = list(self.tokenizer.cut(text))
        tokens = [self.normalize_word(t) for t in tokens]
        tokens = rm_dup(tokens)
        return tokens

    def classify(self, text, verbose=False):
        text = self.normalize_text(text)
        if verbose:
            print '[normalized] %s' % text

        tokens = self.tokenize(text)
        if verbose:
            print '[tokenized] %s' % tokens

        keywords = {}
        for token in tokens:
            if token in self.keywords:
                keywords[token] = self.keywords[token]

        table = self.llk(keywords, verbose)

        rows = len(table)
        if rows == 0:
            return None
        elif rows == 1:
            return table.keys()[0]
        else:
            return table
        
    def llk(self, keywords, verbose=False):
        #llk - init
        table = {}
        categories_has_b = []
        for k in keywords:
            for c, t in keywords[k].iteritems():
                table.setdefault(c, {'b': {}, 'n': {}, 'a': {}, 'has_n': False})
                table[c][t][k] = True
                if t == 'n':
                    table[c]['has_n'] = True
                elif t == 'b':
                    categories_has_b.append(c)
        if verbose:
            print '[inited] %s' % table

        #llk -ll - b
        if categories_has_b:
            if len(categories_has_b) == 1:
                return {categories_has_b[0]: table[categories_has_b[0]]}
            else:
                for c in categories_has_b:
                    table[c]['n'].update(table[c]['b'])

        #llk - ll - a
        for c, keywords in table.iteritems():
            if not keywords['has_n']:
                continue

            for a in keywords['a']:
                for c_2, keywords_2 in table.iteritems():
                    if c == c_2:
                        continue

                    del keywords_2['n'][a]

        #llk - ll - n
        for c, keywords in table.iteritems():
            for n in keywords['n'].copy():
                if len(keywords['n']) <= 1:
                    break

                for c_2, keywords_2 in table.iteritems():
                    if c == c_2:
                        continue
                    if n not in keywords_2['n']:
                        continue

                    del keywords['n'][n]
                    del keywords_2['n'][n]

        #llk - k
        for c, keywords in table.copy().iteritems():
            if not keywords['n']:
                del table[c]

        return table
