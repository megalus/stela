from asgiref.sync import sync_to_async


async def aread_env() -> "Stela":
    """Reload Stela configuration asynchronous.

    Not really needed for default configuration
    but in some cases, if you use a complex blocking custom loader,
    all operation will be wrapped in a coroutine here.

    """
    from stela.utils import read_env

    return await sync_to_async(read_env)()
