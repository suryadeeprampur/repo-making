from aiohttp import web

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("RDX_PVT_LTD")


async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app





# RDX Developer 
# Don't Remove Credit 🥺
# Telegram Channel @RDX_PVT_LTD
# Backup Channel @RDX_PVT_LTD
# Developer @RDX_PVT_LTD
# Contact @RDX1444
