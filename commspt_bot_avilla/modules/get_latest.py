from arclet.alconna import Alconna, Args, CommandMeta
from arclet.alconna.graia import CommandResult, alcommand
from avilla.core import Context, Message

from commspt_bot_avilla.models.version_api import (
    AuthlibInjectorLatest,
    LibericaJavaLatest,
)
from commspt_bot_avilla.utils.adv_filter import dispatcher_from_preset_cafe
from commspt_bot_avilla.utils.setting_manager import S_


@alcommand(
    Alconna(
        f"{S_.command_prompt}csl.latest",
        meta=CommandMeta(
            description="获取 CustomSkinLoader 最新版本信息",
            usage=f"{S_.command_prompt}csl.latest",
            example=f"{S_.command_prompt}csl.latest",
            author="SerinaNya",
        ),
    ),
)
@dispatcher_from_preset_cafe
async def _(ctx: Context, message: Message):
    await ctx.scene.send_message("「CustomSkinLoader」\n请前往 https://littleskin.cn/user/config 下载", reply=message)


@alcommand(
    Alconna(
        f"{S_.command_prompt}ygg.latest",
        meta=CommandMeta(
            description="获取 Yggdrasil 最新版本信息",
            usage=f"{S_.command_prompt}ygg.latest",
            example=f"{S_.command_prompt}ygg.latest",
            author="SerinaNya",
        ),
    ),
)
@dispatcher_from_preset_cafe
async def _(ctx: Context, message: Message):
    ygg_latest = await AuthlibInjectorLatest.get()
    await ctx.scene.send_message(
        f"「Authlib Injector」\n当前最新版本 > {ygg_latest.version}\n下载地址 > {ygg_latest.download_url}",
        reply=message,
    )


@alcommand(
    Alconna(
        f"{S_.command_prompt}java.latest",
        Args["version", int, 17]["type", str, "jre"]["os", str, "windows"],
        meta=CommandMeta(
            description="获取 Java 最新版本信息",
            usage=f"{S_.command_prompt}java.latest [version] [type] [os]",
            example=f"{S_.command_prompt}java.latest 17 jdk windows",
            author="SerinaNya",
        ),
    ),
)
@dispatcher_from_preset_cafe
async def _(ctx: Context, message: Message, res: CommandResult):
    parma = res.result
    version: int = parma["version"]
    ftype: str = parma["type"]
    os: str = parma["os"]
    java_latest: list[LibericaJavaLatest] = await LibericaJavaLatest.get(
        version_feature=version,
        bundle_type=f"{ftype}-full",
        os=os,
    )
    await ctx.scene.send_message(
        f"「Liberica Java {java_latest[0].feature_version} ({java_latest[0].bundle_type})」\n下载地址 > {java_latest[0].download_url_mirror}",
        reply=message,
    )
