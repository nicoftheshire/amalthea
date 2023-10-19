from dagster import Definitions, load_assets_from_modules, define_asset_job, ScheduleDefinition

from . import assets

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
    schedules=[
        ScheduleDefinition(
            job=define_asset_job(name="5minute_refresh", selection="*"),
            cron_schedule="*/5 * * * *",
        )
    ],
)

# from dagster import (
#     load_assets_from_package_module,
#     Definitions,
#     define_asset_job,
#     ScheduleDefinition,
# )
# from my_dagster_project import assets
# import os
# from github import Github
#
# defs = Definitions(
#     assets=load_assets_from_package_module(assets),
#     schedules=[
#         ScheduleDefinition(
#             job=define_asset_job(name="daily_refresh", selection="*"),
#             cron_schedule="@daily",
#         )
#     ],
#     resources={"github_api": Github(os.environ["GITHUB_ACCESS_TOKEN"])},
# )
