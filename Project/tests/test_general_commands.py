import sys
from io import StringIO
from io import TextIOWrapper
from logging import Logger

from django.core.management import call_command
from django.test import override_settings
from pytest import fixture
from pytest import mark

from Emails.models import Email
from Emails.models import Suggestion
from Project.management.commands.populate_db import Command as PopulateCommand
from Users.fakers.user import UserFaker
from Users.models import Profile
from Users.models import User


COMMAND: str = "populate_db"


@fixture(scope="function")
def silent_stdout():
    capturedOutput: StringIO = StringIO()
    sys.stdout: TextIOWrapper = capturedOutput
    yield sys.stdout
    sys.stdout = sys.__stdout__


@mark.django_db
class TestPopulateCommand:
    @override_settings(ENVIRONMENT_NAME="production")
    def test_populate_db_command_fails_on_non_dev_mode(
        self, caplog: Logger
    ) -> None:
        caplog.clear()
        call_command(COMMAND, "-i", "5")
        message: str = (
            "This command creates fake data do NOT run "
            + "this in production environments"
        )
        assert [message] == [record.message for record in caplog.records]

    def test_create_fake_users(self, silent_stdout: TextIOWrapper) -> None:
        silent_stdout
        command: PopulateCommand = PopulateCommand()
        assert User.objects.all().count() == 0
        command.create_fake_users(3)
        assert User.objects.all().count() == 3

    def test_create_fake_verify_emails(
        self, silent_stdout: TextIOWrapper
    ) -> None:
        silent_stdout
        command: PopulateCommand = PopulateCommand()
        users: list = [UserFaker(), UserFaker()]
        assert User.objects.all().count() == 2
        assert Email.objects.all().count() == 0
        command.create_fake_verify_emails(users)
        assert User.objects.all().count() == 2
        assert Email.objects.all().count() == 2

    def test_create_fake_profiles(self, silent_stdout: TextIOWrapper) -> None:
        silent_stdout
        command: PopulateCommand = PopulateCommand()
        users: list = [UserFaker(), UserFaker()]
        assert User.objects.all().count() == 2
        assert Profile.objects.all().count() == 0
        command.create_fake_profiles(users)
        assert User.objects.all().count() == 2
        assert Profile.objects.all().count() == 2

    def test_create_fake_suggestions(
        self, silent_stdout: TextIOWrapper
    ) -> None:
        silent_stdout
        command: PopulateCommand = PopulateCommand()
        users: list = [UserFaker(), UserFaker()]
        assert User.objects.all().count() == 2
        assert Suggestion.objects.all().count() == 0
        command.create_fake_suggestions(users)
        assert User.objects.all().count() == 2
        assert Suggestion.objects.all().count() == 2

    def test_create_admin_user(self, silent_stdout: TextIOWrapper) -> None:
        silent_stdout
        command: PopulateCommand = PopulateCommand()
        assert User.objects.filter(is_admin=True).count() == 0
        command.create_admin_user()
        assert User.objects.filter(is_admin=True).count() == 1

    def test_command_without_admin_flag(
        self, silent_stdout: TextIOWrapper
    ) -> None:
        silent_stdout
        assert User.objects.all().count() == 0
        assert Email.objects.all().count() == 0
        assert Profile.objects.all().count() == 0
        assert Suggestion.objects.all().count() == 0
        call_command(COMMAND, "-i", "5")
        assert User.objects.all().count() == 6
        assert Email.objects.all().count() == 5
        assert Profile.objects.all().count() == 5
        assert Suggestion.objects.all().count() == 5

    def test_command_with_admin_flag_in_false(
        self, silent_stdout: TextIOWrapper
    ) -> None:
        silent_stdout
        assert User.objects.all().count() == 0
        assert Email.objects.all().count() == 0
        assert Profile.objects.all().count() == 0
        assert Suggestion.objects.all().count() == 0
        call_command(COMMAND, "-i", "5", "-n")
        assert User.objects.all().count() == 5
        assert Email.objects.all().count() == 5
        assert Profile.objects.all().count() == 5
        assert Suggestion.objects.all().count() == 5
