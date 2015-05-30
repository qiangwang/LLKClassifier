#连连看分类器

简单、快速、有效的文本分类器

##原理

先对文本分词，然后根据分词去找定义了此分词的类别，最后用连连看的方式消除这些分词，没有被消除掉的分词就决定了文本对应的类别。

##细节

**过滤器**

对文本预处理，事先清掉无用的会产生干扰的内容，格式为正则表达式。

**分词种类**

每个类别下定义一组关键分词，分为专属、属于和干扰

* 专属：一票决定分类, 用字母b表示
* 属于：和分类十分相关，用字母n表示
* 干扰：会干扰当前分类，用字母a表示

**连连看规则**

RULE1. 不同类别之间相同的b可互相抵消, 如果剩余b个数大于1则将剩余的b合并到n中继续下面的规则

RULE2. 如果本类别有n，则可用本类别的a消除其他类别的n

RULE3. 不同类别之间相同的n可互相抵消

RULE4. 最后剩余的b或n决定了分类
