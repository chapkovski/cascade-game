from background_task import background
from logging import getLogger
from .models import Constants, Player, Subsession

logger = getLogger(__name__)

logger.debug('HUHUHU')
print('HUHUHU')
@background(schedule=10)
def demo_task(message, player_id):
    print('chapovski')
    player = Player.objects.get(pk=player_id)
    player.current_ball = 'PIZDA'
    player.save()
    logger.debug('demo_task. message={0}'.format(message))
