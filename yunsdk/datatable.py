#coding:utf-8
import texttable

def Table(colmun,datalist):
    '''
    格式化输出，用于数据展示，colmun定义表有几列,datalist传入数据列表
    '''
    table = texttable.Texttable()
    align = ['l','c']
    for i in range(colmun):
        if i < colmun-2:
            align.insert(i+1,'c')
    table.set_cols_align(align)
    table.add_rows(datalist)

    return table.draw()
