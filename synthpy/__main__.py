import click
import sys
import colored
import logging


import coloredlogs


__SYNTHPY = r"""
Welcome to
                     _   _                 
     ___ _   _ _ __ | |_| |__  _ __  _   _ 
    / __| | | | '_ \| __| '_ \| '_ \| | | |
    \__ \ |_| | | | | |_| | | | |_) | |_| |
    |___/\__, |_| |_|\__|_| |_| .__/ \__, |
         |___/                |_|    |___/    version: {version}
"""


@click.command()
@click.option(
    "--host",
    type=str,
    help="the synth host (default: localhost:8182)",
    default="localhost:8182",
)
@click.option(
    "--namespace", type=str, help="the default namespace to prefix all requests with"
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "WARNING", "ERROR"]),
    default="WARNING",
    help="the desired logging verbosity (default: WARNING)",
)
@click.option(
    "--ipython",
    is_flag=True,
    default=False,
    help="wether to use synthpy with IPython (requires IPython)",
)
@click.pass_context
def shell(ctx, host, namespace, log_level, ipython):
    import synthpy
    from synthpy import (
        Synth,
        Array,
        OneOf,
        Object,
        Faker,
        Id,
        DateTime,
        Categorical,
        Bool,
        Number,
        Range,
        SameAs,
        String,
    )

    client_name = "synth"
    client_name_ = colored.stylize(client_name, colored.attr("bold"))
    header = f"{__SYNTHPY}\nGet started by accessing the client at the variable '{client_name_}'.\n\n".format(
        version=synthpy.__version__,
    )
    footer = ""

    logger = logging.getLogger("synthpy")
    coloredlogs.install(level=log_level)

    defaults = {}
    if namespace:
        defaults["namespace"] = namespace

    with Synth(host, defaults=defaults) as client:
        scope_vars = {
            client_name: client,
            "Array": Array,
            "OneOf": OneOf,
            "Object": Object,
            "Faker": Faker,
            "DateTime": DateTime,
            "Categorical": Categorical,
            "Bool": Bool,
            "Number": Number,
            "Id": Id,
            "Range": Range,
            "SameAs": SameAs,
            "String": String,
        }

        if ipython:
            import IPython

            print(header)
            IPython.start_ipython(argv=[], user_ns=scope_vars)
            print(footer)

        else:
            from code import InteractiveConsole
            from colored import stylize_interactive, fg

            sys.ps1 = stylize_interactive("synthpy> ", fg("magenta"))
            InteractiveConsole(locals=scope_vars).interact(
                banner=header, exitmsg=footer
            )


if __name__ == "__main__":
    shell()
