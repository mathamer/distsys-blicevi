import asyncio
import aiohttp
from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/getJokes")
async def get_jokes(req):
    tasks1 = []
    tasks2 = []
    async with aiohttp.ClientSession() as session:
        for _ in range(6):
            tasks1.append(
                asyncio.create_task(
                    session.get("https://official-joke-api.appspot.com/random_joke")
                )
            )
            tasks2.append(
                asyncio.create_task(session.get("https://randomuser.me/api/"))
            )
        res = await asyncio.gather(*tasks1)
        res = [await x.json() for x in res]
        # res2 = await asyncio.gather(*tasks2)
        # res2 = [await x.json() for x in res2]
    tasks1 = []
    tasks2 = []
    async with aiohttp.ClientSession() as session:
        for i in range(len(res)):
            tasks1.append(
                asyncio.create_task(
                    session.post("http://127.0.0.1:8080/filterUser", json=res[i])
                )
            )
            tasks2.append(
                asyncio.create_task(
                    session.post("http://127.0.0.1:8080/filterJoke", json=res[i])
                )
            )
        res = await asyncio.gather(*tasks1)
        res = [await x.json() for x in res]
        res2 = await asyncio.gather(*tasks2)
        res2 = [await x.json() for x in res2]
    print(res)
    return web.json_response({"status": "ok", "messages": res}, status=200)


temp = []


@routes.post("/filterUser")
async def filter_user(request):
    try:
        json_data = await request.json()
        temp.append(json_data)
        web.json_response(
            {
                "Name": json_data.get("name"),
                "City": json_data.get("city"),
                "Username": json_data.get("username"),
            },
            status=200,
        )
    except Exception as e:
        return web.json_response({"Failed": str(e)}, status=500)


@routes.post("/filterJoke")
async def filter_joke(request):
    try:
        json_data = await request.json()
        temp.append(json_data)
        web.json_response(
            {"Setup": json_data.get("setup"), "Punchline": json_data.get("punchline")},
            status=200,
        )
    except Exception as e:
        return web.json_response({"Failed": str(e)}, status=500)


# wip
@routes.post("/storeData")
async def store_data(request):
    req = await request.json()
    async with aiosqlite.connect(
        "/Users/mh-mbp/Projects/distsys-blicevi/data.db"
    ) as db:
        await db.execute(
            "INSERT INTO joke (setup,punchline) VALUES (?,?)",
            (req["setup"], req["punchline"]),
        )
        await db.commit()

    return web.json_response({"status": "ok"}, status=200)


app = web.Application()

app.router.add_routes(routes)

web.run_app(app)
