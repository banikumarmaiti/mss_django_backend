from pytest import mark

from Emails.choices import CommentType
from Emails.fakers.blacklist import BlackListFaker
from Emails.fakers.block import BlockFaker
from Emails.fakers.email import EmailTestFaker
from Emails.fakers.notification import NotificationTestFaker
from Emails.fakers.suggestion import SuggestionErrorFaker
from Emails.models import BlackList
from Emails.models import Block
from Emails.models import Email
from Emails.models import Notification
from Emails.models import Suggestion
from Users.models import User


@mark.django_db
class TestEmailFakers:
    def test_email_faker_creates_email_with_block(self) -> None:
        assert Email.objects.count() == 0
        assert Block.objects.count() == 0
        email: Email = EmailTestFaker()
        assert Email.objects.count() == 1
        assert Block.objects.count() == 1
        assert email.subject == "Test subject"
        assert email.header == "Test header"
        assert email.is_test == True
        assert isinstance(email.to, User)
        assert email.blocks.first() is not None
        block: Block = email.blocks.first()
        assert block.title == "test"
        assert block.content == "test"
        assert block.show_link == True
        assert block.link_text == "test"
        assert block.link == "test.com"


@mark.django_db
class TestBlockFakers:
    def test_block_faker_creates_block(self) -> None:
        assert Block.objects.count() == 0
        block: Block = BlockFaker()
        assert Block.objects.count() == 1
        assert block.title == "test"
        assert block.content == "test"
        assert block.show_link == True
        assert block.link_text == "test"
        assert block.link == "test.com"


@mark.django_db
class TestSuggestionFakers:
    def test_suggestion_faker_creates_suggestion(self) -> None:
        assert Block.objects.count() == 0
        assert Suggestion.objects.count() == 0
        suggestion: Suggestion = SuggestionErrorFaker()
        assert Block.objects.count() == 1
        assert Suggestion.objects.count() == 1
        assert suggestion.subject == CommentType.SUGGESTION.value
        assert suggestion.header == "Test header"
        assert suggestion.blocks.first() is not None
        block: Block = suggestion.blocks.first()
        assert block.title == "test"
        assert block.content == "test"
        assert block.show_link == True
        assert block.link_text == "test"
        assert block.link == "test.com"


@mark.django_db
class TestNotificationFakers:
    def test_notification_faker_creates_notification_and_blocks(self) -> None:
        assert Block.objects.count() == 0
        assert Notification.objects.count() == 0
        notification: Notification = NotificationTestFaker()
        assert Block.objects.count() == 1
        assert Notification.objects.count() == 1
        assert notification.subject == "Test subject"
        assert notification.header == "Test header"
        assert notification.is_test == True
        assert notification.programed_send_date is None
        assert notification.sent_date is None
        assert notification.was_sent is False
        assert notification.blocks.first() is not None
        block: Block = notification.blocks.first()
        assert block.title == "test"
        assert block.content == "test"
        assert block.show_link == True
        assert block.link_text == "test"
        assert block.link == "test.com"

    def test_notification_faker_creates_emails_when_send(self) -> None:
        assert Block.objects.count() == 0
        assert Email.objects.count() == 0
        assert Notification.objects.count() == 0
        notification: Notification = NotificationTestFaker(is_test=True)
        assert Block.objects.count() == 1
        assert Notification.objects.count() == 1
        notification.send()
        assert Email.objects.count() == 1


@mark.django_db
class TestBlackListFakers:
    def test_blacklist_faker_creates_blacklist(self) -> None:
        assert BlackList.objects.count() == 0
        black_list_item: BlackList = BlackListFaker()
        assert BlackList.objects.count() == 1
        assert isinstance(black_list_item.user, User)
        assert black_list_item.affairs is not None
