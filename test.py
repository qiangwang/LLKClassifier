# -*- coding:utf-8 -*-

import jieba

from llk import LLKClassifier

#初始化，tokenizer需要有cut和add_word两个方法
llk = LLKClassifier(u'二手', tokenizer=jieba)

#添加过滤器
llk.add_badword(u'送.+')

#添加关键词
llk.add_keyword(u'苹果', u'手机', 'n')
llk.add_keyword(u'手机', u'手机', 'n')
llk.add_keyword(u'手机壳', u'手机配件', 'b')
llk.add_keyword(u'苹果', u'笔记本', 'a')
llk.add_keyword(u'mac', u'笔记本', 'n')
llk.add_keyword(u'苹果', u'农产品', 'n')
llk.add_keyword(u'办公', u'办公家具', 'b')
llk.add_keyword(u'家具', u'办公家具', 'n')
llk.add_keyword(u'办公', u'办公用品', 'b')
llk.add_keyword(u'打印机', u'办公用品', 'n')

#分类测试
assert llk.classify(u'苹果').keys() == [u'手机', u'农产品']
assert llk.classify(u'苹果手机') == u'手机'
assert llk.classify(u'苹果手机壳') == u'手机配件'
assert llk.classify(u'苹果手机送手机壳') == u'手机'
assert llk.classify(u'苹果mac') == u'笔记本'
assert llk.classify(u'办公打印机') == u'办公用品'
