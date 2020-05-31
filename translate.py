from nonebot import on_command, CommandSession
import requests
from nonebot import on_natural_language, NLPSession, IntentCommand
import re



@on_command('translate',aliases=('翻译','查询'))
async def translate(session: CommandSession):
    # 从会话状态（session.state）中获取英语(words），如果当前不存在，则询问用户
    words = session.get('words',prompt='要姐给你翻译就好好给喔输!\n 例子 : 翻译 你是我奴隶')

    text = re.sub('翻译','',words) #将翻译替换为空，避免二次询问


    #获取翻译结果
    translate_report = await get_translate(text)

    # 向用户发送翻译结果
    await session.send(translate_report)




@translate.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：翻译 Love
            session.state['words'] = stripped_arg
        return

    if not stripped_arg:
        # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('翻译的内容不能为空!')

    # 如果当前正在向用户询问更多信息，且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg



async def get_translate(words: str) -> str:

    #爬取有道翻译
    data={}
    data['i']= words
    data['from']= 'en'
    data['to']= 'zh-CHS'
    data['smartresult']='dict'
    data['client'] = 'fanyideskweb'
    data['salt'] ='15827240014855'
    data['sign'] = '4739d8a5afb23d9bbfd0f011157181f9'
    data['ts']= '1582724001485'
    data['bv']='0ed2e07b89acaa1301d499442c9fdf79'
    data['doctype']='json'
    data['version']='2.1'
    data['keyfrom']='fanyi.web'
    data['action']=  'FY_BY_CLICKBUTTION'

    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'

    r = requests.post(url, data=data)
    target = r.json()
    text = target['translateResult'][0][0]['src']
    tran = target['translateResult'][0][0]['tgt']

    return f'{text}的意思是: {tran}'


#自然语言处理器，能更智能的回复
@on_natural_language(keywords={'翻译',})
async def _(session: NLPSession):
    return IntentCommand(90.0, 'translate')