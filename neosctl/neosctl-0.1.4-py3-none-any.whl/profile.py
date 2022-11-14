import re
import typing

import click
import typer

from neosctl import schema
from neosctl.util import get_user_profile_section
from neosctl.util import prettify_json
from neosctl.util import remove_config
from neosctl.util import send_output
from neosctl.util import upsert_config


app = typer.Typer()


r = re.compile(r"http[s]?:\/\/.*")


def validate_url(value):
    m = r.match(value)
    if m is None:
        raise click.UsageError("Invalid url, must match pattern: `{}`.".format(r))
    return value


@app.command()
def init(
    ctx: typer.Context,
    gateway_api_url: typing.Optional[str] = typer.Option(None, "--gateway-api-url", "-g"),
    registry_api_url: typing.Optional[str] = typer.Option(None, "--registry-api-url", "-r"),
    iam_api_url: typing.Optional[str] = typer.Option(None, "--iam-api-url", "-i"),
    username: typing.Optional[str] = typer.Option(None, "--username", "-u"),
    ignore_tls: bool = typer.Option(
        False,
        "--ignore-tls",
        help="Ignore TLS errors (useful in local/development environments",
    ),
):
    """Initialise a profile.

    Create a profile that can be reused in later commands to define which
    services to interact with, and which user to interact as.

    Call `init` on an existing profile will update the existing profile.
    """
    typer.echo("Initialising [{}] profile.".format(ctx.obj.profile_name))

    urls = {
        "gateway_api_url": gateway_api_url,
        "registry_api_url": registry_api_url,
        "iam_api_url": iam_api_url,
    }
    for key, default, prompt in [
        ("gateway_api_url", ctx.obj.get_gateway_api_url(), "Gateway API url"),
        ("registry_api_url", ctx.obj.get_registry_api_url(), "Registry API url"),
        ("iam_api_url", ctx.obj.get_iam_api_url(), "IAM API url"),
    ]:

        if urls[key] is None:
            urls[key] = typer.prompt(
                prompt,
                default=default,
                value_proc=validate_url,
            )
        else:
            validate_url(urls[key])

    if username is None:
        kwargs = {}
        if ctx.obj.profile:
            kwargs["default"] = ctx.obj.profile.user
        username = typer.prompt(
            "Username",
            **kwargs,
        )

    profile = schema.Profile(
        user=username,
        access_token="",
        refresh_token="",
        ignore_tls=ignore_tls,
        **urls,
    )

    upsert_config(ctx, profile)


@app.command()
def delete(
    ctx: typer.Context,
):
    """Delete a profile.
    """
    typer.confirm("Remove [{}] profile".format(ctx.obj.profile_name), abort=True)
    remove_config(ctx)


@app.command()
def view(
    ctx: typer.Context,
):
    """View configuration for a profile.
    """
    send_output(
        msg=prettify_json({**get_user_profile_section(ctx.obj.config, ctx.obj.profile_name)}),
    )
