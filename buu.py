from nonebot import on_command, CommandSession
import requests
from nonebot import on_natural_language, NLPSession, IntentCommand
from jieba import posseg
import re



@on_command('buu',aliases=('懒狗查询','刷题'))
async def buu(session: CommandSession):
    # 从会话状态（session.state）中获取用户信息('username'），如果当前不存在，则询问用户
    username = session.get('username',prompt='懒狗给我好好输!')

    await session.send("俺在查这娃儿，稍等一会.........")


    #获取刷题结果
    grade_report = await get_grade(username)

    #向用户发送结果
    await session.send(grade_report)


# buu.args_parser 装饰器将函数声明为 buu 命令的参数解析器


@buu.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:

            session.state['username'] = stripped_arg
        return

    if not stripped_arg:

        session.pause('还发!小心姐弄死你!!!')

    session.state[session.current_key] = stripped_arg



async def get_grade(username: str) -> str:
    #爬取buu刷题信息
    r1 = requests.get('https://buuoj.cn/plugins/new-challenges/affiliation_daily')
    t = r1.json()

    with open('1.txt', 'r') as f:
        team = []
        b = f.readlines()
        for i in b:
            i = re.sub('\n', '', i)
            team.append(i)
    flag = 0

    for i in range(0, len(team)):
        team[i]=re.sub('&','%26',team[i])
        r2 = requests.get('https://buuoj.cn/plugins/new-challenges/affiliation_daily?affiliation={}'.format(team[i]))
        t2 = r2.json()

        count = -1
        for i in range(0, len(t2['data'])):
            team_username = t2['data'][i]['user_name']
            if team_username == username:
                flag = 1
                count = int(t2['data'][i]['count'])
                break
        if count >= 0:
            break


    for i in range(0, len(t['data'])):
        if t['data'][i]['user_name'] == username:
            count = int(t['data'][i]['count'])
            flag = 1
            break

    if flag == 0:
        return f'{username}:\n姐查不到你，你被buu扔了!'

    if count == 1:

        return f'{username}就做了{count}道题,这娃儿是懒狗。'

    elif count == 0:
        return f'{username}啥都没做,这娃儿是废狗。'

    else:
        return f'{username}一共做了{count}道题，这娃儿还阔以!'



@on_natural_language(keywords={'懒狗','刷题'})
async def _(session: NLPSession):
    return IntentCommand(90.0, 'buu',)