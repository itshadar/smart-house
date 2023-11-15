from typer import Argument, Context

from src.cli.commands.electronic_device_command_set import \
    ElectronicDeviceCommandSet
from src.cli.loggers import logger
from src.core.utilities.constants import TVSettings


class TVCommandSet(ElectronicDeviceCommandSet):
    def register_commands(self) -> None:
        super().register_commands()

        @self.app.command()
        async def switch_channel(
            ctx: Context,
            channel: int = Argument(
                ...,
                help="channel value",
                min=TVSettings.MIN_CHANNEL,
                max=TVSettings.MAX_CHANNEL,
            ),
        ) -> None:
            async with ctx.obj.async_uow:
                await ctx.obj.repo.set_channel(ctx.obj.device_id, channel)
            logger.set_log(ctx.obj.device_name, "channel", channel)

        @self.app.command()
        async def get_channel(ctx: Context) -> None:
            async with ctx.obj.async_uow:
                channel = await ctx.obj.repo.get_channel(ctx.obj.device_id)
            logger.get_log(ctx.obj.device_name, "channel", channel)
