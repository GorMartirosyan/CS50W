from django.contrib import admin
from .models import User, AuctionItem, Comment, Bid

# Register your models here.
admin.site.site_header = "Auction's site Administration"

admin.site.register(AuctionItem)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Bid)

