import re

def strip_process(a):
    '''去除首尾空格, 首尾标点, 括号转换为全角'''

    verb = [',', '.', '!', '?', ';', '，', '。', '．', '！', '；', '？', '"', '*','-','/']

    a = a.strip()

    while len(a)>0 and a[0] in verb:
        a = a[1:]
    while len(a)>0 and a[len(a)-1] in verb:
        a = a[:len(a) - 1]

    a = a.replace('(', '（').replace(')','）').replace('））','）').replace('（（','（')\
        .replace('【【','（').replace('】】', '）').replace('【', '（').replace('】', '）')
    
    return a


def specs_process(x):
    '''产品名称中的规格处理, 统一单位为 kg, g, L, mL'''
    def rep(a, old, new):
        text = re.compile(r'\s*[0-9]*\.?[0-9]+\s*' + old)
        result = re.findall(text, a)
        if result:
            for i in result:
                if old in ['ml','Ml','ML','毫升','G','克', 'g']:
                    try:
                        x = eval(i.replace(old, ''))
                        if x >= 1000:
                            x = x/1000
                            if new == 'mL':
                                x = str(x)+'L'
                            elif new == 'g':
                                x = str(x)+'kg'
                            a = a.replace(i, x)
                            continue
                    except:
                        pass
                else:
                    try:
                        x = eval(i.replace(old, ''))
                        if x < 1:
                            x = x * 1000
                            if new == 'L':
                                x = str(x)+'mL'
                            elif new == 'kg':
                                x = str(x)+'g'
                            a = a.replace(i, x)
                            continue
                    except:
                        pass
                a = a.replace(i, i.replace(old, new).replace(' ',''))
        return a

    a = rep(x, '升', 'L')
    a = rep(a, 'l', 'L')  
    a = rep(a, 'ml', 'mL')  
    a = rep(a, 'Ml', 'mL')  
    a = rep(a, 'ML', 'mL')  
    a = rep(a, '毫升', 'mL') 
    a = rep(a, 'G', 'g')  
    a = rep(a, 'KG', 'kg')  
    a = rep(a, 'kG', 'kg')  
    a = rep(a, 'Kg', 'kg')  
    a = rep(a, '千克', 'kg')  
    a = rep(a, '公斤', 'kg')  
    # a = rep2(a, '斤', 'kg')  

    a = rep(a, '克', 'g')  
    a = rep(a, 'L', 'L')
    a = rep(a, 'mL', 'mL')
    a = rep(a, 'kg', 'kg')
    a = rep(a, 'g', 'g')

    a = rep(a, 'MM', 'mm')  
    a = rep(a, 'mM', 'mm')
    a = rep(a, 'Mm', 'mm')
    a = rep(a, 'cM', 'cm')
    a = rep(a, 'Cm', 'cm')
    a = rep(a, 'CM', 'cm')
    a = rep(a, 'M', 'm')

    a = re.sub(r'\s*[（(]\s*[Ww]\s*[)）]\s*', '（W）', a)
    return a


def specs_split(x):
    specs = ['kg', 'mg', 'g', 'mL', 'L', 'cm', 'mm', 'm', '英寸', '寸', '斤', '两', '公分']
    unit = ['包', '袋', '盒', '箱', '罐', '瓶', '件', '块', '个', '桶', '条', '听','两','管','只','份','筐']
    for i in specs:
        r = {}

        pattern = r'\s*（?\s*([0-9]*\.?[0-9一二三四五六七八九十]+\s*\w{0,2}\s*[-~±]\s*[0-9]*\.?[0-9一二三四五六七八九十]+\s*%s)\s*[/／\\]([包袋盒箱罐瓶件块个桶条听两管只份筐片粒头合])\s*）?\s*'%(i)
        result = re.findall(pattern, x)
        if not result:
            pattern = r'\s*（?/?\s*([0-9]*\.?[0-9一二三四五六七八九十]+\s*%s)\s*[\*Xx]\s*([0-9]+\s*[包袋盒箱罐瓶件块个桶条听两管只份筐片粒头合])\s*[/／\\]\s*([包袋盒箱罐瓶件块个桶条听两管只份筐片粒头合])\s*）?\s*'%(i)
            result = re.findall(pattern, x)
            if result and isinstance(result[0],tuple) and len(result[0]) == 3:
                r['amount'] = result[0][1]
                result[0] = (result[0][0],result[0][2])
        if not result:
            pattern = r'\s*（?\s*([0-9]*\.?[0-9一二三四五六七八九十]+\s*\w{0,2}\s*[-~±]\s*[0-9]*\.?[0-9一二三四五六七八九十]+\s*%s)\s*）?\s*[/／\\]?([包袋盒箱罐瓶件块个桶条听两管只份筐片粒头合])\s*'%(i)
            result = re.findall(pattern, x)
        if not result:
            pattern = r'\s*（?/?\s*([0-9]*\.?[0-9]+\s*[\*Xx]\s*[0-9]*\.?[0-9]+)\s*[\*Xx]\s*([0-9]*\.?[0-9]+\s*%s)\s*）?\s*'%(i)
            result = re.findall(pattern, x)
            if result and isinstance(result[0],tuple) and len(result[0]) == 2:
                r['amount'] = result[0][0]
                result[0] = (result[0][1],)
        if not result:
            pattern = r'\s*（?\s*([0-9]+)\s*[\*Xx]\s*([0-9]*\.?[0-9一二三四五六七八九十]+\s*%s)\s*[/／\\]\s*([包袋盒箱罐瓶件块个桶条听两管只份筐片粒头合])\s*）?\s*'%(i)
            result = re.findall(pattern, x)
            if result and isinstance(result[0],tuple) and len(result[0]) == 2:
                r['amount'] = result[0][0]
                result[0] = (result[0][1],result[0][2])
        if not result:
            pattern = r'\s*（?\s*([0-9]*\.?[0-9一二三四五六七八九十]+\s*\w{0,2}\s*[-~±]\s*[0-9]*\.?[0-9一二三四五六七八九十]+\s*%s)\s*）?\s*' %(i)
            result = re.findall(pattern, x)
        if not result:
            pattern = r'\s*（?\s*([0-9一二三四五六七八九十]+\s*[包袋盒箱罐瓶件块个桶条听两管只份筐片粒合]?)\s*[\*Xx]\s*([0-9]*\.?[0-9一二三四五六七八九十]+\s*%s)\s*）?\s*'%(i)
            result = re.findall(pattern, x)
            if result and isinstance(result[0],tuple) and len(result[0]) == 2:
                r['amount'] = result[0][0]
                result[0] = (result[0][1],)
        if not result:
            pattern = r'\s*（?\s*([0-9]*\.?[0-9一二三四五六七八九十]+\s*%s)\s*[\*Xx]\s*([0-9一二三四五六七八九十]+\s*[包袋盒箱罐瓶件块个桶条听两管只份筐片粒头合]?\s*)\s*）?\s*'%(i)
            result = re.findall(pattern, x)
            if result and isinstance(result[0],tuple) and len(result[0]) == 2:
                r['amount'] = result[0][1]
                result[0] = (result[0][0],)
        if not result:
            pattern = r'\s*（?\s*([0-9]*\.?[0-9一二三四五六七八九十]+\s*%s)[/／\\]?\s*([包袋盒箱罐瓶件块个桶条听两管只份筐片粒头合])\s*）?\s*'%(i)
            result = re.findall(pattern, x)
        if not result:
            pattern = r'\s*（?\s*(\s*[0-9]*\.?[0-9一二三四五六七八九十]+\s*%s)\s*）?\s*' %(i)
            result = re.findall(pattern, x)
        if result:
            if result[0]:
                r['name'] = strip_process(re.sub(pattern,'',x))
                if isinstance(result[0],tuple):
                    var1 = result[0][0].replace(' ','')
                    if len(result[0]) >1 and result[0][1]:
                        r['unit'] = result[0][1].replace(' ','')
                else:
                    var1 = result[0]
                if i in ['L', 'mL']:
                    r['volumn'] = var1
                elif i in ['g', 'kg', '斤', '两', 'mg']:
                    r['weight'] = var1
                elif i in ['cm', 'mm', 'm', '寸', '英寸', '公分']:
                    r['length'] = var1
                if 'amount' not in r:
                    pattern = r'\s*（?\s*(\s*[0-9一二三四五六七八九十]*\s*[xX\*]?\s*[0-9一二三四五六七八九十]*-?[0-9一二三四五六七八九十]+\s*[包袋盒箱罐瓶件块个桶条听两管只份筐片粒头合])\s*）?\s*'
                    result = re.findall(pattern,r['name'])
                    if result:
                        r['name'] = strip_process(re.sub(pattern,'',r['name']))
                        r['amount'] = result[0].replace(' ','')
                if 'unit' not in r:
                    pattern = r'\s*（\s*/?\s*([包袋盒箱罐瓶件块个桶条听两管只份筐片粒头合])\s*）\s*'
                    result = re.findall(pattern,r['name'])

                    if result:
                        r['name'] = strip_process(re.sub(pattern,'',r['name']))
                        r['unit'] = result[0].replace(' ', '')
                    else:
                        pattern = r'\s*/\s*([包袋盒箱罐瓶件块个桶条听两管只份筐片粒头合])\s*）?\s*'
                        result = re.findall(pattern,r['name'])

                        if result:
                            r['name'] = strip_process(re.sub(pattern,'',r['name']))
                            r['unit'] = result[0].replace(' ', '')
                return r

    pattern = r'\s*（?\s*([0-9]*\.?[0-9一二三四五六七八九十]+\s*[-~±]\s*[0-9]*\.?[0-9一二三四五六七八九十]+\s*[包袋盒箱罐瓶件块个桶条听两管只份筐片粒头合]?)\s*）?\s*'
    result = re.findall(pattern, x)
    if result and result[0]+'个月' not in x:
        r = {'name': strip_process(re.sub(pattern,'',x)), 'amount':result[0]}
        return r

    pattern = r'\s*（?\s*([0-9一二三四五六七八九十]+[个只支片头粒枚])\s*[/／\\]\s*([^）])\s*）?\s*'
    result = re.findall(pattern, x)
    if result:
        if result[0] and result[0][0]:
            r = {'name': strip_process(re.sub(pattern,'',x)), 'amount':result[0][0]}
            if result[0][1]:
                r['unit'] = result[0][1].replace(' ','')
            return r
    else:
        result = re.findall(r'\s*（?\s*[0-9一二三四五六七八九十]+\s*[个只件支片头粒枚]\s*装\s*）?\s*', x)
        if result:
            r = {'name': strip_process(x.replace(result[0], '')), 'amount':re.sub(r'\s*|装|）|（','',result[0])}
            return r
        else:
            pattern = r'\s*（?\s*([0-9一二三四五六七八九十]+\s*[个只支片头粒枚])\s*[^月]\s*）?\s*'
            result = re.findall(pattern, x)
            if result:
                if result[0]:
                    r = {'name': strip_process(re.sub(pattern,'',x)), 'amount':re.sub(r'\s','',result[0])}
                    return r
    return {}            

    
def remarks(x):
    patten = r'\s*（[^（）]*）\s*'
    result = re.findall(patten, x)
    if result:
        name = re.sub(patten,'',x)
        remarks = re.sub(r'\s*|（|）','',result[0])
        if name == '':
            name = result[0]
            remarks = ''

        return {'name':name, 'remark':remarks}
    else:
        patten = r'\s*（[^）]*\s*'
        result = re.findall(patten, x)
        if result:

            name = re.sub(patten,'',x)
            remarks = re.sub(r'\s*|（|）','',result[0])
            if name == '':
                name = x
                remarks = ''
            return {'name':name, 'remark':remarks}
        return {}




