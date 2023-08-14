import click

from stela.cmd import stela_converter, stela_init


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
@click.option("--convert", is_flag=True, help="Convert Stela old data if found.")
def init(use_default, convert):
    """Initialize Stela for your project."""
    print_title("Initializing Stela")
    click.pause(
        "This command will configure stela for your project.\nPress a key to continue."
    )
    initializer = stela_init.StelaInit(".")
    initializer.run(use_default, convert)


@cli.command()
@click.option("--revert", is_flag=True, help="Revert Stela format data update.")
def update(revert):
    """Update Stela 4.x format data to Stela 5."""
    root_dir = "."
    converter = stela_converter.StelaConverter(root_dir)
    if revert:
        print_title("Revert Stela Data Update")
        converter.revert()
    else:
        print_title("Start Stela data Update")
        converter.run()


@cli.command()
def gen_stub():
    """Generate Stela Stub."""
    from stela.config import StelaOptions
    from stela.config.stub import create_stela_stub
    from stela.main.dot import StelaDotMain

    stela_config = StelaOptions.get_config()
    stela_data = StelaDotMain(options=stela_config)
    stela_data.get_project_settings()

    print_title("Generate Stela Stub file")
    result, message = create_stela_stub(stela_data.settings)
    click.secho(
        f"{'Success' if result else 'Error'}: {message}",
        fg="green" if result else "red",
    )


if __name__ == "__main__":
    cli()
