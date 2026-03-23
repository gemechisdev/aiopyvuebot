"""Webhook management CLI commands."""

from __future__ import annotations

import click

from aiopyvuebot.core.webhook import WebhookManager


def _get_manager(token: str | None) -> WebhookManager:
    if not token:
        raise click.ClickException(
            "BOT_TOKEN is required. Pass --token or set BOT_TOKEN in your .env."
        )
    return WebhookManager(token)


@click.group()
def webhook():
    """Manage the Telegram bot webhook."""


@webhook.command("set")
@click.option("--token", envvar="BOT_TOKEN", help="Telegram bot token.")
@click.option("--url", prompt="Your app URL (e.g. https://your-app.vercel.app)",
              help="Base URL of the deployed app.")
@click.option("--path", default="/api/telegram/webhook", show_default=True,
              help="Webhook path appended to the URL.")
def webhook_set(token, url, path):
    """Register (or update) the Telegram webhook."""
    mgr = _get_manager(token)
    try:
        result = mgr.set(url, path)
        if result.get("ok"):
            click.echo(f"✅ Webhook set to  {url.rstrip('/')}{path}")
        else:
            click.echo(f"❌ Telegram returned: {result}", err=True)
    except Exception as e:
        raise click.ClickException(str(e))


@webhook.command("info")
@click.option("--token", envvar="BOT_TOKEN", help="Telegram bot token.")
def webhook_info(token):
    """Show current webhook information."""
    mgr = _get_manager(token)
    try:
        data = mgr.info().get("result", {})
        url = data.get("url") or "(none)"
        pending = data.get("pending_update_count", 0)
        last_error = data.get("last_error_message", "")
        click.echo(f"🔗 URL:            {url}")
        click.echo(f"📬 Pending updates: {pending}")
        if last_error:
            click.echo(f"⚠️  Last error:     {last_error}")
    except Exception as e:
        raise click.ClickException(str(e))


@webhook.command("delete")
@click.option("--token", envvar="BOT_TOKEN", help="Telegram bot token.")
@click.option("--drop-pending", is_flag=True, help="Also drop pending updates.")
def webhook_delete(token, drop_pending):
    """Delete the current Telegram webhook."""
    mgr = _get_manager(token)
    try:
        result = mgr.delete(drop_pending=drop_pending)
        if result.get("ok"):
            click.echo("✅ Webhook deleted.")
        else:
            click.echo(f"❌ Telegram returned: {result}", err=True)
    except Exception as e:
        raise click.ClickException(str(e))
