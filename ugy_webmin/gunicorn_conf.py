#!/usr/bin/env python3
import click
from pathlib import Path
from typing import Dict

config = {
    "bind": "unix:/tmp/socket.sock",
    "backlog": 1024,
    "workers": 2,
    "worker_connections": 500,
    "timeout": 30,
    "keepalive": 2,
    "wsgi_app": "ugy_webmin.wsgi:app",
    "user": "www-data",
}


class ConfigWriter:
    @staticmethod
    def write(conf_path: Path, config: Dict):

        with conf_path.open(mode="w") as fh:
            for key, val in config.items():
                fh.write(f"{key}={val}\n")



@click.command(
    context_settings=dict(
        allow_extra_args=True,
    )
)
@click.pass_context
@click.argument("out-dir", type=click.Path(exists=True))
def main(ctx, out_dir):
    """Generates a gunicorn.conf file.

    Update configs by adding `key=value` pairs.

    OUT_DIR is the location to save the config file.
    """

    for item in ctx.args:
        config.update([item.split("=")])

    conf_path = Path(out_dir).joinpath("gunicorn.conf.py")
    ConfigWriter.write(conf_path, config)

    click.echo(f"Wrote config file to {conf_path}")

if __name__ == "__main__":
    main()
