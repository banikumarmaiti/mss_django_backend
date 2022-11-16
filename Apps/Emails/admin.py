from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db.models import Model

from Emails.models import BlackList
from Emails.models import Block
from Emails.models import Email
from Emails.models import Notification
from Emails.models import Suggestion


class BlockAdmin(ModelAdmin):
    model: Model = Block
    list_display: tuple = ("id", "title", "show_link")
    list_display_links: tuple = ("id", "title")
    list_filter: tuple = (
        "title",
        "show_link",
    )
    fieldsets: tuple = (
        ("Content", {"fields": ("id", "title", "content")}),
        ("Link", {"fields": ("show_link", "link_text", "link")}),
    )
    readonly_fields: list = [
        "id",
    ]
    search_fields: tuple = ("title", "id", "link", "link_text", "content")


class EmailAdmin(ModelAdmin):
    model: Model = Email
    list_display: tuple = (
        "id",
        "subject",
        "to",
        "is_test",
        "was_sent",
    )
    list_filter: tuple = ("to", "is_test", "was_sent")
    fieldsets: tuple = (
        ("Content", {"fields": ("id", "subject", "header", "to")}),
        ("Blocks", {"fields": ("blocks",)}),
        (
            "Configuration",
            {"fields": ("is_test", "programed_send_date", "language")},
        ),
        ("Sent information", {"fields": ("was_sent", "sent_date")}),
    )
    list_display_links: tuple = ("id", "subject")
    readonly_fields: list = ["id", "was_sent", "sent_date"]
    search_fields: tuple = ("to", "id", "subject", "programed_send_date")
    ordering: tuple = ("is_test", "was_sent", "sent_date", "to")


class SuggestionAdmin(ModelAdmin):
    model: Model = Suggestion
    list_display: tuple = (
        "id",
        "user",
        "subject",
        "was_sent",
        "was_read",
    )
    list_filter: tuple = ("subject", "user", "was_read", "was_sent")

    fieldsets: tuple = (
        ("Content", {"fields": ("id", "user", "subject", "header")}),
        ("Blocks", {"fields": ("blocks",)}),
        (
            "Configuration",
            {"fields": ("to", "was_read", "was_sent")},
        ),
        ("Sent information", {"fields": ("sent_date",)}),
    )
    list_display_links: tuple = ("id", "user")
    readonly_fields: list = ["id", "was_sent", "sent_date"]
    search_fields: tuple = ("id", "user")
    ordering: tuple = ("was_sent", "was_read")


class BlackListAdmin(ModelAdmin):
    model: Model = BlackList
    list_display: tuple = ("id", "user", "affairs")
    list_display_links: tuple = ("id", "user", "affairs")
    readonly_fields: list = ["id"]
    search_fields: tuple = ("user", "id")
    ordering: tuple = ("affairs",)


class NotificationAdmin(ModelAdmin):
    model: Model = Email
    list_display: tuple = (
        "id",
        "subject",
        "is_test",
        "was_sent",
    )
    list_filter: tuple = ("is_test", "was_sent")
    fieldsets: tuple = (
        ("Content", {"fields": ("id", "subject", "header")}),
        ("Blocks", {"fields": ("blocks",)}),
        (
            "Configuration",
            {"fields": ("is_test", "programed_send_date")},
        ),
        ("Sent information", {"fields": ("was_sent", "sent_date")}),
    )
    list_display_links: tuple = ("id", "subject")
    readonly_fields: list = ["id", "was_sent", "sent_date"]
    search_fields: tuple = ("id", "subject", "programed_send_date")
    ordering: tuple = ("is_test", "was_sent", "sent_date")


admin.site.register(Email, EmailAdmin)
admin.site.register(Block, BlockAdmin)
admin.site.register(Suggestion, SuggestionAdmin)
admin.site.register(BlackList, BlackListAdmin)
admin.site.register(Notification, NotificationAdmin)
