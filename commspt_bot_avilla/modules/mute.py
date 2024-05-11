from datetime import timedelta
from typing import Literal

from arclet.alconna import Alconna, Args, CommandMeta
from arclet.alconna.graia import Match, alcommand
from avilla.core import Context, Message, MuteCapability, Notice

from commspt_bot_avilla.utils.adv_filter import (
    dispatcher_from_preset_cafe,
    dispather_by_admin_only,
)
from commspt_bot_avilla.utils.setting_manager import S_

_GROUP_NAME_MAPPING = {
    "main": S_.defined_qq.littleskin_main,
    "cafe": S_.defined_qq.littleskin_cafe,
}


# MARK: %mute
@alcommand(
    Alconna(
        r"%mute",
        Args["target", int | Notice]["duration", int, 10][
            "group", Literal["main", "cafe"] | None, None
        ],
        meta=CommandMeta(
            description="禁言用户 (commspt only)",
            usage=r"%mute <target / qq> [duration] [group]",
            example=r"%mute @user 10 main",
            author="SerinaNya",
        ),
    )
)
@dispatcher_from_preset_cafe
@dispather_by_admin_only
async def mute(
    ctx: Context,
    target: Match[int | Notice],
    duration: int,
    group: Match[Literal["main", "cafe"] | None],
):
    if group.result:
        if isinstance(target.result, Notice):
            await ctx.scene.send_message("指定群组时不允许使用 @user")
            return

        await ctx[MuteCapability.mute](
            target=(
                ctx.scene.into(f"::group({_GROUP_NAME_MAPPING[group.result]})").into(
                    f"~.member({target.result})"
                )
            ),
            duration=timedelta(minutes=duration),
        )
        return

    else:
        await ctx[MuteCapability.mute](
            target=(
                target.result.target
                if isinstance(target.result, Notice)
                else ctx.scene.into(f"~.member({target.result})")
            ),
            duration=timedelta(minutes=duration),
        )
        return


# MARK: %unmute
@alcommand(
    Alconna(
        r"%unmute",
        Args["target", int | Notice]["group", Literal["main", "cafe"] | None, None],
        meta=CommandMeta(
            description="解除禁言 (commspt only)",
            usage=r"%unmute <target / qq> [group]",
            example=r"%unmute @user main",
            author="SerinaNya",
        ),
    )
)
@dispatcher_from_preset_cafe
@dispather_by_admin_only
async def unmute(
    ctx: Context,
    target: Match[int | Notice],
    group: Match[Literal["main", "cafe"] | None],
):
    if group.result:

        if isinstance(target.result, Notice):
            await ctx.scene.send_message("指定群组时不允许使用 @user")
            return

        await ctx[MuteCapability.unmute](
            target=(
                ctx.scene.into(f"::group({_GROUP_NAME_MAPPING[group.result]})").into(
                    f"~.member({target.result})"
                )
            ),
        )
        return

    else:
        await ctx[MuteCapability.unmute](
            target=(
                target.result.target
                if isinstance(target.result, Notice)
                else ctx.scene.into(f"~.member({target.result})")
            )
        )
        return


# MARK: %recall
@alcommand(
    Alconna(
        r"%recall",
        meta=CommandMeta(
            description="撤回消息 (commspt only)",
            usage=r"%recall",
            example=r"%recall",
            author="FalfaChino",
        ),
    )
)
@dispatcher_from_preset_cafe
@dispather_by_admin_only
async def recall(ctx: Context, message: Message):
    if message.reply:
        origin_message = await ctx.pull(Message, message.reply)
    else:
        await ctx.scene.send_message("需要回复消息")
        return
    await origin_message.revoke()
    await message.revoke()
