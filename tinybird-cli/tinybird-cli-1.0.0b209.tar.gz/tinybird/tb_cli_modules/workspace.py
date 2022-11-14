
# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

import json
from os import getcwd
from pathlib import Path
import click
from click import Context

import humanfriendly
from tinybird.client import CanNotBeDeletedException, DoesNotExistException, TinyB
from tinybird.config import VERSION, write_config
from tinybird.tb_cli_modules.cli import cli
from tinybird.tb_cli_modules.common import _get_config, _get_workspace_plan_name, ask_for_user_token, coro, create_workspace_interactive, create_workspace_non_interactive, get_config_and_hosts, is_valid_starterkit
from tinybird.feedback_manager import FeedbackManager


@cli.group()
@click.pass_context
def workspace(ctx):
    '''Workspace commands'''


@workspace.command(name="ls")
@click.pass_context
@coro
async def workspace_ls(ctx):
    """List all the workspaces you have access to in the account you're currently authenticated to
    """

    client = ctx.obj['client']
    config = ctx.obj['config']

    if 'id' not in config:
        config = await _get_config(config['host'], config['token'], load_tb_file=False)

    response = await client.workspaces()

    if 'scope' in response and response['scope'] == 'admin':
        click.echo(FeedbackManager.warning_workspaces_admin_token())

    columns = ['name', 'id', 'role', 'plan', 'current']
    table = []
    click.echo(FeedbackManager.info_workspaces())

    for workspace in response['workspaces']:
        table.append([workspace['name'], workspace['id'], workspace['role'], _get_workspace_plan_name(workspace['plan']), config['id'] == workspace['id']])

    click.echo(humanfriendly.tables.format_smart_table(table, column_names=columns))


@workspace.command(name='use')
@click.argument('workspace_name_or_id')
@click.pass_context
@coro
async def workspace_use(ctx: Context, workspace_name_or_id: str):
    """Switch to another workspace. Use 'tb workspace ls' to list the workspaces you have access to.
    """

    config_file = Path(getcwd()) / ".tinyb"
    config = {}
    client: TinyB = ctx.ensure_object(dict)['client']
    config = ctx.ensure_object(dict)['config']

    try:
        if 'id' not in config:
            config = await _get_config(config['host'], config['token'], load_tb_file=False)
        else:
            with open(config_file) as file:
                config = json.loads(file.read())

        response = await client.workspaces()

        workspaces = response['workspaces']
        workspace = next((workspace for workspace in workspaces if workspace['name'] == workspace_name_or_id or workspace['id'] == workspace_name_or_id), None)

        if not workspace:
            click.echo(FeedbackManager.error_workspace(workspace=workspace_name_or_id))
            return

        client = TinyB(workspace['token'], config['host'], version=VERSION)

        config['id'] = workspace['id']
        config['name'] = workspace['name']
        config['token'] = workspace['token']
        host = config['host']

        tokens = config.get('tokens', {})
        tokens[host] = config['token']

        config['tokens'] = tokens

        ctx.ensure_object(dict)['client'] = client
        ctx.ensure_object(dict)['config'] = config

        await write_config(config)
        click.echo(FeedbackManager.success_now_using_config(name=config['name'], id=config['id']))
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=str(e)))
        return


@workspace.command(name='current')
@click.pass_context
@coro
async def workspace_current(ctx: Context):
    """Show the workspace you're currently authenticated to
    """

    client: TinyB = ctx.ensure_object(dict)['client']
    config = ctx.ensure_object(dict)['config']

    if 'id' not in config:
        config = await _get_config(config['host'], config['token'], load_tb_file=False)

    response = await client.workspaces()

    columns = ['name', 'id', 'role', 'plan', 'current']
    table = []
    click.echo(FeedbackManager.info_current_workspace())

    for workspace in response['workspaces']:
        if config['id'] == workspace['id']:
            table.append([workspace['name'], workspace['id'], workspace['role'], _get_workspace_plan_name(workspace['plan']), True])

    click.echo(humanfriendly.tables.format_smart_table(table, column_names=columns))


@workspace.command(name='clear', short_help="Drop all the resources inside a project. This command is dangerous because it removes everything, use with care.")
@click.option('--yes', is_flag=True, default=False, help="Do not ask for confirmation")
@click.option('--dry-run', is_flag=True, default=False, help="Run the command without removing anything")
@click.pass_context
@coro
async def clear_workspace(ctx: Context, yes: bool, dry_run: bool):
    """Drop all the resources inside a project. This command is dangerous because it removes everything, use with care"""

    """ Get current workspace to add the name to the alert message"""
    client: TinyB = ctx.ensure_object(dict)['client']
    config = ctx.ensure_object(dict)['config']

    if 'id' not in config:
        config = await _get_config(config['host'], config['token'], load_tb_file=False)

    response = await client.workspaces()

    columns = ['name', 'id', 'role', 'plan', 'current']
    table = []
    click.echo(FeedbackManager.info_current_workspace())

    for workspace in response['workspaces']:
        if config['id'] == workspace['id']:
            table.append([workspace['name'], workspace['id'], workspace['role'], _get_workspace_plan_name(workspace['plan']), True])

    click.echo(humanfriendly.tables.format_smart_table(table, column_names=columns))

    if yes or click.confirm(FeedbackManager.warning_confirm_clear_workspace()):

        pipes = await client.pipes(dependencies=False, node_attrs='name', attrs='name')
        pipe_names = [pipe['name'] for pipe in pipes]
        for pipe_name in pipe_names:
            if not dry_run:
                click.echo(FeedbackManager.info_removing_pipe(pipe=pipe_name))
                try:
                    await client.pipe_delete(pipe_name)
                except DoesNotExistException:
                    click.echo(FeedbackManager.info_removing_pipe_not_found(pipe=pipe_name))
            else:
                click.echo(FeedbackManager.info_dry_removing_pipe(pipe=pipe_name))

        datasources = await client.datasources()
        ds_names = [datasource['name'] for datasource in datasources]
        for ds_name in ds_names:
            if not dry_run:
                click.echo(FeedbackManager.info_removing_datasource(datasource=ds_name))
                try:
                    await client.datasource_delete(ds_name, force=True)
                    print(ds_names, ds_name)
                except DoesNotExistException:
                    click.echo(FeedbackManager.info_removing_datasource_not_found(datasource=ds_name))
                except CanNotBeDeletedException as e:
                    click.echo(FeedbackManager.error_datasource_can_not_be_deleted(datasource=ds_name, error=e))
                except Exception as e:
                    if ("is a Shared Data Source" in str(e)):
                        click.echo(FeedbackManager.error_operation_can_not_be_performed(error=e))
                    else:
                        raise click.ClickException(FeedbackManager.error_exception(error=e))
            else:
                click.echo(FeedbackManager.info_dry_removing_datasource(datasource=ds_name))


@workspace.command(name='create', short_help="Create a new Workspace for your Tinybird user")
@click.argument('workspace_name', required=False)
@click.option('--starter-kit', type=str, required=False, help="Use a Tinybird starter kit as a template")
@click.option('--user_token', is_flag=False, default=None, help="Do not ask for your user token")
@click.option('--fork', is_flag=True, default=False, help="When enabled, we will share all datasource from the current workspace to the new created one")
@click.pass_context
@coro
async def create_workspace(ctx: Context, workspace_name: str, starter_kit: str,
                           user_token: str, fork: bool):

    if starter_kit:
        if not await is_valid_starterkit(ctx, starter_kit):
            click.echo(FeedbackManager.error_starterkit_name(starterkit_name=starter_kit))
            return

    if not user_token:
        _, _, ui_host = await get_config_and_hosts(ctx)
        user_token = ask_for_user_token('create a new workspace', ui_host)
        if not user_token:
            return

    # If we have at least workspace_name, we start the non interactive
    # process, creating an empty workspace
    if workspace_name:
        await create_workspace_non_interactive(ctx, workspace_name, starter_kit,
                                               user_token, fork)
    else:
        await create_workspace_interactive(ctx, workspace_name, starter_kit,
                                           user_token, fork)


@workspace.command(name='delete', short_help="Delete a Workspace for your Tinybird user")
@click.argument('workspace_name_or_id')
@click.option('--user_token', is_flag=False, default=False, help="Do not ask for your user token")
@click.option('--yes', is_flag=True, default=False, help="Do not ask for confirmation")
@click.pass_context
@coro
async def delete_workspace(ctx: Context, workspace_name_or_id: str, user_token: str, yes: bool):
    """Delete a workspace where you are admin"""

    client: TinyB = ctx.ensure_object(dict)['client']
    config, host, ui_host = await get_config_and_hosts(ctx)

    if not user_token:
        user_token = ask_for_user_token('delete a workspace', ui_host)

    if yes or click.confirm(FeedbackManager.warning_confirm_delete_workspace()):
        workspaces = (await client.workspaces()).get('workspaces', [])
        workspace_to_delete = next((workspace for workspace in workspaces if workspace['name'] == workspace_name_or_id or workspace['id'] == workspace_name_or_id), None)

        if not workspace_to_delete:
            raise click.ClickException(FeedbackManager.error_workspace(workspace=workspace_name_or_id))

        client.token = user_token

        try:
            await client.delete_workspace(workspace_to_delete['id'])
            click.echo(FeedbackManager.success_workspace_deleted(workspace_name=workspace_to_delete['name']))
        except Exception as e:
            click.echo(FeedbackManager.error_exception(error=str(e)))
            return
