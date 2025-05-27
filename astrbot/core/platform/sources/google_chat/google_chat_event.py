import aiohttp
from astrbot.api.event import AstrMessageEvent, MessageChain
from astrbot.api.message_components import Plain
from astrbot import logger


class GoogleChatMessageEvent(AstrMessageEvent):
    @staticmethod
    async def _send_chain(webhook_url: str, message: MessageChain):
        text = ""
        for comp in message.chain:
            if isinstance(comp, Plain):
                text += comp.text
        payload = {"text": text or ""}
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=payload) as resp:
                if resp.status != 200:
                    try:
                        error_text = await resp.text()
                    except Exception:
                        error_text = resp.status
                    logger.error(f"Failed to send Google Chat message: {error_text}")

    async def send(self, message: MessageChain):
        await self._send_chain(self.session_id, message)
        await super().send(message)
