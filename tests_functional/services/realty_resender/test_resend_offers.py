async def test_resend_offers(runner):
    # arrange

    # act
    await runner.run_python_command('phone-health-check-cron', '--provider=mts')

    # assert
