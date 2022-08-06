import os

rep = os.popen(
    '''curl -X POST -d 'api_dev_key=3MYEHqc7-Or2hjNPhxJsW4vwsL_5yyxX' -d 'api_paste_code=test' -d 'api_option=paste' "https://pastebin.com/api/api_post.php"''')
ls = rep.read()
print(ls)