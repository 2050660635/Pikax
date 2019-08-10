import datetime
from typing import Union

from .. import params, settings
from pikax.v2.models import PikaxUserInterface, PikaxResult, PikaxPagesInterface
from .models import PikaxInterface
from .items import LoginHandler


class Pikax(PikaxInterface):

    def __init__(self, username=None, password=None):
        self._login_handler = LoginHandler()
        self.username = username
        self.password = password

        if username and password:
            self.login(self.username, self.password)

    def access(self, user_id: int) -> PikaxUserInterface:
        pass

    def login(self, username: str = settings.username, password: str = settings.password) -> (
            PikaxUserInterface, PikaxPagesInterface):
        pass

    def search(self, keyword: str = '',
               search_type: params.Type = params.Type.ILLUST,
               match: params.Match = params.Match.EXACT,
               sort: params.Sort = params.Sort.DATE_DESC,
               search_range: datetime.timedelta = None,
               popularity: Union[int, str] = None,
               limit: int = None) \
            -> PikaxResult:
        pass

    def rank(self, limit: int = datetime.datetime,
             date: Union[str, datetime.datetime] = format(datetime.datetime.today(), '%Y%m%d'),
             content: params.Type = params.Type.ILLUST,
             rank_type: params.Rank = params.Rank.DAILY) \
            -> PikaxResult:
        pass

    def visits(self, user_id: int) -> PikaxUserInterface:
        pass
