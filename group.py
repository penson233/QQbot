from nonebot import on_notice, NoticeSession
from nonebot import on_command, CommandSession
import nonebot


#定义CQHTTP API接口
#调用bot对象
bot = nonebot.get_bot()



@on_notice('group_increase')
async def _(session: NoticeSession):
    if session.event.group_id == 332897571:
        await session.send(f'欢迎新奴隶~\n奴隶qq:{session.event.user_id}')


@on_notice('group_decrease')
async def _(session: NoticeSession):
    if session.event.group_id == 332897571:
        await session.send(f'奴隶:{session.event.user_id}\n默默无闻的走了~')


@on_command('jinyan',aliases=('禁言',))
async def jinyan(session: CommandSession):
    qq_id =session.get('qq',prompt='你想禁言谁?')
    if qq_id.isdigit():
        await bot.set_group_ban(group_id=332897571,user_id=qq_id,duration=60)


@on_command('quxiaojinyan',aliases=('取消禁言',))
async def jinyan(session: CommandSession):
    qq_id2 =session.get('qq',prompt='取消谁呀?')
    if qq_id2.isdigit():
        await bot.set_group_ban(group_id=332897571,user_id=qq_id2,duration=0)




