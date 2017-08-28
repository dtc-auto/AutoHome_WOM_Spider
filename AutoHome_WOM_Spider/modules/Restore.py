# coding:utf8
import re
import urllib
import urllib.parse
import requests


def get_char(js):
    all_var = {}
    # 判断混淆 无参数 返回常量 函数
    if_else_no_args_return_constant_function_functions = []
    """
    function zX_() {
            function _z() {
                return '09';
            };
            if (_z() == '09,') {
                return 'zX_';
            } else {
                return _z();
            }
        }
    """
    constant_function_regex4 = re.compile("""
        function\s+\w+\(\)\s*\{\s*
            function\s+\w+\(\)\s*\{\s*
                return\s+[\'\"][^\'\"]+[\'\"];\s*
            \};\s*
            if\s*\(\w+\(\)\s*==\s*[\'\"][^\'\"]+[\'\"]\)\s*\{\s*
                return\s*[\'\"][^\'\"]+[\'\"];\s*
            \}\s*else\s*\{\s*
                return\s*\w+\(\);\s*
            \}\s*
        \}
        """,
                                          re.X)
    l = constant_function_regex4.findall(js)
    # print("l 38",l)
    for i in l:
        function_name = re.search("""
        function\s+(\w+)\(\)\s*\{\s*
            function\s+\w+\(\)\s*\{\s*
                return\s+[\'\"]([^\'\"]+)[\'\"];\s*
            \};\s*
            if\s*\(\w+\(\)\s*==\s*[\'\"]([^\'\"]+)[\'\"]\)\s*\{\s*
                return\s*[\'\"]([^\'\"]+)[\'\"];\s*
            \}\s*else\s*\{\s*
                return\s*\w+\(\);\s*
            \}\s*
        \}
        """, i,
                                  re.X)
        if_else_no_args_return_constant_function_functions.append(function_name.groups())
        js = js.replace(i, "")
        # 替换全文
        a, b, c, d = function_name.groups()
        all_var["%s()" % a] = d if b == c else b

    # 判断混淆 无参数 返回函数 常量
    if_else_no_args_return_function_constant_functions = []
    """
    function wu_() {
            function _w() {
                return 'wu_';
            };
            if (_w() == 'wu__') {
                return _w();
            } else {
                return '5%';
            }
        }
    """
    constant_function_regex5 = re.compile("""
        function\s+\w+\(\)\s*\{\s*
            function\s+\w+\(\)\s*\{\s*
                return\s+[\'\"][^\'\"]+[\'\"];\s*
            \};\s*
            if\s*\(\w+\(\)\s*==\s*[\'\"][^\'\"]+[\'\"]\)\s*\{\s*
                return\s*\w+\(\);\s*
            \}\s*else\s*\{\s*
                return\s*[\'\"][^\'\"]+[\'\"];\s*
            \}\s*
        \}
        """,
                                          re.X)
    l = constant_function_regex5.findall(js)
    # print("l 87",l)
    for i in l:
        function_name = re.search("""
        function\s+(\w+)\(\)\s*\{\s*
            function\s+\w+\(\)\s*\{\s*
                return\s+[\'\"]([^\'\"]+)[\'\"];\s*
            \};\s*
            if\s*\(\w+\(\)\s*==\s*[\'\"]([^\'\"]+)[\'\"]\)\s*\{\s*
                return\s*\w+\(\);\s*
            \}\s*else\s*\{\s*
                return\s*[\'\"]([^\'\"]+)[\'\"];\s*
            \}\s*
        \}
        """, i,
                                  re.X)
        if_else_no_args_return_function_constant_functions.append(function_name.groups())
        js = js.replace(i, "")
        # 替换全文
        a, b, c, d = function_name.groups()
        all_var["%s()" % a] = b if b == c else d

    # var 参数等于返回值函数
    var_args_equal_value_functions = []
    """
    var ZA_ = function(ZA__) {
            'return ZA_';
            return ZA__;
        };
    """
    constant_function_regex1 = re.compile(
        "var\s+[^=]+=\s*function\(\w+\)\{\s*[\'\"]return\s*\w+\s*[\'\"];\s*return\s+\w+;\s*\};")
    l = constant_function_regex1.findall(js)
    # print("l 119",l)
    for i in l:
        function_name = re.search("var\s+([^=]+)", i).group(1)
        var_args_equal_value_functions.append(function_name)
        js = js.replace(i, "")
        # 替换全文
        a = function_name
        js = re.sub("%s\(([^\)]+)\)" % a, r"\1", js)

    # var 无参数 返回常量 函数
    var_no_args_return_constant_functions = []
    """
    var Qh_ = function() {
            'return Qh_';
            return ';';
        };
    """
    constant_function_regex2 = re.compile("""
            var\s+[^=]+=\s*function\(\)\{\s*
                [\'\"]return\s*\w+\s*[\'\"];\s*
                return\s+[\'\"][^\'\"]+[\'\"];\s*
                \};
            """,
                                          re.X)
    l = constant_function_regex2.findall(js)
    # print("l 144",l)
    for i in l:
        function_name = re.search("""
            var\s+([^=]+)=\s*function\(\)\{\s*
                [\'\"]return\s*\w+\s*[\'\"];\s*
                return\s+[\'\"]([^\'\"]+)[\'\"];\s*
                \};
            """,
                                  i,
                                  re.X)
        var_no_args_return_constant_functions.append(function_name.groups())
        js = js.replace(i, "")
        # 替换全文
        a, b = function_name.groups()
        all_var["%s()" % a] = b

    # 无参数 返回常量 函数
    no_args_return_constant_functions = []
    """
    function ZP_() {
            'return ZP_';
            return 'E';
        }
    """
    constant_function_regex3 = re.compile("""
            function\s*\w+\(\)\s*\{\s*
                [\'\"]return\s*[^\'\"]+[\'\"];\s*
                return\s*[\'\"][^\'\"]+[\'\"];\s*
            \}\s*
        """,
                                          re.X)
    l = constant_function_regex3.findall(js)
    # print("l 176",l)
    for i in l:
        function_name = re.search("""
            function\s*(\w+)\(\)\s*\{\s*
                [\'\"]return\s*[^\'\"]+[\'\"];\s*
                return\s*[\'\"]([^\'\"]+)[\'\"];\s*
            \}\s*
        """,
                                  i,
                                  re.X)
        no_args_return_constant_functions.append(function_name.groups())
        js = js.replace(i, "")
        # 替换全文
        a, b = function_name.groups()
        all_var["%s()" % a] = b

    # 无参数 返回常量 函数 中间无混淆代码
    no_args_return_constant_sample_functions = []
    """
    function do_() {
            return '';
        }
    """
    constant_function_regex3 = re.compile("""
            function\s*\w+\(\)\s*\{\s*
                return\s*[\'\"][^\'\"]*[\'\"];\s*
            \}\s*
        """,
                                          re.X)
    l = constant_function_regex3.findall(js)
    # print("l 206",l)
    for i in l:
        function_name = re.search("""
            function\s*(\w+)\(\)\s*\{\s*
                return\s*[\'\"]([^\'\"]*)[\'\"];\s*
            \}\s*
        """,
                                  i,
                                  re.X)
        no_args_return_constant_sample_functions.append(function_name.groups())
        js = js.replace(i, "")
        # 替换全文
        a, b = function_name.groups()
        all_var["%s()" % a] = b

    # 字符串拼接时使无参常量函数
    """
    (function() {
                'return sZ_';
                return '1'
            })()
    """
    constant_function_regex6 = re.compile("""
            \(function\(\)\s*\{\s*
                [\'\"]return[^\'\"]+[\'\"];\s*
                return\s*[\'\"][^\'\"]*[\'\"];?
            \}\)\(\)
        """,
                                          re.X)
    l = constant_function_regex6.findall(js)
    # print("l 236",l)
    for i in l:
        function_name = re.search("""
            \(function\(\)\s*\{\s*
                [\'\"]return[^\'\"]+[\'\"];\s*
                return\s*([\'\"][^\'\"]*[\'\"]);?
            \}\)\(\)
        """,
                                  i,
                                  re.X)
        js = js.replace(i, function_name.group(1))

    # 字符串拼接时使用返回参数的函数
    """
    (function(iU__) {
                'return iU_';
                return iU__;
            })('9F')
    """
    constant_function_regex6 = re.compile("""
            \(function\(\w+\)\s*\{\s*
                [\'\"]return[^\'\"]+[\'\"];\s*
                return\s*\w+;
            \}\)\([\'\"][^\'\"]*[\'\"]\)
        """,
                                          re.X)

    l = constant_function_regex6.findall(js)
    # print("l 264",l)
    for i in l:
        function_name = re.search("""
            \(function\(\w+\)\s*\{\s*
                [\'\"]return[^\'\"]+[\'\"];\s*
                return\s*\w+;
            \}\)\(([\'\"][^\'\"]*[\'\"])\)
        """,
                                  i,
                                  re.X)
        js = js.replace(i, function_name.group(1))
    print("275",js)
    # 获取所有变量
    var_regex = "var\s+(\w+)=(.*?);\s"
    var_find = re.findall(var_regex, js)
    print("var_find",var_find)
    for var_name, var_value in var_find:
        var_value = var_value.strip("\'\"").strip()
        # print(var_name,"---",var_value)
        if "(" in var_value:
            var_value = ";"
        all_var[var_name] = var_value
    print("all var",all_var)
    # 注释掉 此正则可能会把关键js语句删除掉
    # js = re.sub(var_regex, "", js)

    for var_name, var_value in all_var.items():
        js = js.replace(var_name, var_value)
    print("----282",js)
    js = re.sub("[\s+']", "", js)
    print("----284",js)
    string_m = re.search("(%\w\w(?:%\w\w)+)", js)
    # string = urllib.parse.unquote(string_m.group(1)).encode("utf-8").decode("utf8")
    print("string_m",string_m.groups())
    string = urllib.parse.unquote(string_m.group(1)).encode("utf-8").decode("utf8")
    print(string)
    index_m = re.search("([\d,]+(;[\d,]+)+)", js[string_m.end():])
    print(index_m.group())
    string_list = list(string)
    print("str",len(string_list))
    # print("string_list",string_list)
    index_list = index_m.group(1).split(";")
    # print("index_list",index_list)
    _word_list = []
    # print(type(_word_list))
    # print(_word_list)
    i = 1
    exflag = 0;
    # deal exception

    # print("--max ",type(int(max(index_list))))
    max_index=0;
    for word_index_list in index_list:
        _word = ""
        if "," in word_index_list:
            word_index_list = word_index_list.split(",")
            word_index_list = [int(x) for x in word_index_list]
        else:
            word_index_list = [int(word_index_list)]
        for word_index in word_index_list:
            # print(word_index)
            if(word_index>max_index):
                max_index=word_index
            try:
                string_list[word_index]
            except Exception as e:
                exflag=1;
    print(max_index)
    print("exflag",exflag)
    less = max_index - len(string_list)
    print(less)
    for word_index_list in index_list:
        _word = ""
        if "," in word_index_list:
            word_index_list = word_index_list.split(",")
            # print("word_index_list",word_index_list)
            word_index_list = [int(x) for x in word_index_list]
            # print("word_index_list", word_index_list)
        else:
            word_index_list = [int(word_index_list)]
        j = 1;
        for word_index in word_index_list:
            # print("for",j)
            j += 1
            # print("word_index",word_index)
            # print("string_list[word_index]",string_list[word_index])
            try:
                _word += string_list[word_index-1-less]
            except Exception as e:
                print(e)

        # print(_word)
        _word_list.append(_word)
        # print("----------")
        # print(i)
        # print(_word_list)

        i += 1

    return _word_list


def get_complete_text_autohome(text):
    #print("text0",text)
    text = text.replace(r"\u0027","'").replace(r"\u003e",">").replace(r"\u003c","<")
    #print("text1",text)
    js = re.search("<!--@HS_ZY@--><script>([\s\S]+)\(document\);</script>", text)
    #print("find : %s" % js.group())
    if not js:
        print("  if not js:")
        return text
    try:
        #print("try0")
        char_list = get_char(js.group(1))
        print("try111")

    except Exception as e:
        print(e)
        print("except222")
        return text

    def char_replace(m):
        index = int(m.group(1))
        char = char_list[index]  # 溢出
        return char

    text = re.sub("<span\s*class=[\'\"]hs_kw(\d+)_[^\'\"]+[\'\"]></span>", char_replace, text)
    # print(text)
    return text


# # resp = requests.get("http://k.autohome.com.cn/FrontAPI/GetFeelingByEvalId?evalId=1538569")
# resp = requests.get("http://k.autohome.com.cn/spec/29129/view_1567098_1.html?st=16&piap=0|2951|0|0|1|0|0|0|0|0|1")
# resp.encoding = "gbk"
# text = get_complete_text_autohome(resp.text)
#
#
# print(re.search("<!--@HS_BASE64@-->.*<!--@HS_ZY@-->", text).group())
# print("2")
