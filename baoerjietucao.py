from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand


@on_command('baoer',aliases=('张楚岚'))
async def baoer(session: CommandSession):
    await session.send('我奴隶在练老农功，咩时间鸟你.')


@on_natural_language(keywords={'张楚岚',})
async def _(session: NLPSession):
    return IntentCommand(90.0, 'baoer')


@on_command('baoer2',aliases=('观音坐莲','老汉推车','连续中出','阿威十八式','毒龙钻'))
async def baoer2(session: CommandSession):
    await session.send('喊啥子喊，你又学不会')

@baoer2.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['word'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('小心我把你全家都埋咯!')

    session.state[session.current_key] = stripped_arg


@on_natural_language(keywords={'观音坐莲','老汉推车','连续中出','阿威十八式','毒龙钻',})
async def _(session: NLPSession):
    return IntentCommand(90.0, 'baoer2')