from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
import random


@on_command('baoerjie',aliases=('宝儿姐'))
async def baoerjie(session: CommandSession):

    name = session.get('name',prompt='叫姐干哈')

    tu = await tu_cao(name)


    await session.send(tu)





@baoerjie.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:

            session.state['name'] = stripped_arg
        return

    if not stripped_arg:
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('再没事喊姐，窝把你一家都埋了!')

    # 如果当前正在向用户询问更多信息，且用户输入有效，则放入会话状态
    session.state[session.current_key] = stripped_arg



async def tu_cao(name: str) -> str:
    dir =['再叫，把你埋咯!','想尝尝阿威十八式吗????','你要当姐的奴隶吗!']
    d = random.choice(dir)
    return f'{d}'




@on_natural_language(keywords={'宝儿姐',})
async def _(session: NLPSession):
    return IntentCommand(90.0, 'baoerjie')