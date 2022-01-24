from django.contrib import admin
from .models import User,Category,Auction, Bid,Comment,Watchlist, PostImage


# register your models here.
admin.site.register(User)
admin.site.register(Category)

admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)


class PostImageAdmin(admin.StackedInline):
    model = PostImage


@admin.register(Auction)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageAdmin]

    class Meta:
       model = Auction


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass
