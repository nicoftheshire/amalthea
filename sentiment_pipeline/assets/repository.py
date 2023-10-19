from dagster import (
    load_assets_from_modules,
    repository,
    define_asset_job,
    ScheduleDefinition
)
import assets

sentiment_job = define_asset_job(name="10min_schedule", selection="*")
sentiment_schedule = ScheduleDefinition(
    job=sentiment_job,
    cron_schedule="*/10 * * * *"
)


@repository
def sentiment_pipeline():
    return [
        sentiment_job,
        sentiment_schedule,
        load_assets_from_modules([assets])
    ]
