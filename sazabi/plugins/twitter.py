from discord.user import User

from sazabi.types import SazabiBotPlugin


class Twitter(SazabiBotPlugin):
    async def parse(self, client, message, *args, **kwargs):
        twitter_client = kwargs.get('twitter')
        if message.content.startswith('https://twitter.com/'):
            status = twitter_client.show_status(id=message.content.split('/')[-1])
            try:
                if len(status['extended_entities']['media']) > 1:
                    extra_images = list(map(
                        lambda media: media['media_url_https'], 
                        status['extended_entities']['media'][1:]
                    ))
                if status is not None:
                    await client.send_message(message.channel, '\n'.join(extra_images))
            except KeyError:
                pass
            except Exception as e:
                self.logger.exception('Something went wrong grabbing tweet')
                raise e
