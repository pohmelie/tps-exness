from importlib import resources

from facet import ServiceMixin
from fastapi import Body
from fastapi.responses import HTMLResponse

from tps_exness.injector import inject
from tps_exness.server import WebServer
from tps_exness.entities import InCalculateQuery, State, OutCalculateQuery


INDEX_HTML = resources.read_text("tps_exness", "index.html")


class TPSExnessService(ServiceMixin):

    DISCOUNT_RULES = {
        50_000: 15,
        10_000: 10,
        7000: 7,
        5000: 5,
        1000: 3,
    }
    TAXES = {
        State.UT: 6.85,
        State.NV: 8.00,
        State.TX: 6.25,
        State.AL: 4.00,
        State.CA: 8.25,
    }

    @inject
    def __init__(self, web_server: WebServer):
        self.web_server = web_server

    @property
    def dependencies(self):
        return [
            self.web_server,
        ]

    async def start(self):
        self.configure_routes()

    def configure_routes(self):
        self.web_server.add_get("/", lambda: INDEX_HTML, response_class=HTMLResponse, include_in_schema=False)
        self.web_server.add_post("/calculate", self.calculate, response_model=OutCalculateQuery)

    async def calculate(self, query: InCalculateQuery = Body(...)) -> OutCalculateQuery:
        calculated_price = query.count * query.price
        for bound, discount in self.DISCOUNT_RULES.items():
            if calculated_price >= bound:
                calculated_price *= 1 - discount / 100
                break

        tax = self.TAXES[query.state]
        calculated_price *= 1 + tax / 100

        return OutCalculateQuery(calculated_price=calculated_price)
