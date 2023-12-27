import click

from stela.cmd import stela_init


def print_title(title: str):
    title_length = len(title)
    box_width = title_length + 4

    click.echo("*" * box_width)
    click.echo("* " + " " * title_length + " *")
    click.echo("* " + title + " *")
    click.echo("* " + " " * title_length + " *")
    click.echo("*" * box_width)


@click.group("cli")
@click.pass_context
def cli(ctx):
    # No need for code, just group commands.
    pass


@cli.command()
@click.option("--default", is_flag=True, help="Use Default Values.")
def init(default):
    """Initialize Stela for your project."""
    print_title("Initializing Stela")
    click.pause(
        "This command will configure stela for your project.\nPress a key to continue."
    )
    initializer = stela_init.StelaInit(".")
    initializer.run(default)


@cli.command()
def gen_stub():
    """Generate Stela Stub."""
    from stela.config import StelaOptions
    from stela.helpers.stub import create_stela_stub
    from stela.main import StelaMain

    stela_config = StelaOptions.get_config()
    stela_data = StelaMain(options=stela_config)
    stela_data.get_project_settings()

    print_title("Generate Stela Stub file")
    result, message = create_stela_stub(stela_data.settings)
    click.secho(
        f"{'Success' if result else 'Error'}: {message}",
        fg="green" if result else "red",
    )


if __name__ == "__main__":
    cli()
