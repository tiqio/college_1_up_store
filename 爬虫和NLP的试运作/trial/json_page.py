g_page_config = re.search(r'g_page_config = (.*?);\n', res.text)
# 可以将text视为特殊的无法打开的特殊的文件格式,无法用with open打开,自然也无法写入,但可以正则
# 可以认为txt与text只有写差异,text无法使用with open
page_config_json = json.loads(g_page_config.group(1))
page_items = page_config_json['modes']~

results = []
for each_item in page_items:
  dict1 = dict.fromkeys(('nid',~))
  dict1['nid'] = each_item['nid']
  ~
  results.append(dict1)