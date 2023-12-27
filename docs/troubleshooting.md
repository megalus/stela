# Troubleshooting Guide

### Common questions:

??? Question "How can I use [...] with Stela?"
    The use cases in [Using Frameworks](frameworks.md) above give a good hint about how to use Stela with several python projects.
    If you have a question which this guideline didn't resolve, please open an
    [issue](https://github.com/megalus/stela/issues).

??? Question "Got Error: _Stela did not found value for <MY_VARIABLE>_, but MY_VARIABLE exists in .env file."
    Please check if the root project folder is the same as the stela configuration file. If is correct, and your
    .env file is in another folder, you can use the `env_path` parameter to set the path to the .env file. You can also
    turn on Stela logs (`export STELA_SHOW_LOGS=true`) to see if the .env file and stela configuration file are being
    loaded correctly.

??? Question "Stela is not importing on my asynchronous code."
    Stela was tested against many popular asynchronous libraries like [Django-Ninja](https://github.com/vitalik/django-ninja), [Starlite](https://github.com/starlite-api/starlite)
    and [Sanic](https://github.com/sanic-org/sanic), and almost all the time the `from stela import env` import works successfully.

    But there's some cases, especially when using blocking final loaders, that the `from stela import env` import will not work, or will give a blocking error.
    In these cases, you can use the `aread_env` function to read the environment variables. This function is a coroutine, so you need to use the `await` keyword to call it.

    ```python
    from my_project import app
    from stela.asyncio import aread_env


    @app.get("/")
    async def root():
        env = await aread_env()
        return {
            "message": "Hello World",
            "environment": env.current_environment,
            "secret": env.MY_SECRET,
        }
    ```

### Example Apps

To see how this library works check the `Example Folder` provided [here](https://github.com/megalus/stela/tree/main/examples).

### Not working?

Don't panic. Get a towel and, please, open an [issue](https://github.com/megalus/stela/issues).
